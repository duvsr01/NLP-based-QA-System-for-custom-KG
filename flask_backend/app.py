from flask import Flask, jsonify, request
from flask_cors import CORS
import spacy
import requests
from urllib.parse import quote
import json
import pkg_resources
import pickle
from symspellpy import SymSpell, Verbosity
from difflib import get_close_matches
from spacy.matcher import PhraseMatcher
import re
from googletrans import Translator
from suggestions import removePunctuations, chooseWords


sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_dictionary_en_82_765.txt")
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

nlp = spacy.load("en_core_web_trf")

phrase_matcher = PhraseMatcher(nlp.vocab)
prop_phrase_matcher = PhraseMatcher(nlp.vocab)

app = Flask(__name__)
CORS(app)  # Let the api access for frontends.


def get_entity_names(url):
    query = """
                SELECT ?res 
                WHERE {
                  ?entity %s ?res .
                }
            """ % url
    percent_encoded_sparql = quote(query, safe='')

    url = 'http://localhost:3030/ama/sparql?query=%s' % (percent_encoded_sparql)
    response = requests.post(url)
    print(response.json())
    # return json.dumps(response.json())

    if "results" in response.json():
        bindings = response.json()["results"]["bindings"]
        return [binding["res"]["value"] for binding in bindings]
    else:
        return []


def get_entity_properties():
    query = """
                SELECT DISTINCT ?predicate 
                WHERE {
                  ?entity ?predicate ?object .
                }
            """
    percent_encoded_sparql = quote(query, safe='')

    url = 'http://localhost:3030/ama/sparql?query=%s' % (percent_encoded_sparql)
    response = requests.post(url)
    print(response.json())
    # return json.dumps(response.json())

    if "results" in response.json():
        bindings = response.json()["results"]["bindings"]
        ans = []
        for binding in bindings:
            match = re.search(r'http://www.w3.org/2001/ama/sjsu#?([^\']+)', binding["predicate"]["value"])
            # ans.append(binding["predicate"]["value"].split("#")[1])
            if match:
                print(match.group(1))
                ans.append(match.group(1))

        print(ans)
        return ans
        # return [binding["res"]["value"] for binding in bindings]
    else:
        return []


entity_names_arr = get_entity_names("<http://www.w3.org/2001/ama/sjsu#name>")
alias_names_arr = get_entity_names("<http://www.w3.org/2001/ama/sjsu#hasAlias>")
entity_names = set(entity_names_arr)
# phrases = ['machine learning', 'robots', 'intelligent agents']
phrases = entity_names_arr
patterns = [nlp(text) for text in phrases]
phrase_matcher.add('AI', None, *patterns)
entity_properties = get_entity_properties()
entity_properties.extend(alias_names_arr)
print("entity_properties", entity_properties)
prop_patterns = [nlp(text) for text in entity_properties]
prop_phrase_matcher.add('property', None, *prop_patterns)


# on the terminal type: flask run or curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/', methods=['GET'])
def home():
    if (request.method == 'GET'):
        data = "hello world"
        return jsonify({'data': data})


# post request accepts a query argument value
# return status string
@app.route('/question', methods=['POST'])
def process():
    error = ''
    try:
        data = request.json
        print("data", data)

        question = data['question']
        print("question", question)

        version = 3
        langCode = "en"
        
        doc = nlp(question)
        entity_set = []
        property_set = []

        matched_phrases = phrase_matcher(doc)
        for match_id, start, end in matched_phrases:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            entity_set.append(span.text)

        if version >= 2:
            print("version", version)

            tokens = []
            for token in doc:
                if token.pos_ == "NOUN":
                    print(token.text)

                    input_term = token.text  # misspelling of "members"
                    # max edit distance per lookup
                    # (max_edit_distance_lookup <= max_dictionary_edit_distance)

                    suggestions = sym_spell.lookup(input_term, Verbosity.CLOSEST,
                                                   max_edit_distance=2)
                    # display suggestion term, term frequency, and edit distance
                    for suggestion in suggestions:
                        print("suggestion", suggestion.term)
                        tokens.append(suggestion.term)
                        break
                else:
                    tokens.append(token.text)

                doc = nlp(" ".join(tokens))

        matched_phrases_prop = prop_phrase_matcher(doc)
        for match_id, start, end in matched_phrases_prop:
            string_id = nlp.vocab.strings[match_id]
            span = doc[start:end]
            print(match_id, string_id, start, end, span.text)
            property_set.append(span.text)

        entities = doc.ents
        print("** property_set", property_set)

        print("** entities")
        for entity in entities:
            print(entity.text, entity.label_)

            if version >= 3:
                print("entity_names", entity_names)
                if entity.text not in entity_names:
                    close_matches = get_close_matches(entity.text, entity_names)
                    for close_match in close_matches:
                        if close_match not in entity_set:
                            entity_set.append(close_match)
                            break
            else:
                if str(entity.text) not in entity_set:
                    entity_set.append(str(entity.text))

        print("entitySet")
        print(entity_set)

        for token in doc:
            print(token, token.pos_)

        # print("Nouns:", [token.text for token in doc if token.pos_ == "NOUN"])
        # pos_nouns = [token.text for token in doc if token.pos_ == "NOUN" and len(token) >= 2]

        print("chunks")
        chunks = set()
        for chunk in doc.noun_chunks:
            print(chunk.text, chunk.label_, chunk.root.text)

        # Try to find entities from chunks
        if version >= 3:
            if len(entity_set) == 0:
                for chunk in doc.noun_chunks:
                    if chunk.label_ == "NP":
                        close_matches = get_close_matches(chunk.text, entity_names)
                        print("entity.text", chunk.text)
                        print("close_matches", close_matches)
                        for close_match in close_matches:
                            entity_set.append(close_match)
                            break
        if len(property_set) > 1:
            property_set = property_set[:1]

        if (len(entity_set) == 1) and (len(property_set) == 1):
            result_obj = one_entity_one_predicate(entity_set, property_set, langCode)
            print("result_obj", result_obj)
            result = json.loads(result_obj)

            if "results" in result:
                bindings = result["results"]["bindings"]
                for binding in bindings:
                    return binding["answer"]["value"]
                    break

            return getQueryResults(entity_set, langCode)
        elif len(entity_set) == 1 and len(property_set) != 1:
            return getQueryResults(entity_set, langCode)
        else:
            return getQueryResults(entity_set, langCode)

    except Exception as e:
        print(e)
        return "Error occurred!!" + e


def one_entity_one_predicate(entitySet, property_set, langCode):
    data = {'entities': []}
    print("entity", entitySet[0])
    entity = entitySet[0]
    print("property", property_set[0])
    noun = property_set[0]

    # query = """
    #     SELECT ?answer
    #     WHERE {
    #
    #       ?subject <http://www.w3.org/2001/ama/sjsu#name> "%s" .
    #       ?subject <http://www.w3.org/2001/ama/sjsu#%s>|<http://www.w3.org/2001/ama/sjsu#hasAlias> ?answer
    #     }
    #     """ % (entity, noun)

    query = """
    SELECT DISTINCT ?answer
    WHERE {
      {
         ?subject <http://www.w3.org/2001/ama/sjsu#name> "%s"
         OPTIONAL
         {
            ?subject <http://www.w3.org/2001/ama/sjsu#%s> ?answer .
         }
      } 
      UNION 
      {
         ?subject <http://www.w3.org/2001/ama/sjsu#name> "%s"
         OPTIONAL
         {
            ?prop <http://www.w3.org/2001/ama/sjsu#hasAlias> "%s" .
            ?subject ?prop ?answer
         }
      }
      FILTER(strlen(?answer)>0)
    }
    """% (entity, noun, entity, noun)

    percent_encoded_sparql = quote(query, safe='')

    url = 'http://localhost:3030/ama/sparql?query=%s' % (percent_encoded_sparql)
    response = requests.post(url, data=data)
    print(response.json())
    return json.dumps(response.json())


def getQueryResults(entitySet, langCode):
    data = {}
    return json.dumps(data)



# post request accepts a string 
# returns list of sentence suggestions
@app.route('/suggestions', methods=['POST'])
def suggestion_process():
    error = ''
    try:
        data = request.json
        print("data", data)
        question = data['question']

        if(not (question and not question.isspace())):
            return ('', 204)

       # Text Pre-Processing on the sentence typed
        sen = removePunctuations(question)
        temp = sen.split()
        if len(temp) < 3:
            print("Please enter atleast 3 words !")
        else:
            temp = temp[-3:]
        sen = " ".join(temp)

        print("processed text: ",sen)
        
        ### PREDICTION
        # choose most probable words for prediction
        # load the pre-computed probability dictionaries from pickle files
        with open('./pickle/bi_prob_dict.pickle', 'rb') as bi_prob:
                bi_prob_dict = pickle.load(bi_prob)

        with open('./pickle/tri_prob_dict.pickle', 'rb') as tri_prob:
                tri_prob_dict = pickle.load(tri_prob)

        with open('./pickle/quad_prob_dict.pickle', 'rb') as quad_prob:
                quad_prob_dict = pickle.load(quad_prob)

        word_choice = chooseWords(sen,bi_prob_dict,tri_prob_dict,quad_prob_dict)
        
        print("word_choices are: ",word_choice)
        
        result = set()
        for word in word_choice:
            key = sen + ' ' + word[1]
            result.add(key)

        def convert_to_list(obj):
            if isinstance(obj, set):
                return list(obj)
            raise TypeError

        response = json.dumps(result, default=convert_to_list)  
        print(response)

        return response

    except Exception as e:
        print(e)
        return "Error occurred!!" + e


# driver function
if __name__ == '__main__':
    app.run(debug=False)
    # app.run(host='0.0.0.0', port = 5001)

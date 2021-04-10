from flask import Flask, jsonify, request
from flask_cors import CORS
import spacy
import requests
from urllib.parse import quote
import json
import pkg_resources
from symspellpy import SymSpell, Verbosity

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_dictionary_en_82_765.txt")
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

nlp = spacy.load("en_core_web_trf")

app = Flask(__name__)
CORS(app)  # Let the api access for frontends.

# on the terminal type: flask run or curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/', methods=['GET'])
def home():
    if(request.method == 'GET'):
        data = "hello world"
        return jsonify({'data': data})

# post request accepts a query argument value
# return status string
@app.route('/question', methods=['POST'])
def process():
    error = ''
    try:
        data = request.json
        question = data['question']
        version = data['version']

        print(question)

        langCode = "en"
        doc = nlp(question)

        if version == "v2":
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

        for token in doc:
            print(token, token.pos_)

        print("Nouns:", [token.text for token in doc if token.pos_ == "NOUN"])
        pos_nouns = [token.text for token in doc if token.pos_ == "NOUN" and len(token) >= 2]

        entities = doc.ents

        entitySet = []

        print("** entities")
        for entity in entities:
            print(entity.text, entity.label_)
            entitySet.append(str(entity))
            # splits = str(entity).split(" ")
            #
            # for split in splits:
            #     entitySet.add(str(split).strip())

        print("entitySet")
        print(entitySet)

        print("chunks")
        chunks = set()
        for chunk in doc.noun_chunks:
            print(chunk.text, chunk.label_, chunk.root.text)
        if (len(entitySet) == 1) and (len(pos_nouns) == 1):
            result_obj = one_entity_one_predicate(entitySet, pos_nouns, langCode)
            result = json.loads(result_obj)
            answer = result["results"]["bindings"][0]["answer"]["value"]
            print(answer)
            return(answer)
        elif len(entitySet) == 1 and len(pos_nouns) != 1:
            # print("pos_nouns", pos_nouns)
            # result = json.loads(result_obj)
            # answer = result["results"]["bindings"][0]["answer"]["value"]
            # print(answer)
            # return(answer)
            return getQueryResults(entitySet, langCode)
        else:
            return getQueryResults(entitySet, langCode)

    except Exception as e:
        print(e)
        return "Error occurred!!" + e


def one_entity_one_predicate(entitySet, pos_nouns, langCode):
        data = {'entities': []}
        print("entity", entitySet[0])
        entity = entitySet[0]
        print("noun", pos_nouns[0])
        noun = pos_nouns[0]

        query = """
            SELECT ?answer 
            WHERE {
              
              ?subject <http://www.w3.org/2001/ama/sjsu#name> "%s" .
              ?subject <http://www.w3.org/2001/ama/sjsu#%s> ?answer
            }
            """ % (entity, noun)

        percent_encoded_sparql = quote(query, safe='')

        url = 'http://localhost:3030/ama/sparql?query=%s' % (percent_encoded_sparql)
        response = requests.post(url, data=data)
        print(response.json())
        return json.dumps(response.json())

def getQueryResults(entitySet, langCode):
        data = {}
        return json.dumps(data)


# driver function
if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0', port = 5001)

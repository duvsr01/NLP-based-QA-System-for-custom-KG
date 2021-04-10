import json
import spacy
import requests
from urllib.parse import quote
from spacy import displacy

import re
from klein import Klein
from SPARQLWrapper import SPARQLWrapper, JSON

nlp = spacy.load("en_core_web_trf")

class ItemStore(object):
    app = Klein()

    def _init_(self):
        self._items = {}

    @app.route('/')
    def items(self, request):
        request.setHeader('Content-Type', 'application/json')
        return json.dumps(self._items)

    @app.route('/<string:name>', methods=['POST'])
    def post_item(self, request, name):
        request.setHeader('Content-Type', 'application/json')
        content = json.loads(request.content.read())

        #print("123langCode")
        #print(content["langCode"])langCode
        langCode = "en"
        text = content["data"]

        print("pure text")
        print(text)

        # text = text\
        #     .replace("\r", " ")\
        #     .replace("\n", " ") \
        #     .replace("gm", " ") \
        #     .replace("mg/dl", " ")\
        #     .replace("high", " ") \
        #     .lower()
        #
        # text = re.sub(r'[^A-Za-z ]+', " is a ", text)
        # text = re.sub(' +', " ", text)
        #
        # text = text \
        #     .replace("high", " ")\
        #     .replace("desirable", " ")\
        #     .replace("borderline", " ")

        # text = re.sub(' +', " ", text)
        #
        # print("regexed text")
        # print(text)

        # sentence = sp(text)
        # text = " ".join([token.lemma_ for token in sentence])
        #
        # print("lemmatized text")
        # print(text)

        doc = nlp(json.dumps(text))

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

        print("chunks") #What is emal of Dan
        # What machine learning course are offered by CMPE depart?
        # ?ent - category - "machine learning"
        # ?ent - offeredBy - "CMPE departmnet"
        # ?ent - type - course
        chunks = set()
        for chunk in doc.noun_chunks:
            print(chunk.text, chunk.label_, chunk.root.text)

        if (len(entitySet) == 1) and (len(pos_nouns) == 1):
            return self.one_entity_one_predicate(entitySet, pos_nouns, langCode)
        elif len(entitySet) == 1 and len(pos_nouns) != 1:
            print("pos_nouns", pos_nouns)


            return self.one_entity_one_predicate(entitySet, pos_nouns, langCode)
        else:
            return self.getQueryResults(entitySet, langCode)

    def one_entity_one_predicate(self, entitySet, pos_nouns, langCode):
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

    def getQueryResults(self, entitySet, langCode):
        data = {}

        # for entity in entitySet:
        #     # result_entity = dict()
        #     result_entity = {"entityName": "", "comment": "", "foods": [], "diseases": []}
        #
        #     abstract_sparql_query = self.getAbstractQuery(entity, langCode)
        #     abstract_query_results = abstract_sparql_query.query().convert()
        #
        #     print("abstract_query_results")
        #     print(abstract_query_results)
        #
        #     if len(abstract_query_results["results"]["bindings"]) == 0:
        #         continue
        #
        #     for result in abstract_query_results["results"]["bindings"]:
        #         result_entity["entityName"] = entity
        #         #result_entity['entityURI'] = str(result["chem"]["value"])
        #         result_entity["comment"] = str(result["comment"]["value"])
        #         #print(result_entity)

            # food_sparql_query = self.getFoodQuery(entity, langCode)
            # food_query_results = food_sparql_query.query().convert()
            #
            # for result in food_query_results["results"]["bindings"]:
            #     result_entity["foods"].append(str(result["label"]["value"]))

            # food_dict = dict()
            # food_sparql_query = self.getLowFoodQuery(entity, langCode)
            # food_query_results = food_sparql_query.query().convert()
            #
            # for result in food_query_results["results"]["bindings"]:
            #     result_entity["foods"].append(str(result["label"]["value"]))

            # food_sparql_query = self.getFoodQuery(entity, langCode)
            # food_query_results = food_sparql_query.query().convert()
            #
            # for result in food_query_results["results"]["bindings"]:
            #     result_entity["foods"].append(str(result["label"]["value"]))
            #
            #
            # disease_sparql_query = self.getDiseaseQuery(entity, langCode)
            # disease_query_results = disease_sparql_query.query().convert()
            #
            # for result in disease_query_results["results"]["bindings"]:
            #     result_entity["diseases"].append(str(result["label"]["value"]))
            #
            # data['entities'].append(result_entity)

        return json.dumps(data)

    # def getAbstractQuery(self, entity, langCode):
    #     sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    #     sparql.setReturnFormat(JSON)
    #     query = """
    #         PREFIX dbo: <http://dbpedia.org/ontology/>
    #     PREFIX dbp: <http://dbpedia.org/resource/>
    #     PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    #     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    #     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    #
    #     SELECT distinct(?chem) ?comment where
    #        {
    #         ?chem rdf:type dbo:ChemicalCompound .
    #         ?chem rdfs:label ?label .
    #         ?chem rdfs:comment ?comment .
    #         FILTER regex(?label, "^%s$", "i")
    #         FILTER (langMatches(lang(?comment),"%s"))
    #        }
    #     """ % (entity, langCode)
    #
    #     #print("query")
    #     #print(query)
    #
    #     sparql.setQuery(query)
    #
    #     return sparql
    #
    # def getFoodQuery(self, entity, langCode):
    #     sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    #     sparql.setReturnFormat(JSON)
    #     query = """
    #         PREFIX dbo: <http://dbpedia.org/ontology/>
    #     PREFIX dbp: <http://dbpedia.org/resource/>
    #     PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    #     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    #     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    #
    #     SELECT distinct(?food) ?label where
    #        {
    #         ?food rdf:type dbo:Food .
    #         ?food rdfs:label ?label .
    #         ?food dbo:abstract ?abstract .
    #         FILTER regex(?abstract, "%s", "i")
    #         FILTER (langMatches(lang(?label),"%s"))
    #         FILTER (langMatches(lang(?abstract),"%s"))
    #        }
    #     """ % (entity, langCode, langCode)
    #
    #     sparql.setQuery(query)
    #
    #     return sparql
    #
    # def getLowFoodQuery(self, entity, langCode):
    #     sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    #     sparql.setReturnFormat(JSON)
    #     query = """
    #         PREFIX dbo: <http://dbpedia.org/ontology/>
    #     PREFIX dbp: <http://dbpedia.org/resource/>
    #     PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    #     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    #     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    #
    #     SELECT distinct(?food) ?label where
    #        {
    #         ?food rdf:type dbo:Food .
    #         ?food rdfs:label ?label .
    #         ?food dbo:abstract ?abstract .
    #         FILTER regex(?abstract, "%s", "i")
    #         FILTER (langMatches(lang(?label),"%s"))
    #         FILTER (langMatches(lang(?abstract),"%s"))
    #        }
    #     """ % (entity, langCode, langCode)
    #
    #     sparql.setQuery(query)
    #
    #     return sparql
    #
    #
    # def getDiseaseQuery(self, entity, langCode):
    #     sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    #     sparql.setReturnFormat(JSON)
    #     query = """
    #     PREFIX dbo: <http://dbpedia.org/ontology/>
    #     PREFIX dbp: <http://dbpedia.org/resource/>
    #     PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    #     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    #     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    #
    #     SELECT distinct(?chem) ?label where
    #        {
    #         ?chem rdf:type dbo:Disease .
    #         ?chem rdfs:label ?label .
    #         ?chem dbo:abstract ?abstract .
    #         FILTER regex(?abstract, "%s", "i")
    #         FILTER (langMatches(lang(?label),"%s"))
    #         FILTER (langMatches(lang(?abstract),"%s"))
    #        }
    #     """ % (entity, langCode, langCode)
    #
    #     sparql.setQuery(query)
    #
    #     return sparql


if __name__ == '__main__':
    store = ItemStore()
    store.app.run('localhost', 8080)
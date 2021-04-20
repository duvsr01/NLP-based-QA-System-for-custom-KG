# NLP-based-QA-System-for-custom-KG

AMA has 3 versions, each of which gives better results as you go higher in the version
1. Version 1 - No optimization
2. Version 2 - Spelling correction in nouns
3. Version 3 - Fuzzy matching of entities + using chunking to extract entities + all features of version 2

Processing pipeline with example -
"What is the emaul of Dan Harky?" with version 3

1. phrase_matcher is given names of entities (such as "Dan Harkey", "CMPE", etc.) and asked to find if any of the supplied entities are present in the question.
Output = None since there is typo in "Dan Harky" and it will not match with "Dan Harkey"

2. Since, we are at version 3, we will perform spelling correction in NOUN using sym_spell.lookup(). This would correct "emaul" to "email".

3. phrase_matcher is given names of properties (such as "email", "tuition fees", etc.) and asked to find if any of the supplied properties are present in the question.
Output = email

4. We perform spaCy NER and use get_close_matches to do fuzzy matching of entities returned by NER
NER output = "Dan Harky" <PERSON>
get_close_matches output = "Dan Harkey"
  
5. We generate chunks using spaCy and 
Chunker output =
chunks
What NP What
the email NP email
Dan Harky NP Harky

get_close_matches output = "Dan Harkey"

6. Supply the entity and property to SPARQL query
Use aliases to get all answers. For example, "email" can have aliases such as "sjsu contact", "contact email", etc. All of them are resolved to "email".
So all three below questions will produce same answer -
"What is the email of Dan Harky?"
"What is the sjsu contact of Dan Harky?"
"What is the contact email of Dan Harky?"

`query = """
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
    """% (entity, noun, entity, noun)`


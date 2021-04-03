1. Install all Python libraries present in `klien-server.py` file
2. Install `python3 -m spacy download en_core_web_sm`
3. Make sure custom KG is running on Fuseki by following "Steps to perform REST query using Apache Jena Fuskei"
4. Frontend needs to make a POST call to `http://localhost:8080/ok` with JSON body as -
`{"data": "What is email of Dan Harkey?",
"langCode": "en"}`
4. Answer would be in `results`

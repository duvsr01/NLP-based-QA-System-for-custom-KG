1. Install all Python libraries present in `klien-server.py` file
2. Install `python3 -m spacy download en_core_web_trf`
3. If you get a timeout, you can use `sudo pip install --default-timeout=100 future` and then re-try   
4. Make sure custom KG is running on Fuseki by following "Steps to perform REST query using Apache Jena Fuskei"
5. Frontend needs to make a POST call to `http://localhost:8080/ok` with JSON body as -
`{"data": "What is email of Dan Harkey?",
"langCode": "en"}`
6. Answer would be in `results`
7. Please see below screenshow from Postman for reference -
![Image of Yaktocat](https://github.com/duvsr01/NLP-based-QA-System-for-custom-KG/blob/main/klien/images/end-to-end-postman.png)

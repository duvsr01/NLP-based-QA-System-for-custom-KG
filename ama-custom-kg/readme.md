# Steps to perform REST query using Apache Jena Fuskei

1. Download and uncompress Apache Jena Fuseki zip file from here - https://archive.apache.org/dist/jena/binaries/apache-jena-fuseki-3.16.0.zip
2. Go to the uncompressed Fueski dir and place this file there - https://drive.google.com/file/d/1JU_AV1ngZCMU8lGNL1GXRUEHyNbsJjpw/view?usp=sharing
3. To start the server, run command - ./fuseki-server --file latest.nt /ama
4. To execute SPARQL query using web UI, go to the following link and enter your query http://localhost:3030/dataset.html?tab=query&ds=/ama
For example, you can try below SPARQL queries
```javascript
#All subjects in SJSU
SELECT ?name 
WHERE {
  ?subject <http://www.w3.org/2001/ama/sjsu#type> "course" .
  ?subject <http://www.w3.org/2001/ama/sjsu#name> ?name
}
LIMIT 25
```


```javascript
#All subjects in CMPE department
SELECT ?name 
WHERE {
  ?subject <http://www.w3.org/2001/ama/sjsu#type> "course" .
  ?subject <http://www.w3.org/2001/ama/sjsu#department> ?department .
  ?department <http://www.w3.org/2001/ama/sjsu#name> "CMPE" .
  ?subject <http://www.w3.org/2001/ama/sjsu#name> ?name
}
LIMIT 25
```

5. To execute query over REST (using Postman or REST calls in code), use the GET url http://localhost:3030/ama/sparql?query=<your-query>
Replace <your-query> with percent encoded query. For example, if your query is - 
  
```javascript
#All subjects in SJSU
SELECT ?name 
WHERE {
  ?subject <http://www.w3.org/2001/ama/sjsu#type> "course" .
  ?subject <http://www.w3.org/2001/ama/sjsu#name> ?name
}
LIMIT 25
```
then if you percent encode it (can be done via this web tool https://www.url-encode-decode.com/), it will become 

 `
SELECT+%3Fname+%0D%0AWHERE+%7B%0D%0A++%3Fsubject+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2Fama%2Fsjsu%23type%3E+%22course%22+.%0D%0A++%3Fsubject+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2Fama%2Fsjsu%23name%3E+%3Fname%0D%0A%7D
 `

So, your final GET call will be  -
 `http://localhost:3030/ama/sparql?query=SELECT+%3Fname+%0D%0AWHERE+%7B%0D%0A++%3Fsubject+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2Fama%2Fsjsu%23type%3E+%22course%22+.%0D%0A++%3Fsubject+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2Fama%2Fsjsu%23name%3E+%3Fname%0D%0A%7D`
 
 

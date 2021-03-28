# Steps to perform REST query using Apache Jena Fuskei

1. Download and uncompress Apache Jena Fuseki zip file from here - https://archive.apache.org/dist/jena/binaries/apache-jena-fuseki-3.16.0.zip
2. Go to the uncompressed Fueski dir and place this file there - https://drive.google.com/file/d/1JU_AV1ngZCMU8lGNL1GXRUEHyNbsJjpw/view?usp=sharing
3. To start the server, run command - ./fuseki-server --file latest.nt /ama
4. To execute SPARQL query using web UI, go to the following link and enter your query http://localhost:3030/dataset.html?tab=query&ds=/ama
For example,
#All subjects in SJSU
SELECT ?name 
WHERE {
  ?subject <http://www.w3.org/2001/ama/sjsu#type> "course" .
  ?subject <http://www.w3.org/2001/ama/sjsu#name> ?name
}
LIMIT 25



#All subjects in CMPE department
SELECT ?name 
WHERE {
  ?subject <http://www.w3.org/2001/ama/sjsu#type> "course" .
  ?subject <http://www.w3.org/2001/ama/sjsu#department> ?department .
  ?department <http://www.w3.org/2001/ama/sjsu#name> "CMPE" .
  ?subject <http://www.w3.org/2001/ama/sjsu#name> ?name
}
LIMIT 25

6. 


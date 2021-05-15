<h1>NLP based Question Answering (QA) System for custom KG</h1>

<h3>Introduction</h3>
Question Answering systems utilize information retrieval techniques to retrieve the most relevant information based upon a user query in natural language posed against various data sources like knowledge graphs, relational databases, or documents.

In this project, we propose a Question Answering system that can answer factoid questions using a knowledge graph that will allow us to scale the number of entities and relationships among them. This system accepts user questions in natural language and uses Natural Language Processing techniques to understand the question and produce answers by querying the knowledge graph. The project will also give the user the ability to customize the system by providing support for the usage of custom knowledge graphs.

<h3>Steps to build the application</h3>
Our QA system has 4 components and steps to build each are listed below -

1. [UI](https://github.com/duvsr01/NLP-based-QA-System-for-custom-KG/tree/main/frontend) that provides a user friendly experience to ask questions
2. [Flask backend](https://github.com/duvsr01/NLP-based-QA-System-for-custom-KG/tree/main/flask_backend) that uses entity and relationship recognition to answer question
3. [Rules backend](https://github.com/duvsr01/NLP-based-QA-System-for-custom-KG/tree/main/backend) uses NLP techniques and rules to answer questions
4. [Custom KG](https://github.com/duvsr01/NLP-based-QA-System-for-custom-KG/tree/main/ama-custom-kg) allows users to create a custom KG

<h3>Architecture</h3>

![](https://github.com/duvsr01/NLP-based-QA-System-for-custom-KG/blob/main/klien/images/ama-archi.png)

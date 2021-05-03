# To run flask backend


Inside flask_backend folder -> create python3 virtual environment

source env/bin/activate

# Install all dependencies

pip install -r requirements.txt


# To start Bert as a Service:
  1. pip install tensorflow=1.13
     pip install -U bert-serving-server bert-serving-client
  
  2. Download a Pre-trained BERT Model : https://bert-as-service.readthedocs.io/en/latest/section/get-start.html. eg : BERT-Base, Uncased
  3. To start BERT as a service, run the following command in the terminal :
     bert-serving-start -model_dir uncased_L-12_H-768_A-12/ -num_worker=1&
  
 # To run flask server:

python3 app.py
The flask server should be up and running and API requests can now be made.



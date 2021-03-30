# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import sys

#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
#import pdb;
#pdb.set_trace()
#sys.path.append('/Users/jainsh/Documents/cmpe295/NLP-based-QA-System-for-custom-KG-demo')
import sys
from os import path
sys.path.append(path.dirname(__file__))
#print(sys.path)
#print(sys.path[1])
from backend.app.dbpedia.main import quepy_main

# creating a Flask app
#import pdb; pdb.set_trace()
app = Flask(__name__)
CORS(app)  # Let the api acces for frontends.
load_dotenv()



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
        print(question)
        #str_return = 'answer'
        str_return = quepy_main(question)
        # quepy_main(question)
        return str_return

    except Exception as e:
        print(e)
        return "Error occurred!!" + e


def run_app():
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5001)


# driver function
if __name__ == '__main__':
    run_app()
# app.run(debug= True) # This has to be used while debugging. The other while deployment.

# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

from backend.app.dbpedia.main import quepy_main

# creating a Flask app
#import pdb; pdb.set_trace()
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}}) # Let the api acces for frontends.
#CORS(app)  # Let the api acces for frontends.
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


# search api
@app.route('/search', methods=['POST'])
def search():
    # If you send json body, you have to access like this only # https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request

    print(request.json)
    data = request.json

    # Putting label and value into result object.
    answer = "here is your answer"
    return jsonify({'answer': answer})


# driver function
# if __name__ == '__main__':
#     run_app()
# app.run(debug= True) # This has to be used while debugging. The other while deployment.

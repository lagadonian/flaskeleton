import time
import json
from pprint import pprint

from flask import Flask, jsonify, request

application = Flask(__name__)

@application.route("/")
def hello():
    return "Hello World!"

#example API function
#curl -d @"testdata.json" -X POST http://localhost:5000/num/3 -H "Content-Type: application/json"

@application.route('/num/<int>', methods=['GET', 'POST'])
def thricer(int): 
    if (request.method == 'POST'):
		msg_json = request.get_json()
		num1 = int(msg_json["num1"])
		num2 = int(msg_json["num2"])
		answer = 3*num1*num2
		return jsonify({'answer': answer})


    else:
        return jsonify({'INSTRUCTIONS': 'include params num1 (int) and num2 (int)'})


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
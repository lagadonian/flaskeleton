import time
import json
from pprint import pprint
import tests

from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo



application = Flask(__name__)

application.config['MONGO_DBNAME'] = 'restdb'
#https://mlab.com/databases/restdb#users
application.config['MONGO_URI'] = 'mongodb://lagadonian:lagadonian@ds157057.mlab.com:57057/restdb'

mongo = PyMongo(application)




"""
Hello, World!
"""
@application.route("/")
def hello():
    return render_template('index.html')



@application.route('/work1', methods=['GET', 'POST'])
def work(): 
    return jsonify({"directory": {"check": "/work1/check",
                                    "work": "work1/work"}})
"""
example API function: given three numbers and worker address, sends a "wallet key"
if they add up to more than 10 and worker is new, sends an error otherwise.
"""
#curl -d @"testdata2.json" -X POST http://localhost:5000/work1/work -H "Content-Type: application/json"
#curl -d @"testdata2bad.json" -X POST http://localhost:5000/work1/work -H "Content-Type: application/json"

#function that pays out if data/user passes the test(s)

"""
pickled TEST needs to be stored on blockchain and referenced in work manifest
then, worker() needs to be agnostic about what test it is running
"""



@application.route('/<job>/work', methods=['GET', 'POST'])
def worker(job): 
    instructions = getattr(tests, job+'i')
    tester = getattr(tests, job+'t')

    if (request.method == 'POST'):
        

        msg_json = request.get_json()
        address = str(msg_json["ad"])
        data = msg_json["data"]


        rewardKey = 839330039930

        ads = mongo.db.ads
        flag = ads.find_one({"ad": address, "job": job})
        testresult = tester(data)

        if not flag and testresult:
            ads.insert({'ad': address, "job": job})
            return jsonify({'reward': rewardKey})
        else: 
            if flag: 
                return jsonify({'reward': 'None; address used'})
            return jsonify({'reward': 'None; bad data'})


    else:
        return jsonify({'instructions': instructions})



#testing worker
#curl -d @"stestdata1.json" -X POST http://localhost:5000/work1/check -H "Content-Type: application/json"
#curl -d @"stestdata2.json" -X POST http://localhost:5000/work1/check -H "Content-Type: application/json"
@application.route('/<job>/check', methods=['GET', 'POST'])
def checker(): 
    if (request.method == 'POST'):
        msg_json = request.get_json()
        address = str(msg_json["ad"])
        ads = mongo.db.ads
        flag = not ads.find_one({"ad": address})
        return jsonify({'qualify': flag})
    else:
        return jsonify({'instructions': 'include parameter ad (stellar address) to see if you qualify'})




if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
import time
import json
from pprint import pprint


from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo



application = Flask(__name__)

application.config['MONGO_DBNAME'] = 'restdb'
#https://mlab.com/databases/restdb#users
application.config['MONGO_URI'] = 'mongodb://<username>:<password>@ds157057.mlab.com:57057/restdb'

mongo = PyMongo(application)




"""
Hello, World!
"""
@application.route("/")
def hello():
    return render_template('index.html')



@application.route('/<job>', methods=['GET', 'POST'])
def work(job): 
    return jsonify({"directory": {"check": job+"/check",
                                    "work": job+"/work"}})
"""
example API function: given three numbers and worker address, sends a "wallet key"
if they add up to more than 10 and worker is new, sends an error otherwise.
"""
#curl -d @"testdata2.json" -X POST http://localhost:5000/work1/work -H "Content-Type: application/json"
#curl -d @"testdata2bad.json" -X POST http://localhost:5000/work1/work -H "Content-Type: application/json"

#function that pays out if data/user passes the test(s)


@application.route('/<job>/work', methods=['GET', 'POST'])
def worker(job): 
    module = __import__(job)
    instructions = getattr(module, job+'i')
    requirements = getattr(module, job+'r')
    tester = getattr(module, job+'t')
    rewardKey = getattr(module, job+'s')

    if (request.method == 'POST'):
        

        msg_json = request.get_json()
        address = str(msg_json["ad"])
        data = msg_json["data"]



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
def checker(job): 
    module = __import__(job)
    requirements = getattr(module, job+'r')

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

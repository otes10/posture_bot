from flask import Flask, request, jsonify
from flask_restful import abort, Api, Resource
from PIL import Image
from aws import get_object, get_total_bytes

import glob
import json


app = Flask(__name__)
api = Api(app)

@app.route("/current", methods=["POST"])
def current_report():
    filename = request.args.get('date','') + '.json'
    total_bytes = get_total_bytes(filename)
    data = json.load(get_object(total_bytes, filename))
    # with open(f"/home/pi/nwhacks/api/data/{filename}.json") as f:
        # data = json.load(f)
    return jsonify({filename: data})

@app.route("/hourly", methods=["POST"])
def hourly_report():
    result = request.args
    filename = result.get('date') + '.json'
    hour = result.get('hour')
    # # with open(f"/home/pi/nwhacks/api/data/{filename}.json") as f:
    # #     data = json.load(f)
    total_bytes = get_total_bytes(filename)
    data = json.load(get_object(total_bytes, filename))
    print(type(result))
    return jsonify({filename:hour})

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, jsonify, send_file
from flask_restful import abort, Api, Resource
from aws import get_object, get_total_bytes

import io
import json
import base64

app = Flask(__name__)
api = Api(app)

@app.route("/current", methods=["POST"])
def current_report():
    filename = request.args.get('date','')
    data = json.load(open(f"/home/pi/nwhacks/api/data/{filename}.json"))
    return jsonify({filename: data})

@app.route("/hourly", methods=["POST"])
def hourly_report():
    result = request.args
    filename = result.get('date')
    hour = result.get('hour')
    data = json.load(open(f"/home/pi/nwhacks/api/data/{filename}.json"))

    result = []
    for item in data:
        if item['hour'] == str(hour):
            result.append(item)

    return jsonify({filename:result})

@app.route("/image", methods=["POST"])
def get_image():
    filename = '/photos/' + request.args.get('datetime','') + '.jpg'
    total_bytes = get_total_bytes(filename)
    data = get_object(total_bytes, filename)

    return data

if __name__ == "__main__":
    app.run(debug=True)
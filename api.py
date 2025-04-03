from flask import Flask, jsonify, request
import subprocess
from datetime import datetime

app = Flask(__name__)
#https://medium.com/@asvinjangid.kumar/creating-your-own-api-in-python-a-beginners-guide-59f4dd18d301
@app.route('/logs', methods=['GET'])
def get_logs():
    result = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    return jsonify({'date': result.strip()})

@app.route('/logs', methods=['POST'])
def post_logs():
    new_log = request.get_json()

    if not new_log:
        return jsonify({"error": "No JSON received"}), 400
    
    service_name = new_log.get('service_name', '?')
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    message = new_log.get('message', '?')

    return jsonify({
        "service_name": service_name,
        "timestamp": timestamp,
        "message": message
    })


if __name__ == '__main__':
    app.run()
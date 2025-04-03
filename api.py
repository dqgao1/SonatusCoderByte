from flask import Flask, jsonify, request
import subprocess
from datetime import datetime
import time
import threading


app = Flask(__name__)
app.json.sort_keys = False # doesn't sort the json collection, without this message was first before timestamp (Constraint: Handling Unordered Logs)

logs = []

EXPIRATION =  3600 # set time to remove logs (1hr)
#EXPIRATION = 10 # set time to remove logs(1m) TEST case

def remove_expired_logs():
    while True:
        current_time = time.time()
        print(f"{current_time} Running checks for expired logs")
        global logs
        new_logs = []
        for log in logs:
            datetime_obj = datetime.strptime(log['timestamp'].replace("T"," ").replace("Z",""), '%Y-%m-%d %H:%M:%S')
            timestamp = datetime_obj.timestamp()
            if current_time - timestamp < EXPIRATION:
                new_logs.append(log)
            else:
                print("Log expired")

        logs = new_logs
        time.sleep(60)
        
#Constraint: Thread-safee design
threading.Thread(target=remove_expired_logs, daemon=True).start()
#https://medium.com/@asvinjangid.kumar/creating-your-own-api-in-python-a-beginners-guide-59f4dd18d301
#Constraint: Efficient Storage and Retrieval/Concurrency
@app.route('/logs', methods=['GET'])
def get_logs():
    """GET /logs method, reads in arguments passed in either through the URL or cURL command, updates the values, filters them out based on start and end and returns a list of filtered out logs"""
    #remove_expired_logs()
    service_name = request.args.get('service_name')
    start_timestamp = request.args.get('start')
    end_timestamp = request.args.get('end')

    filtered_logs = []

    #Constraint: Memory Efficiency
    for log in logs:
        datetime_obj = datetime.strptime(log['timestamp'].replace("T"," ").replace("Z",""), '%Y-%m-%d %H:%M:%S')
        timestamp = datetime_obj.timestamp()

        start_timestamp_conversion = datetime.strptime(start_timestamp.replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S').timestamp()
        end_timestamp_conversion = datetime.strptime(end_timestamp.replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S').timestamp()

        if (not service_name or log['service_name'] == service_name) and (not start_timestamp_conversion or timestamp >= start_timestamp_conversion) and (not end_timestamp_conversion or timestamp <= end_timestamp_conversion):
            filtered_logs.append({
                "timestamp": log['timestamp'],
                "message": log['message']
            })


    print(logs)
    print(filtered_logs)
    return jsonify(filtered_logs)

@app.route('/logs', methods=['POST'])
def post_logs():
    """POST /logs method, takes in service_name, timestamp and message and returns it as a JSON object"""
    new_log = request.get_json()

    if not new_log:
        return jsonify({"error": "No JSON received"}), 400
    
    service_name = new_log.get('service_name', '?')
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    message = new_log.get('message', '?')

    log_entry = {
        "service_name": service_name,
        "timestamp": timestamp,
        "message": message
    }
    logs.append(log_entry)

    return jsonify({
        "service_name": service_name,
        "timestamp": timestamp,
        "message": message
    })


if __name__ == '__main__':
    app.run()
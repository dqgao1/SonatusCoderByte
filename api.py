from flask import Flask, jsonify, request
import subprocess
from datetime import datetime
import time
import threading

app = Flask(__name__)

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
            #print((log['timestamp'].replace("Z","").replace("T"," "))).timestamp()
            datetime_obj = datetime.strptime(log['timestamp'], '%Y-%m-%d %H:%M:%S')
            timestamp = datetime_obj.timestamp()
            #log_timestamp = float(log['timestamp'].replace(":","").replace("Z","").replace("T"," "))
            if current_time - timestamp < EXPIRATION:
                new_logs.append(log)
            else:
                print("Log expired")

        logs = new_logs
        time.sleep(60)
        

threading.Thread(target=remove_expired_logs, daemon=True).start()
#https://medium.com/@asvinjangid.kumar/creating-your-own-api-in-python-a-beginners-guide-59f4dd18d301
@app.route('/logs', methods=['GET'])
def get_logs():
    #remove_expired_logs()
    return jsonify({"logs": logs})

@app.route('/logs', methods=['POST'])
def post_logs():
    new_log = request.get_json()

    if not new_log:
        return jsonify({"error": "No JSON received"}), 400
    
    service_name = new_log.get('service_name', '?')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
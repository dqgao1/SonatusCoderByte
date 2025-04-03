
# SonatusCoderByte

Sonatus CoderByte Software Engineer Interview

---

## Prerequisites
1. Python 3.11.4
2. requests
	`pip install requests`
3. Flask
	`pip install flask`

## Architecture
### GET /logs
**Takes in the following parameters**
1. service_name
2. start
3. end
---
### GET cURL Command
`curl "http://127.0.0.1:5000/logs?service_name=auth-service&start=2025-04-03T18:33:00Z&end=2025-04-03T18:33:59Z"`
### POST /logs
**Takes in the following parameters**
1. service_name
2. timestamp
3. message
---
### POST cURL Command
1. `curl -X POST http://127.0.0.1:5000/logs -d '{"service_name": "auth-service", "timestamp":"2025-03-17T10:15:00Z","message":"User login successful"'`

2. `$headers = @{"Content-Type" = "application/json"}`
`>> $body = '{"service_name": "auth-service", "timestamp":"2025-04-03T19:21:00Z","message":"CURL TEST"}'     ` 
`>> `
`>> Invoke-RestMethod -Uri http://127.0.0.1:5000/logs -Method POST -Headers $headers -Body $body`
*Note: I used a windows machine so the POST cURL command did not work for me, even when using curl.exe so I instead used 2nd command to test*
## Running the code / Testing
1. Navigate to the directory where `api.py` and `DistributedLogAggregate.py` are located:
2. Start a new terminal in this directory and run the following to start the Flask server
	`python api.py`
	*(Make sure you are using Python 3, try `python3 api.py` if Python 2 and 3 are installed on the same machine)*
3. Enter arbitrary values into the started Flask service using the `POST` curl commands found in the **Architecture** section
4. Filter the logs by using the `GET` request found under the **Architecture** section by setting a start time and end time
*Note: I used the example directly and when adding a start/end time, please include the T and Z as described in the example problem*
*E.g. curl http://127.0.0.1:5000/logs?service_name=auth-service&start=2025-04-03T18:33:00Z&end=2025-04-03T18:40:59Z*
*The above will search for logs with the service_name auth-service and logs made between the times 6:33pm-6:40pm made on 04/03/2025*
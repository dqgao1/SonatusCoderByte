import logging
from datetime import datetime
import requests



#pip install requests
#pip install flask


logger = logging.getLogger(__name__)



def main():
    logging.basicConfig(filename='logging.log', level=logging.INFO)
    logging.info('Started')
    print("Hello World!")
    url = "http://127.0.0.1:5000/logs"
    payload = {"service_name": "auth-service",
               "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
               "message": "User login successful"
               }
    response = requests.post(url, json=payload)

    

if __name__ == '__main__':
    main()
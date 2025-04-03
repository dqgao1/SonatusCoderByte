import logging
import datetime


logger = logging.getLogger(__name__)



def main():
    logging.basicConfig(filename='logging.log', level=logging.INFO)
    logging.info('Started')
    print("Hello World!")

    

if __name__ == '__main__':
    main()
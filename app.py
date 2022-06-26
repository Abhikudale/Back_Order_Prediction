import sys
import housing
from flask import Flask
from housing.exception import HousingException
from housing.logger import logging 

app=Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    try:
        print("Let's test an application")
    except Exception as e:
        housing = HousingException(e,sys)
        logging.info(housing.error_message)
        logging.info("We are testing Logging module")
    return "CI CD Pipeline has been established and running now."

if __name__=="__main__":
    app.run(debug=True)


import json
from flask import Flask, jsonify, request
from ibm_botocore.client import Config, ClientError
import ibm_boto3
import os
import eml_parser
import json
import datetime
app = Flask(__name__)


@app.route('/domain-check', methods=['POST'])
def domain_check():
    try:
        data = request.json
        print('request', data)
        fromAddress = data['from'].split("@")[1]
        valueCheck = False
        
        if fromAddress in data['returnPath']: 
            valueCheck = True
        
        return {
            "headers": {
                "Content-Type": "application/json",
            },
            "statusCode": 200,
            "body": valueCheck,
        }
    except Exception as e:
        print(f"Failed to upload file 'object_name to bucket {str(e)}")


if __name__ == '__main__':
   app.run(port=3003)

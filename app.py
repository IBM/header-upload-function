import json
from flask import Flask, jsonify, request
from ibm_botocore.client import Config, ClientError
import ibm_boto3
import os
import eml_parser
import json
import datetime
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
app = Flask(__name__)

load_dotenv()

def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial


@app.route('/upload-file', methods=['POST'])
def upload_file():
    # credentials = {
    #     'IBM_API_KEY_ID': os.getenv("IBM_API_KEY_ID"),
    #     'IAM_SERVICE_ID': os.getenv("IAM_SERVICE_ID"),
    #     'ENDPOINT': os.getenv("ENDPOINT"),
    #     'BUCKET': os.getenv("BUCKET"),
    #     'AUTH_ENDPOINT' : os.getenv("AUTH_ENDPOINT"),
    #     'INSTANCE_CRN' : os.getenv("INSTANCE_CRN")
    # }
    file = request.files['fileObj']
    try:
        # cos_client = ibm_boto3.client("s3",
        #     ibm_api_key_id=credentials['IBM_API_KEY_ID'],
        #     ibm_service_instance_id=credentials['INSTANCE_CRN'],
        #     ibm_auth_endpoint=credentials['AUTH_ENDPOINT'],
        #     config=Config(signature_version="oauth"),
        #     endpoint_url=credentials['ENDPOINT']
        # )
        # cos_client.upload_fileobj(file, credentials['BUCKET'], file.filename)
        print('file', file)
        raw_email = file.read()
        print('raw_emailk', raw_email)
        ep = eml_parser.EmlParser()
        parsed_eml = ep.decode_email_bytes(raw_email)
        print(f"File 'object_name uploaded successfully to bucket.")
        parsed_json = json.dumps(parsed_eml, default=json_serial)      
        return {
            "headers": {
                "Content-Type": "application/json",
            },
            "statusCode": 200,
            "body": parsed_json,
        }
    except Exception as e:
        print(f"Failed to upload file 'object_name to bucket {str(e)}")

if __name__ == '__main__':
   app.run(port=3003)

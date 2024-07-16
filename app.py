import json
from flask import Flask, jsonify, request
from ibm_botocore.client import Config, ClientError
import ibm_boto3
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
app = Flask(__name__)

load_dotenv()

@app.route('/upload-file', methods=['POST'])
def upload_file():
    credentials = {
        'IBM_API_KEY_ID': os.getenv("IBM_API_KEY_ID"),
        'IAM_SERVICE_ID': os.getenv("IAM_SERVICE_ID"),
        'ENDPOINT': os.getenv("ENDPOINT"),
        'BUCKET': os.getenv("BUCKET"),
        'AUTH_ENDPOINT' : os.getenv("AUTH_ENDPOINT"),
        'INSTANCE_CRN' : os.getenv("INSTANCE_CRN")
    }
    file = request.files['fileObj']
    try:
        cos_client = ibm_boto3.client("s3",
            ibm_api_key_id=credentials['IBM_API_KEY_ID'],
            ibm_service_instance_id=credentials['INSTANCE_CRN'],
            ibm_auth_endpoint=credentials['AUTH_ENDPOINT'],
            config=Config(signature_version="oauth"),
            endpoint_url=credentials['ENDPOINT']
        )
        cos_client.upload_fileobj(file, credentials['BUCKET'], file.filename)
        print(f"File 'object_name uploaded successfully to bucket '{credentials['BUCKET']}'.")
    except Exception as e:
        print(f"Failed to upload file 'object_name to bucket '{credentials['BUCKET']}': {str(e)}")

    return '', 200, {"message": "Success"}

if __name__ == '__main__':
   app.run(port=3003)

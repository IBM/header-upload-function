import json
from flask import Flask, jsonify, request
from ibm_botocore.client import Config, ClientError
import ibm_boto3
app = Flask(__name__)


@app.route('/upload-file', methods=['POST'])
def upload_file():
    credentials = {
        'IBM_API_KEY_ID': 'Jo0EEG92SeoiEXQeIxJFRv0Eg4WOCFzsr_CcakDbaH9X',
        'IAM_SERVICE_ID': 'iam-ServiceId-a5824351-ee48-468b-9e12-1cf26321bb8d',
        'ENDPOINT': 'https://s3.us-south.cloud-object-storage.appdomain.cloud',
        'BUCKET': 'custom-bucket-watsonx-challenge',
        'AUTH_ENDPOINT' : 'https://iam.cloud.ibm.com/identity/token',
        'INSTANCE_CRN' : 'crn:v1:bluemix:public:cloud-object-storage:global:a/1d341fdce08c4011b670e9f4de4b401a:79cf80bb-1526-4d27-85d5-6ee25077ec58::'
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

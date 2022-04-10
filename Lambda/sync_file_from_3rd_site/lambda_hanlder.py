import json
import os
import boto3
import shutil
import requests
import mimetypes
from urllib.parse import urljoin

ENDPOINT = os.environ.get('endpoint', '')
S3_BUCKET = os.environ.get('s3_bucket', '')
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    
    print(event)
    
    file_uri = event['rawPath']
    # file exists in s3 bucket, 403 for fallback process
    if is_file_exist(file_uri):
        return {
            'statusCode': 403,
            'body': json.dumps('File exists, 403 to SIH for process')
        }
    else:
        result = sync_file_from_3rd_site(file_uri)
        if result == 'STATUS404':
            return {
                'statusCode': 404,
                'body': json.dumps('Target file does not exist')
            }
        # file sync success, 403 for fallback process
        else:
            return {
                'statusCode': 403,
                'body': json.dumps('File synced, 403 to SIH for process')
            }

def is_file_exist(file_uri):
    """
    check if file exists in S3
    """
    try:
        obj_key = file_uri[1:]
        response = s3_client.get_object(
            Bucket=S3_BUCKET,
            Key=obj_key,
        )
        return True
    except Exception as e:
        print(e)
        return False


def sync_file_from_3rd_site(file_uri):
    """
    download file to /tmp for further process
    """
    file_url = urljoin(ENDPOINT, file_uri)
    tmp_file_path = os.path.join('/tmp', os.path.basename(file_uri))
    res = requests.get(file_url, stream=True)
    # Check if the image was retrieved successfully
    if res.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        
        # Open a local file with wb ( write binary ) permission.
        with open(tmp_file_path,'wb') as f:
            res.raw.decode_content = True
            shutil.copyfileobj(res.raw, f)
        # Upload to S3
        obj_key = file_uri[1:]
        mimetype, _ = mimetypes.guess_type(tmp_file_path)

        ext_args = {"ContentType": mimetype}
        s3_client.upload_file(tmp_file_path, S3_BUCKET, obj_key, ExtraArgs = ext_args)
        return tmp_file_path
    else:
        print('Image Couldn\'t be retreived')
        return 'STATUS404'
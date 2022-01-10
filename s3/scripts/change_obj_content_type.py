import json
import boto3


def lambda_handler(event, context):

    obj_key = event["tasks"][0]["s3Key"]
    obj_ext = obj_key.split('.')[-1]
    bucket_arn = event["tasks"][0]["s3BucketArn"]
    bucket_name = bucket_arn.split(":")[-1]
    task_id = event["tasks"][0]["taskId"]

    s3_client = boto3.client("s3")

    s3_client.copy_object(
        Key=obj_key,
        Bucket=bucket_name,
        CopySource={"Bucket": bucket_name, "Key": obj_key},
        Metadata={"src": "dth"},
        MetadataDirective="REPLACE",
        ContentType=get_content_type(obj_ext),
    )

    return {
        "invocationSchemaVersion": "1.0",
        "treatMissingKeysAs": "PermanentFailure",
        "invocationId": "YXNkbGZqYWRmaiBhc2RmdW9hZHNmZGpmaGFzbGtkaGZza2RmaAo",
        "results": [
            {"taskId": task_id, "resultCode": "Succeeded", "resultString": "Great"}
        ],
    }


def get_content_type(ext):
    type_dict = {
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'jpeg': 'image/jpeg'
    }
    return type_dict.get(ext, 'binary/octet-stream')
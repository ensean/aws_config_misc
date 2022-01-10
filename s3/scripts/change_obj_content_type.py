import json
import boto3


def lambda_handler(event, context):

    obj_key = event["tasks"][0]["s3Key"]
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
        ContentType="image/png",
    )

    return {
        "invocationSchemaVersion": "1.0",
        "treatMissingKeysAs": "PermanentFailure",
        "invocationId": "YXNkbGZqYWRmaiBhc2RmdW9hZHNmZGpmaGFzbGtkaGZza2RmaAo",
        "results": [
            {"taskId": task_id, "resultCode": "Succeeded", "resultString": "Great"}
        ],
    }

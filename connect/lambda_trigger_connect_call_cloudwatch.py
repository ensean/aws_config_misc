import boto3
import logging
import os
import json
import botocore.session
from botocore.exceptions import ClientError

session = botocore.session.get_session()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    logger.setLevel(logging.DEBUG)
    # Getting the destination phone number from api gw.
    DestPhoneNumber = event["destPhoneNumber"]

    # Getting the Amazon Connect ContactFlowID passed in by the environment variables.
    ContactFlowId = os.environ["ContactFlowId"]

    # Getting the Amazon Connect InstanceId passed in by the environment variables.
    InstanceId = os.environ["InstanceId"]

    # Getting the Source Phone Number passed in by the environment variables. This phone number is your Amazon Connect phone number.
    SourcePhoneNumber = os.environ["SourcePhoneNumber"]

    # Getting alarm name from sns event, 
    # you can refer to sns_cloudwatch_lambda_event.json for sample event
    message_body = json.loads(event['Records'][0]['Sns']['Message'])
    cloudwatch_alarm_name = message_body['AlarmName']

    connectclient = boto3.client("connect")
    try:
        # Making the outbound phone call...
        OutboundResponse = connectclient.start_outbound_voice_contact(
            DestinationPhoneNumber=DestPhoneNumber,
            ContactFlowId=ContactFlowId,
            InstanceId=InstanceId,
            SourcePhoneNumber=SourcePhoneNumber,
            Attributes={
                "Message": "%s, 请留意处理" % cloudwatch_alarm_name
            },  # Attributes for contact flow's reference, if needed
        )
        logger.debug("outbound Call response is-- %s" % OutboundResponse)
    except ClientError as e:
        logger.error("An error occurred: %s" % e)

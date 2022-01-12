import boto3
import logging
import os
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

    connectclient = boto3.client("connect")
    try:
        # Making the outbound phone call...
        OutboundResponse = connectclient.start_outbound_voice_contact(
            DestinationPhoneNumber=DestPhoneNumber,
            ContactFlowId=ContactFlowId,
            InstanceId=InstanceId,
            SourcePhoneNumber=SourcePhoneNumber,
            Attributes={
                "Message": "This is a critical alert message!"
            },  # Attributes for contact flow's reference, if needed
        )
        logger.debug("outbound Call response is-- %s" % OutboundResponse)
    except ClientError as e:
        logger.error("An error occurred: %s" % e)

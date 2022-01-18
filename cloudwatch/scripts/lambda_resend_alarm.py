import os
import boto3
import json
import logging
from datetime import datetime

cw_client = boto3.client('cloudwatch')
sns_client =boto3.client('sns')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# get alarm list from env var
target_alarm_list = os.environ.get('target_alarm_list', '').strip()
sns_topic_arn = os.environ.get('sns_topic_arn', '').strip()

# format datetime
def default_seira(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S %Z')
    else:
        return str(obj)

def lambda_handler(event, context):

    if target_alarm_list == '' or sns_topic_arn == '':
        return {
            'statusCode': 500,
            'body': json.dumps({'msg': 'sns_topic or target_alarm_list is not set in env'})
        }
    targets = target_alarm_list.split(',')
    for t in targets:
        alarm_info = get_alarm(t)
        process_alarm(alarm_info)

def get_alarm(alarm_name):
    info = cw_client.describe_alarms(
        AlarmNames = [alarm_name]
    )
    return info['MetricAlarms'][0]

def process_alarm(alarm):
    # is the alarm in ALARM state ?
    state = alarm['StateValue']
    if state == 'ALARM':
        # 推送告警内容到sns主题，也可根据需要自行实现通知逻辑
        logger.info('%s re triggered' % alarm['AlarmName'])
        send_alarm_to_sns(alarm)

def send_alarm_to_sns(alarm):
    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=json.dumps(alarm, indent=4, default=default_seira, ensure_ascii=False)
    )

def main():
    info = get_alarm('rds cpu high超过20%')
    print(json.dumps(info, indent=4, default=default_seira,ensure_ascii=False))

if __name__ == '__main__':
    main()
### 只能在特定区域操作EC2，但不能终止、停止EC2

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "ec2:*",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "ec2:Region": [
                        "ap-east-1",
                        "ap-northeast-1"
                    ]
                }
            }
        },
        {
            "Sid": "CloudWatch",
            "Effect": "Allow",
            "Action": "cloudwatch:*",
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Deny",
            "Action": [
                "ec2:RebootInstances",
                "ec2:DeleteVolume",
                "ec2:TerminateInstances",
                "ec2:DeleteNatGateway",
                "ec2:DeleteInternetGateway",
                "ec2:StopInstances"
            ],
            "Resource": "*"
        }
    ]
}
```
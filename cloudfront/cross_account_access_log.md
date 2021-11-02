### 配置Cloudfront存储访问日志到另外一个AWS账号的S3桶

#### 前提假设

* 账号A: CloudFront分发所在账号
* 账号B: 日志存放专用账号
* 账号B存放CloudFront访问日志S3桶：cloudfront_access_logs


#### 配置

* 账号B S3桶策略配置

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "CloudFrontAccessLog",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::<A-account-id>:root"
            },
            "Action": [
                "s3:PutBucketAcl",
                "s3:GetBucketAcl"
            ],
            "Resource": "arn:aws:s3:::cloudfront_access_logs"
        }
    ]
}
```


* 账号A

CloudFront访问日志S3桶手动输入`cloudfront_access_logs.s3.amazonaws.com`，并根据需要配置前缀。
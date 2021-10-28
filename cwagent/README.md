### Cloudwatch agent 监控磁盘使用量

1. 给EC2配置角色，包含如下策略
    * CloudWatchAgentServerPolicy
    * AmazonSSMManagedInstanceCore

1. 安装cloudwatch agent 
    ```shell
    sudo yum install amazon-cloudwatch-agent    # amazon linux2，其余os请参考https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/install-CloudWatch-Agent-commandline-fleet.html

    ```

2. 生成Cloudwatch agent配置文件，也可直接使用`config.json`
    ```shell
    sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
    ```

3. 启动Cloudwatch agent，其中`configuration-file-path`为上一步`config.json`绝对路径
    ```shell
    sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:configuration-file-path
    ```
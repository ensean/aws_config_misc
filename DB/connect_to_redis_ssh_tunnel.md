### 通过SSH tunnel访问elasticache redis

`此操作可能会使redis暴露于公网，请谨慎使用`

1. 启动EC2，确保该EC2能够访问目标elasticache redis

2. 将步骤1 EC2的ssh登录秘钥上传至该EC2的~/.ssh/目录，命名为id_rsa，权限配置为400

3. 登录到步骤1 EC2，执行如下命令建立SSH Tunnel转发

```
sudo yum install tmux -y
tmux
ssh -L 6000:redisxxxxxx.12xxxx.clustercfg.apne1.cache.amazonaws.com:6379 -g 127.0.0.1
```
相关说明：
* 6000: EC2映射端口
* redisxxxxxx.12xxxx.clustercfg.apne1.cache.amazonaws.com：Redis访问endpoint, 具体参考[这里](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/Endpoints.html)

4. 配置EC2安全组，允许映射的端口，应用程序通过EC2映射端口访问Redis

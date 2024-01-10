

## 使用 stunnel 以非 tls 方式访问开启了 tls 的集群

* 参考链接 https://docs.aws.amazon.com/zh_cn/AmazonElastiCache/latest/red-ug/connect-tls.html

* 参考配置

```shell
fips = no
setuid = root
setgid = root
pid = /var/run/stunnel.pid
debug = 7 
delay = yes
options = NO_SSLv2
options = NO_SSLv3
[redis-cli]
   client = yes
   accept = 0.0.0.0:6379
   connect = master.xxxxxx.sbc6gu.apne1.cache.amazonaws.com:6379
```

* 使用方式

通过 EC2 公网 IP、6379 端口（留意更新安全组配置）连接到 Elasticache Redis

## 使用 nginx stream 转发，以 tls 方式访问开启了 tls 的 redis 集群

* 参考配置

```shell
stream {
      server {
          listen 9000;
          proxy_pass app_server;
      }
      upstream app_server{
          server master.xxxxxx.sbc6gu.apne1.cache.amazonaws.com:6379;
      }
}
```

* 使用方式
通过 EC2 公网IP、9000 端口（留意更新安全组配置）tls 方式连接到 Elasticache Redis


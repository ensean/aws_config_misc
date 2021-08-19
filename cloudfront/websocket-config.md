### 配置Cloudfront以支持websocket

#### 配置说明

1. 创建自定义Origin request policy（源请求策略），包含如下Header

  * Sec-WebSocket-Key
  * Sec-WebSocket-Version
  * Sec-WebSocket-Protocol
  * Sec-WebSocket-Accept

2. 配置Behavior（行为）使用步骤1配置的源请求策略

#### 参考资料
1. [Using WebSocket with CloudFront Distributions](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-working-with.websockets.html)
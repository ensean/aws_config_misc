### 背景

Lambda限制返回playload最高6M，但由于图片返回时会有base64编码引入放大系数（约1.33）从而会导致SIH方案支持的图片最大在4.5MB左右，超过此大小会导致413错误。

### 临时解决方案

#### 原理说明
Cloudfront配置备用源直达S3桶，通过Lambda@Edge将造成413的访问请求设置为301，使浏览器通过备用域名访问原图

#### 配置方式

* Lambda@Edge 绑定事件：源响应
* 代码：[LE_SIH](./scripts/LE_SIH.js)

### 后续解决方案

1）使用Graviton2图片剪裁方案
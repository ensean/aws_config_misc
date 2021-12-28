### 通过zip包方式引入PHP SDK示例

* 上传文件至S3操作步骤
1. 操作系统依赖安装
    * php-mbstring
    * php-xml

2. 创建IAM用户并配置对应的S3桶权限，生成AK、SK备用

3. 执行如下命令查看上传是否成功, 其中`sfadfghgkfjkl789456897083r`为s3桶名，`/tmp/aws.zip`为本地文件名

```
php pubObj.php sfadfghgkfjkl789456897083r /tmp/aws.zip
```

4. 进入S3桶确认文件上传是否成功


* 参考资料

1. https://docs.aws.amazon.com/sdk-for-php/v3/developer-guide/getting-started_installation.html#installing-by-using-the-zip-file
1. 权限配置 https://docs.aws.amazon.com/sdk-for-php/v3/developer-guide/guide_credentials_hardcoded.html
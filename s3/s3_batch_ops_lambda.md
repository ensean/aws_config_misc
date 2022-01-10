### 借助S3 batch job修改s3文件content-type

1. 将需要修改的文件以如下格式录入到csv文件，并将csv文件上传至S3备用
```
test345643-media,imgs/Tom-And-Jerry.jpg
test345643-media,imgs/nginx-access.png
test345643-media,imgs/wh5mb.jpg
```

2. 创建Lambda函数，留意权限配置

3. 创建S3批量作业

4. 确认执行S3批量作业
<?php
// aws.zip 文件解压路径为/usr/share/nginx/html/sdk/
// 本文件路径为 /usr/share/nginx/html/putObj.php
require '/usr/share/nginx/html/sdk/aws-autoloader.php';

use Aws\S3\S3Client;
use Aws\Exception\AwsException;
// Hard-coded credentials
$s3Client = new S3Client([
    'version'     => 'latest',
    'region'      => 'ap-northeast-1',  // 匹配桶所在区域
    // 'use_accelerate_endpoint' => true,  // 使用S3传输加速功能，需要先在S3界面开启
    'credentials' => [
        'key'    => 'ak',   // 后台用户ak，该用户需要有S3桶访问权限
        'secret' => 'sk',   // 后台用户sk
    ],
]);
// snippet-start:[s3.php.put_object.main]
$USAGE = "\n" .
    "To run this example, supply the name of an S3 bucket and a file to\n" .
    "upload to it.\n" .
    "\n" .
    "Ex: php PutObject.php <bucketname> <filename>\n";

if (count($argv) <= 2) {
    echo $USAGE;
    exit();
}

$bucket = $argv[1];
$file_Path = $argv[2];
$key = basename($argv[2]);

try {
    //Create a S3Client
    $result = $s3Client->putObject([
        'Bucket' => $bucket,    // 桶名称
        'Key' => $key,
        'SourceFile' => $file_Path, // 本地文件路径
    ]);
} catch (S3Exception $e) {
    echo $e->getMessage() . "\n";
}
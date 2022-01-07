#!/bin/bash
cd $(dirname $0)
cd ..
BASE_DIR=$(pwd)

SERVER_NAME='business_job.py'

#兼容部分服务器 找不到环境变量
source /etc/profile

#兼容部分服务器 找不到环境变量
export PYTHONPATH=$BASE_DIR:$PYTHONPATH

nohup python3 $SERVER_NAME > business_job.out 2>&1 &

echo "$SERVER_NAME is starting!"
cd $(dirname $0)
cd ..
export BASE_DIR=$(pwd)

SERVER_NAME='business_job.py'

#兼容部分服务器 找不到环境变量
source /etc/profile

nohup python3 $SERVER_NAME > /dev/null 2>&1 &

echo "$SERVER_NAME is starting!"
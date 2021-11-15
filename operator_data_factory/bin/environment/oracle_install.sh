#!/bin/bash

cd $(dirname $0)
cd ../..
export BASE_DIR=$(pwd)

## oracle连接环境安装
mkdir -p /opt/oracle
cd /opt/oracle

# 获取oracle client安装包并解包
#wget https://download.oracle.com/otn_software/linux/instantclient/1911000/instantclient-basic-linux.x64-19.11.0.0.0dbru.zip
unzip  $BASE_DIR/resource/instantclient-basic-linux.x64-19.11.0.0.0dbru.zip

# 安装oracle client 所需包
sudo yum install libaio

# 建立连接
sudo sh -c "echo /opt/oracle/instantclient_19_11 > /etc/ld.so.conf.d/oracle-instantclient.conf"
sudo ldconfig

# 设置环境变量
export LD_LIBRARY_PATH=/opt/oracle/instantclient_19_11:$LD_LIBRARY_PATH

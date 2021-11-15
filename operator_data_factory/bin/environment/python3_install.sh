#!/bin/bash

cd $(dirname $0)
cd ../..
export BASE_DIR=$(pwd)

## python3环境安装

# 创建python3文件夹并打开
mkdir -p /opt/python3
cd /opt/python3

# 获取python3.7的安装包并解包
#wget https://www.python.org/ftp/python/3.7.1/Python-3.7.1.tgz
tar -xzvf  $BASE_DIR/resource/Python-3.7.1.tgz

# 安装编译工具及库
cd Python-3.7.1
#yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel gcc* glien*
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel

# 运行脚本config
./configure --prefix=/usr/local/python3.7

# 编译并安装
make
make install

# 创建软连接路径
ln -s /usr/local/python3.7/bin/python3.7 /bin/python3
ln -s /usr/local/python3.7/bin/pip3.7 /bin/pip3

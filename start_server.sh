#!/bin/bash

confpath="./server_config.json"
if [ "$1"] ; then
    confpath=$1
fi

find_pid='ps -aux | grep -E "python.*main.py $confpath" | grep -v grep'

count=`eval "$find_pid|wc -l"`
if [ $count -ne 0 ] ; then
        echo "进程已存在"
        exit 1
fi

App="python3"
`nohup $App ./server/code/main.py $confpath 1>/dev/null 2>>error.log &`
sleep 3
count=`eval "$find_pid|wc -l"`
if [ $count -ne 0 ] ; then
        echo "进程启动成功"
        exit 1
fi








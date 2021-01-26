#!/bin/bash

confpath="./server_config.json"
if [ "$1"] ; then
    confpath=$1
fi

find_pid='ps -aux | grep -E "python.*main.py $confpath" | grep -v grep'

count=`eval "$find_pid|wc -l"`
if [ $count -eq 0 ] ; then
	echo "没有相关进程"
	exit 1
fi

if [ $count -ne 1 ] ; then
	echo "匹配进程数 >  1"
	exit 1
fi

pid=`eval $find_pid| awk '{print $2}'`
echo $pid > stop_server
echo "正在关闭，请等待"
sleep 5
pid2=`eval $find_pid| awk '{print $2}'`
echo $pid
echo $pid2
if [  "$pid2" == ""  ] ; then
	echo "关闭成功"
	exit 0
fi
echo "进程关闭失败，强制杀掉进程"

`kill -9 $pid2`

sleep 2

pid2=`eval $find_pid| awk '{print $2}'`
echo $pid2
if [ "$pid2" == "" ] ; then
        echo "关闭成功"
        exit 0
fi
echo "杀掉进程失败，关闭失败"



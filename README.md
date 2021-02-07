# 简介
爬取天天基金的基金并将其存入数据库，每天指定时间爬取，再对比数据后已邮件方式发送。
- server: 爬取数据并运行定时任务发送邮件
- client: 使用pyqt5制作的界面，用于连上数据库，查看爬取的信息（未完成）

## 运行环境
1. python3.7
2. mongodb

## 依赖库
1. demjson
2. lxml
3. pymongo
4. requests
5. pyqt5(客户端用的库，不需要安装)


## 启动
1. 服务器
    1. 启动 sh start_server.sh
    2. 关闭 sh stop_server.sh

## 配置

- 服务器配置 server_config.json
```
{
    "db": { //数据库连接
        "addr": "Ip地址", 
        "port": "端口", 
        "user": "用户", 
        "password": "密码"
    },
    "mail":{
        "user":"邮箱用户",
        "password":"密码或者授权码",
        "host":"smtp.163.com",
        "to":["接收邮箱地址1","接收邮箱地址2"],
    },
    "log":"./log.log", 
    "abort":"stop_server", //当运行目录下有该文件则会停止服务器
    "fund_list":[ //关注基金
        "260108",
        "003095",
        "270002",
        "090010",
        "001595",
        "160222",
        "519688",
        "161005"
    ]
}


```

- 客户端配置 client_config.json
```
待补充
```




项目基于python [fastAPI](https://fastapi.tiangolo.com/zh/)构建, 以[ChatGLM3](https://github.com/THUDM/ChatGLM3)微调大模型为主要交互数据源
实现用户注册、登录等日常功能,


## 项目结构
```
  |-src
    |- __init__     模块声明文件, 为空
    |- controller   路由
    |- database     数据库基础设置
    |- models       数据库表
    |- schemas      DTO
    |- middleware   中间件
    |- exceptions   异常处理
    |- service_auth 权限服务
    |- service_user 用户服务
  .env              环境变量, 用于设置全局配置变量
  .env.example      环境变量示例
  .gitignore        git忽略文件
  main              程序主入口
  README.md         项目文档
  requirements.txt  项目依赖
  sql_app.db        数据库文件
```



## 依赖安装

初始开发使用Python版本为:3.11.2

```
  安装插件(vscode)
  SQLite, SQLite3 Editor
```

```
  安装依赖, 下载速度若过慢请设置pip代理
  > pip install -r requirements.txt
```

```
  设置私钥:
  最外层目录中创建.env文件, 在.env文件下设置token私钥
```



## 项目启动

```
  启动项目
  > cd [项目]
  > uvicorn src.main:app --reload --port 3000 或 python main.py
```

```
  查看wagger接口定义文档
  URL: http://127.0.0.1:8000/docs
```

## 其它

个人学习可另外打开一个数据库, 备份当前项目
备份并复制当前项目, 项目中导入已有数据库或另建数据库, 自己用于学习
  (vscode sqlite创建数据库)vscode中 ctrl + shift + p, 输入sqlite, 选择Open Database

tip: 默认处理无效时, fastAPI默认报422错误码


## 更新记录
v1.0.0
- 2024/03/11, 项目初始化

# LLM-Back

项目后端核心基于[FastAPI]("https://fastapi.tiangolo.com/zh/")构建, 大模型部分基于[ChatGLM3](https://github.com/THUDM/ChatGLM3)以及[LLaMA-Factory]("https://github.com/hiyouga/LLaMA-Factory")构建而成

- 用户登录与注册注册、Token验证
- 可拓展的服务端用户历史记录存储
- 流式Completion Dialogue
- 模型Automatic Finetune
- 数据Automatic Crawl
- 微调模型的Automatic Deploy




## 目录结构
```
|-
  |- data			采集到的json数据与微调用的json map
  |- output			微调后导出的模型
  |-src
  	|- api
		__init__
		api_server 基于GLM3的API服务
		utils	辅助功能

  	|- base
	        __init__     模块声明文件, 为空
	        controller   基础功能路由
	        database     数据库基础设置
	        models       数据库表
	        schemas      DTO
	        middleware   中间件
	        exceptions   异常处理
	        service_auth 权限服务
	        service_user 用户服务

	|- crawl
	    	crawler		爬虫核心实现
	    	driver		selenium驱动
	    	main		爬虫入口文件
	    	utils		辅助功能

	|- finetune
		...		LLaMA-Factory微调文件
  .env              环境变量, 用于设置全局配置变量
  .env.example      环境变量示例
  .gitignore        git忽略文件
  crawl.log			crawl采集日志
  main.py           程序主入口
  pid.txt			用于一键自动化部署的python runtime pid
  README.md         说明文档
  reboot.sh			用于一键自动化部署的shell脚本
  requirements.txt  项目依赖
  run_crwal.py		crawl路由
  run_deploy.py		deploy路由
  run_export_model.py 模型导出路由
  run_export		模型导出入口
  run_finetune.py	模型微调路由
  run_train.py		模型微调入口
  sql_app.db        数据库文件
  sql_app.db		sql文件(默认)
```

## 项目启动

### 端口转发

服务器的127.0.0.1:3000转发至本地的127.0.0.1:3000，提供给配套前端使用

### 环境切换

切换至后端统一环境
```
conda activate llm_env
```

切换至后端项目根目录下
```
cd ~/travelAssistant/emLLM-back
```

### 依赖安装

初始开发使用Python版本为:3.11.2

```
  安装插件(vscode)
  SQLite, SQLite3 Editor 
  
  通过SQLite插件初始化生成.db文件（若需要） 
  (vscode sqlite创建数据库)vscode中 ctrl + shift + p, 输入sqlite, 选择Open Database
```

```
  安装依赖, 下载速度若过慢请设置pip代理
  pip install -r requirements.txt
```

```
  配置env:
  	1. 将.env.example复制并重命名为.env
  	2. 配置.env私钥、环境、模型路径、文件根路径等
```



### 启动

* 确认env配置无误：PORT无占用、MODE正确等

```
  在项目的根目录下(~/travelAssistant/emLLM-back)， 运行后等待加载，时间可能较长
  python main.py
```

能打开swagger文档，则项目启动完毕：

```
查看swagger后端接口文档
  URL: http://127.0.0.1:8000/docs 
  （端口设置为xx就是xx/docs，比如端口在8000即8000/docs）
```



## 其它

个人学习可另外打开一个数据库, 备份当前项目
备份并复制当前项目, 项目中导入已有数据库或另建数据库, 自己用于学习

tip: 默认处理无效时, fastAPI默认报422错误码

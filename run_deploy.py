import os

from fastapi import APIRouter
from src.base.schemas import Deploy, DeployAuto
from dotenv import get_key, set_key
from time import sleep
from sys import executable, argv
from subprocess import call
from os import system, _exit
from run_crawl import crawl


deploy_route = APIRouter(prefix="/llm")


@deploy_route.post("/deploy")
def deploy(config: Deploy):
    name = config.name
    if not name:
        return {"code": 400, "status": "error", "data": {}, "message": "Error: 传入模型名称错误"}
    env_path = "./.env"
    set_key(env_path, "MODEL_PATH", f"./export/{name}")
    system("ps aux | grep 'python' | awk '{print $1}' >> pid.txt")
    # source在windows下不起作用
    system("source reboot.sh")

# @deploy_route("/deploy/auto")
# def deploy_auto(config: DeployAuto):
#     # 爬取配置
#     city = config.city
#     amount = config.amount

#     # 微调配置
#     finetune_data = None
#     if config.is_multi == True:
#       finetune_data = city + "_more.json"
#     else:
#       finetune_data = city + ".json"
#     max_samples = config.max_samples

#     # 导出配置
#     export_name = config.dir_name

#     # 部署配置
#     deploy_name = export_name

#     crawl()

import os

from fastapi import APIRouter
from src.base.schemas import Deploy
from dotenv import get_key, set_key
from time import sleep
from sys import executable, argv
from subprocess import call
from os import system, _exit
import pyautogui


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
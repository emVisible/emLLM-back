import os
from fastapi import APIRouter
from src.base.schemas import ExportModel
from json import dumps, load

export_route = APIRouter(prefix="/llm")


@export_route.get("/model")
async def get_models():
    models = os.listdir("./export")
    return {
        "code": 200,
        "status": "success",
        "data": {"names": models},
        "message": "获取模型成功",
    }


@export_route.post("/export")
async def export_model(dir_config: ExportModel):
    dir_name = dir_config.dir_name
    dir_path = f"./export/{dir_name}"
    if not os.path.exists(os.path.abspath(dir_path)):
        os.mkdir(dir_path)
    model_name = "C:/_code/store/chatglm3-6b"
    model_path = "./output/test"
    export_dir = dir_path
    command = f"""
    python ./run_export.py \
    --model_name_or_path {model_name} \
    --adapter_name_or_path {model_path} \
    --template chatglm3 \
    --finetuning_type lora \
    --export_dir {export_dir} \
    --export_size 2 \
    --export_legacy_format False
    """
    os.system(command)
    return {"code": 200, "status": "success", "data": {}, "message": "模型导出完毕"}
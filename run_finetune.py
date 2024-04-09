import os
from fastapi import APIRouter
from src.base.schemas import FinetuneConig

finetune_route = APIRouter(prefix="/llm")
@finetune_route.post("/finetune", tags=["LLM"])
async def fine_tune(finetune_config:FinetuneConig):
    data_path = finetune_config.data_path
    max_samples = finetune_config.max_samples
    if max_samples <= 0 or max_samples > 1000:
      return {"code": 400, "status": "error", "data": {}, "message": "Error: max samples设置错误"}
    if  len(data_path) == 0:
      return {"code": 400, "status": "error", "data": {}, "message": "Error: 微调数据文件名错误"}
    # 定义微调命令
    base_dir = "./"
    model_path = "C:/_code/store/chatglm3-6b"
    data_name = data_path
    max_samples = max_samples or 1000
    command = f"""
    python {base_dir}run_train.py \
    --model_name_or_path {model_path or 'C:/_code/store/chatglm3-6b'} \
    --stage sft \
    --do_train True \
    --finetuning_type lora \
    --template chatglm3 \
    --dataset_dir {base_dir}data \
    --dataset {data_name} \
    --cutoff_len 1024 \
    --learning_rate 5e-05 \
    --num_train_epochs 3.0 \
    --max_samples {max_samples or '1000'} \
    --per_device_train_batch_size 4 \
    --gradient_accumulation_steps 4 \
    --lr_scheduler_type cosine \
    --max_grad_norm 1.0 \
    --logging_steps 5 \
    --save_steps 100 \
    --warmup_steps 0 \
    --lora_rank 8 \
    --lora_dropout 0.1 \
    --lora_target query_key_value \
    --output_dir {base_dir}output \
    --overwrite_output_dir True \
    --plot_loss True \
    """
    # 执行命令
    os.system(command)
    return {"code": 200, "status": "success", "data": {}, "message": "微调完毕"}


# fine_tune()

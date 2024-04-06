import os
from fastapi import APIRouter

finetune_route = APIRouter(prefix="/llm")


@finetune_route.post("/finetune", tags=["LLM"])
async def fine_tune():
    # 定义微调命令
    base_dir = "./"
    model_path = "C:/_code/store/chatglm3-6b"
    data_name = "finetune_data"
    max_samples = 1000
    command = f"""
    python {base_dir}/run_train.py \
    --model_name_or_path {model_path or 'C:/_code/store/chatglm3-6b'} \
    --stage sft \
    --do_train True \
    --finetuning_type lora \
    --template chatglm3 \
    --dataset_dir {base_dir}/data/finetune \
    --dataset {data_name or 'finetune_data'} \
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
    --output_dir {base_dir}/output \
    --overwrite_output_dir True \
    --plot_loss True \
    """
    # 执行命令
    os.system(command)


# fine_tune()

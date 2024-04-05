python3.9 qlora.py \
    --model_name_or_path NousResearch/Llama-2-7b-hf \
    --output_dir ./output/phi-1_5-marunachef-v1 \
    --logging_steps 1 \
    --save_strategy steps \
    --data_seed 42 \
    --save_steps 235 \
    --save_total_limit 10 \
    --report_to wandb \
    --evaluation_strategy steps \
    --eval_dataset_size 100 \
    --max_eval_samples 100 \
    --per_device_eval_batch_size 1 \
    --max_new_tokens 256 \
    --dataloader_num_workers 1 \
    --group_by_length \
    --logging_strategy steps \
    --remove_unused_columns False \
    --do_train \
    --do_eval \
    --lora_r 64 \
    --lora_alpha 16 \
    --lora_modules all \
    --double_quant \
    --quant_type nf4 \
    --bf16 \
    --bits 4 \
    --warmup_ratio 0.03 \
    --lr_scheduler_type constant \
    --gradient_checkpointing \
    --dataset ../../data/recipe/02_oasst/train_v6.jsonl \
    --dataset_format oasst1 \
    --run_name phi-1_5-marunachef-v1 \
    --source_max_len 0 \
    --target_max_len 3800 \
    --per_device_train_batch_size 4 \
    --gradient_accumulation_steps 4 \
    --max_steps 2350 \
    --eval_steps 100 \
    --learning_rate 0.0002 \
    --adam_beta2 0.999 \
    --max_grad_norm 0.3 \
    --lora_dropout 0.1 \
    --weight_decay 0.0 \
    --seed 0 \

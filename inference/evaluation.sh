#!/bin/bash
#SBATCH -c 1  # Number of Cores per Task
#SBATCH --mem=30G  # Requested Memory
#SBATCH -p hgx-alpha  # Partition
#SBATCH -t 168:00:00  # Wall Time
#SBATCH -G 1  # Number of GPUs
#SBATCH -o eval-%j.out  # %j = job ID
#SBATCH -e eval-%j.err  # %j = job ID
#SBATCH --mail-type=ALL  
eval "$(conda shell.bash hook)"
conda activate vllm
export HF_HOME=/project/pi_hzamani_umass_edu/ppromthaw/recipe-inferences/cache
python -c "from huggingface_hub.hf_api import HfFolder; HfFolder.save_token('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')"
python extract_evaluation.py \
  --model kimmypracha/llama-marunashop-v2-a100-2115 \
  --eval_file ecommerce/marunashop-v2-llama.jsonl \
  --output_file results/marunashop-llama.llama-slot-metrics.jsonl

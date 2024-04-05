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
export HF_HOME=/work/pi_hzamani_umass_edu/ppromthaw/cache
python -c "from huggingface_hub.hf_api import HfFolder; HfFolder.save_token('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')"
python evaluation_script.py \
  --model kimmypracha/mistral-marunashop-v3-0.2 \
  --eval_file ../../data/ecommerce/03_inference_pair/mistral-marunashop-v3-all-0.2.jsonl \
  --output_dir ../../reports/mistral-marunashop-v3-all/20/ \
  --domain ecommerce
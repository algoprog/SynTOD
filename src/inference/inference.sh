#!/bin/bash
#SBATCH -c 1  # Number of Cores per Task
#SBATCH --mem=30G  # Requested Memory
#SBATCH -p hgx-alpha  # Partition
#SBATCH -t 168:00:00  # Wall Time
#SBATCH -G 1  # Number of GPUs
#SBATCH -o slurm-inference-a100-%j.out  # %j = job ID
#SBATCH -e slurm-inference-a100-%j.err  # %j = job ID
#SBATCH --mail-type=ALL  
eval "$(conda shell.bash hook)"
conda activate vllm
export HF_HOME=/project/pi_hzamani_umass_edu/ppromthaw/recipe-inferences/cache
python -c "from huggingface_hub.hf_api import HfFolder; HfFolder.save_token('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')"
python inference_script.py \
  --model kimmypracha/llama-marunachef-v3-0.05 \
  --output_file ../../data/recipe/03_inference_pair/marunachef-v3-gemini-0.05.jsonl \
  --test_file ../../data/recipe/02_oasst/test_gemini_v3.jsonl
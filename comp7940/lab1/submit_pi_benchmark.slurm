#!/bin/bash
#SBATCH --job-name=pi_mpi
#SBATCH --partition=debug
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --time=00:30:00
#SBATCH --output=pi_mpi_%j.out
#SBATCH --error=pi_mpi_%j.err

echo "Job started on $(date)"
echo "Running on node: $(hostname)"
echo "Job ID: $SLURM_JOB_ID"

# 激活conda环境
source ~/anaconda3/etc/profile.d/conda.sh
conda activate recsys-py310

# 检查环境是否激活成功
echo "Active conda environment: $CONDA_DEFAULT_ENV"
python --version

cd /home/comp/cswjyu/lab1

# 运行你的脚本
bash run_prallel.sh

echo "Job completed on $(date)"
#sbatch submit_pi_benchmark.slurm
#!/bin/bash

# 设置变量
dataset="dtd"
seed=1
txt_file="image_paths/${dataset}-train-16shots-seed=${seed}.txt"
target_dir="selected_fewshots/${dataset}/seed_${seed}"

# 创建目标文件夹
mkdir -p "$target_dir"

# 读取 TXT 文件并移动图片
while IFS= read -r line
do
  # 获取类名
  class_name=$(basename "$(dirname "$line")")
  # 创建类名文件夹
  mkdir -p "${target_dir}/${class_name}"
  # 移动图片
  cp "$line" "${target_dir}/${class_name}/"
done < "$txt_file"

echo "图片已成功移动到 ${target_dir}"


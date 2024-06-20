import os
from pathlib import Path

# 目录路径
data_dir = Path('/shared-network/yliu/projects/disef/fine-tune/data/tinyimagenet')
classes = [
    "n01443537", "n01629819", "n01641577", "n01644900", "n01698640", "n01742172", "n01768244",
    "n01770393", "n01774384", "n01774750", "n01784675", "n01855672", "n01882714", "n01910747",
    "n01917289", "n01944390", "n01945685", "n01950731", "n01983481", "n01984695", "n02002724", "n02056570",
    "n02058221", "n02074367", "n02085620"
]

# 文件路径初始化
image_id_path = '/home/yliu/projects/DataDream-ECCV2024-private/classify/metadata/tinyimagenet/val/image_ids.txt'
image_label_path = '/home/yliu/projects/DataDream-ECCV2024-private/classify/metadata/tinyimagenet/val/class_labels.txt'

# Ensure directory exists before writing to file
os.makedirs(os.path.dirname(image_id_path), exist_ok=True)
os.makedirs(os.path.dirname(image_label_path), exist_ok=True)

image_id_file = open(image_id_path, 'w')
image_label_file = open(image_label_path, 'w')

# 遍历每个类的目录
val_dir = data_dir / 'val'  # 直接指定验证目录路径
annotations_path = val_dir / 'val_annotations.txt'

with open(annotations_path) as f:
    for line in f:
        parts = line.strip().split('\t')
        image_name = parts[0]
        label = parts[1]
        if label in classes:
            # 写入 image_ids.txt
            image_id_file.write(f'val/images/{image_name}\n')
            # 写入 class_labels.txt，这里使用classes.index(label)来获取索引
            image_label_file.write(f'val/images/{image_name},{classes.index(label)}\n')

# 关闭文件
image_id_file.close()
image_label_file.close()



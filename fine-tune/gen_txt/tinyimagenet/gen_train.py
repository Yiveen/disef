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
image_id_path = '/home/yliu/projects/DataDream-ECCV2024-private/classify/metadata/tinyimagenet/train/image_ids.txt'
image_label_path = '/home/yliu/projects/DataDream-ECCV2024-private/classify/metadata/tinyimagenet/train/class_labels.txt'
image_id_file = open(image_id_path, 'w')
image_label_file = open(image_label_path, 'w')

# 遍历每个类的目录
train_dir = data_dir / 'train'  # 直接指定train目录路径
for obj_class in os.listdir(train_dir):
    if obj_class in classes:
        print('in!!')
        class_dir = train_dir / obj_class / 'images'
        for image_path in class_dir.iterdir():
            print(image_path)
            if image_path.is_file() and image_path.suffix == '.JPEG':  # 确保处理的是JPEG文件
                # 写入 image_ids.txt
                image_id_file.write(f'train/{obj_class}/{image_path.name}\n')
                # 写入 class_labels.txt
                image_label_file.write(f'train/{obj_class}/{image_path.name},{classes.index(obj_class)}\n')

# 关闭文件
image_id_file.close()
image_label_file.close()


from pathlib import Path
from typing import Optional

import pandas as pd
from src.data._base import BaseDataModule
from src.data.components.datasets import ClassificationDataset, SyntheticDataset


class TinyImageNet(BaseDataModule):
    """LightningDataModule for Tiny ImageNet dataset.

    Statistics:
        - 100000 samples.
        - 200 classes.
        - 500 samples per class

    Reference:
        - Russakovsky et al. ImageNet Large Scale Visual Recognition Challenge. IJCV 2015.

    Args:
        data_dir (str): Path to the data directory. Defaults to "data/".
        train_val_split (tuple[float, float]): Train/val split ratio. Defaults to (0.9, 0.1).
        artifact_dir (str): Path to the artifacts directory. Defaults to "artifacts/".
    """

    name: str = "tinyimagenet"
    task: str = "classification"

    classes: list[str]

    data_url: str = ""

    def __init__(
        self,
        *args,
        data_dir: str = "data/",
        train_val_split: tuple[float, float] = (0.9, 0.1),
        artifact_dir: str = "artifacts/",
        **kwargs,
    ):
        super().__init__(*args, data_dir=data_dir, train_val_split=train_val_split, **kwargs)

    @property
    def classes(self):
        if not self._classes:
            metadata_fp = str(Path(self.hparams.artifact_dir, "tinyimagenet", "words.txt"))

            class_names = []

            # 使用 open 函数打开文件，'r' 代表以只读模式打开
            with open(metadata_fp, 'r') as file:
                # 遍历文件的每一行
                for line in file:
                    parts = line.strip().split(maxsplit=1)
                    if len(parts) == 2:  # 确保每行至少有两个部分
                        class_names.append(parts[1])
     
            self._classes = class_names
            self._classes = self.subsample_classes(self._classes)
        return self._classes

    def setup(self, stage: Optional[str] = None):
        """Load data.

        Set variables: `self.data_train`, `self.data_val`, `self.data_test`.
        """
        if self.data_train and self.data_val and self.data_test:
            return

        # setup paths
        dataset_path = Path(self.hparams.data_dir, self.name)

        # some settings
        k_shot = self.hparams.get("k_shot", None)
        seed = self.hparams.get("seed", 5)
        subsample = self.hparams.get("subsample", "all")

        if self.hparams.get("synthetic", False):
            real_train_set = ClassificationDataset(
                str(dataset_path / "train"),
                class_names=self.classes,
                transform=self.get_transforms("train", self.hparams.get("augment", True)),
                split="train",
                k_shot=k_shot,
                seed=seed,
                subsample=subsample,
            )
            synthetic_train_set = SyntheticDataset(
                self.hparams.get("synthetic_data_dir", None),
                transform=self.get_transforms("train", self.hparams.get("augment", True)),
                maximum_synthetic_samples=self.hparams.get("maximum_synthetic_samples", -1),
                class_names=self.classes,
                subsample=subsample,
            )
            train_set = [real_train_set, synthetic_train_set]
        else:
            train_set = ClassificationDataset(
                str(dataset_path / "train"),
                class_names=self.classes,
                transform=self.get_transforms("train", self.hparams.get("augment", True)),
                split="train",
                k_shot=k_shot,
                seed=seed,
                subsample=subsample,
            )

        test_set = ClassificationDataset(
            str(dataset_path / "val"),
            class_names=self.classes,
            transform=self.get_transforms("val", self.hparams.get("augment", True)),
            split="val",
            k_shot=k_shot,
            seed=seed,
            subsample=subsample,
        )

        self.data_train = train_set
        self.data_val = self.data_test = test_set


if __name__ == "__main__":
    _ = ImageNet()

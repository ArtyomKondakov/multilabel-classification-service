import typing as tp
import albumentations as albu
import numpy as np
import torch

from albumentations.pytorch import ToTensorV2

MAX_UINT8 = 255


def preprocess_image(image: np.ndarray, target_image_size: tp.Tuple[int, int]) -> torch.Tensor:
    """Препроцессинг albumentations.

    :param image: RGB изображение;
    :param target_image_size: целевой размер изображения;
    :return: батч с одним изображением.
    """
    preprocess = albu.Compose(
        [
            albu.Resize(height=target_image_size[0], width=target_image_size[1]),
            albu.Normalize(),
            ToTensorV2(),
        ],
    )
    procecces_image = preprocess(image=image)['image']
    return procecces_image[None]

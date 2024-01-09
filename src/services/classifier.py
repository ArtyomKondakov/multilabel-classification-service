import typing as tp

import numpy as np
import torch

from src.services.preprocess_utils import preprocess_image


class Classifier:

    def __init__(self, config: tp.Dict):
        self._model_path = config['model_path']
        self._device = config['device']

        self._model: torch.nn.Module = torch.jit.load(self._model_path, map_location=self._device)
        self._classes: np.ndarray = np.array(config['classes'])
        self._size: tp.Tuple[int, int] = (config['size'], config['size'])
        self._list_thresholds = [config['thresholds']]
        self._thresholds: np.ndarray = np.array(
            self._list_thresholds * len(config['classes']),
        )

    @property
    def satellite_img(self):
        return list(self._classes.tolist())

    def predict(self, image: np.ndarray) -> tp.List[str]:
        """Предсказание списка типов поверхностей земли.

        :param image: RGB изображение;
        :return: список типов поверхностей земли.
        """
        return self._postprocess_predict(self._predict(image))

    def predict_proba(self, image: np.ndarray) -> tp.Dict[str, float]:
        """Предсказание вероятностей принадлежности к определенному типу поверхности земли.

        :param image: RGB изображение.
        :return: словарь вида `тип поверхности`: вероятность.
        """
        return self._postprocess_predict_proba(self._predict(image))

    def _predict(self, image: np.ndarray) -> np.ndarray:
        """Предсказание вероятностей.

        :param image: RGB изображение;
        :return: вероятности после прогона модели.
        """
        batch = preprocess_image(image, self._size).to(self._device)

        with torch.no_grad():
            pred = self._model(batch)
            model_predict = torch.sigmoid(pred)[0].cpu().numpy()

        return model_predict

    def _postprocess_predict(self, predict: np.ndarray) -> tp.List[str]:
        """Постобработка для получения списка типов поверхности земли.

        :param predict: вероятности после прогона модели;
        :return: список типов поверхности земли.
        """
        return self._classes[predict > self._thresholds].tolist()

    def _postprocess_predict_proba(self, predict: np.ndarray) -> tp.Dict[str, float]:
        """Постобработка для получения словаря с вероятностями.

        :param predict: вероятности после прогона модели;
        :return: словарь вида `тип поверхности`: вероятность.
        """
        sorted_idxs = reversed(predict.argsort())
        return {self._classes[i]: float(predict[i]) for i in sorted_idxs}

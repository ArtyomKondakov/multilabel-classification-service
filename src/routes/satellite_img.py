import cv2
import numpy as np
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, File

from src.containers.conainers import AppContainer
from src.routes.routers import router
from src.services.classifier import Classifier


@router.get('/satellite_img')
@inject
def satellite_img_list(service: Classifier = Depends(Provide[AppContainer.classifier])):
    return {
        'satellite_img': service.satellite_img,
    }


@router.post('/predict')
@inject
def predict(
    image: bytes = File(),
    service: Classifier = Depends(Provide[AppContainer.classifier]),
):
    img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    satellite_img = service.predict(img)

    return {'satellite_img': satellite_img}


@router.post('/predict_proba')
@inject
def predict_proba(
    image: bytes = File(),
    service: Classifier = Depends(Provide[AppContainer.classifier]),
):
    img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    return service.predict_proba(img)


@router.get('/health_check')
def health_check():
    return 'OK'

from dependency_injector import containers, providers

from src.services.classifier import Classifier


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    classifier = providers.Singleton(
        Classifier,
        config=config.services.classifier,
    )

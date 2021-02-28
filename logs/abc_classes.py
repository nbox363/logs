from abc import ABC, abstractmethod

import requests
from requests.models import Response

__all__ = ['ABCResp', 'ABCRequestsClient', 'RequestsClient']


class ABCResp(ABC):
    @abstractmethod
    def json(self) -> dict:
        pass


class ABCRequestsClient(ABC):
    @abstractmethod
    def get(self, url) -> ABCResp:
        pass


class RequestsClient(ABCRequestsClient):
    def get(self, url) -> Response:
        return requests.get(url)

from abc import ABC, abstractmethod

import psycopg2
import requests
from psycopg2.extensions import connection
from requests.models import Response

__all__ = ['ABCResp', 'ABCRequestsClient', 'RequestsClient', 'ABCCur', 'ABCConn', 'ABCPsycopgClient', 'ConnClient']


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


class ABCCur(ABC):
    @abstractmethod
    def execute(self, func, *args) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


class ABCConn(ABC):
    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def cursor(self) -> ABCCur:
        pass


class ABCPsycopgClient(ABC):
    @abstractmethod
    def connect(self, **kwargs) -> ABCConn:
        pass


class ConnClient(ABCPsycopgClient):
    def connect(self, **kwargs) -> connection:
        return psycopg2.connect(**kwargs)
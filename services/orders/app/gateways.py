from abc import abstractmethod, ABCMeta
from uuid import uuid4

from flask import current_app
from tinydb import TinyDB, where
from tinyrecord import transaction

from app.exceptions import StorageError, NoResultFound


class AbstractJSONStorageGateway(metaclass=ABCMeta):

    @abstractmethod
    def create(self, data: dict, max_retries: int = 10) -> dict:
        pass

    @abstractmethod
    def update(self, uuid: str, data: dict):
        pass

    @abstractmethod
    def delete(self, uuid: str):
        pass

    @abstractmethod
    def retrieve(self, uuid: str) -> dict:
        pass

    @abstractmethod
    def list_(self):
        pass

    @abstractmethod
    def search(self):
        pass


class TinyDBGateway(AbstractJSONStorageGateway):
    def __init__(self, file_path: str, table_name: str = "_default") -> None:
        self.table = TinyDB(file_path).table(table_name)

    def create(self, data: dict, max_retries: int = 10) -> dict:
        with transaction(self.table) as tr:
            while max_retries > 0:
                uuid = uuid4()
                if not self.table.contains(where('uuid') == str(uuid)):
                    data.update(uuid=str(uuid))
                    tr.insert(data)
                    return data
                else:
                    max_retries -= 1
            raise StorageError('could not set unique UUID')

    def list_(self) -> list:
        return self.table.all()

    def retrieve(self, uuid: str) -> dict:
        record = self.table.get(where('uuid') == uuid)
        if record:
            return record
        else:
            raise NoResultFound('object do not exist')

    def update(self, uuid: str, data: dict):
        with transaction(self.table) as tr:
            record = self.table.get(where('uuid') == uuid)
            if record:
                tr.update(data, where('uuid') == uuid)
            else:
                raise NoResultFound('object do not exist')

    def delete(self, uuid: str):
        with transaction(self.table) as tr:
            record = self.table.get(where('uuid') == uuid)
            if record:
                tr.remove(where('uuid') == uuid)
            else:
                raise NoResultFound('object do not exist')

    def search(self):
        raise NotImplementedError()


def get_default_gateway():
    return TinyDBGateway(file_path=current_app.config['DATABASE_FILE'],
                         table_name=current_app.config['DATABASE_TABLE_NAME'])

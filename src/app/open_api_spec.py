import logging
import threading
from dataclasses import dataclass, field
from typing import List

import yaml

from app.exceptions import HttpUnsupportedMediaTypeError

logger = logging.getLogger(__name__)


# OpenAPI Spec のディクショナリを受け取って、Operationsのコレクションに変換する
class OpenApiSpec:
    # pythonで良い感じのシングルトンを書く - BlankTar
    #   https://blanktar.jp/blog/2016/07/python-singleton.html
    _instance = None
    _lock = threading.Lock()

    # OpenAPI Spec を読み込んで、Operationオブジェクトに変換する
    @classmethod
    def from_yaml(cls, file_path):
        logging.info(f"Getting spec from {file_path}")
        with open(file_path, "r") as f:
            spec = yaml.load(f, yaml.SafeLoader)
        return OpenApiSpec(file_path, spec["openapi"], spec["info"], spec["paths"])

    def __new__(cls, file_path=None, openapi=None, info=None, paths=None):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, file_path=None, openapi=None, info=None, paths=None):
        self.file_path = file_path
        self.openapi = openapi
        self.info = info
        self.paths = paths
        # key: operation_id, value: Operation のディクショナリ
        self.operations = self._paths_to_operations()

    def _paths_to_operations(self):
        operations = {}

        if self.paths is None:
            return operations

        for path, path_item in self.paths.items():
            for method, operation_item in path_item.items():
                if not self.is_method(method):
                    continue

                operation_id = operation_item["operationId"]
                media_types = (
                    operation_item["requestBody"]["content"].keys()
                    if "requestBody" in operation_item.keys()
                    else []
                )

                operations[operation_id] = Operation(
                    operation_id=operation_id, path=path, method=method, media_types=media_types
                )
        return operations

    @classmethod
    def is_method(cls, value):
        return value in ["get", "put", "post", "delete", "options", "head", "patch", "trace"]

    def has_operation(self, operation_id):
        return operation_id in self.operations

    def get_operation(self, operation_id):
        return self.operations.get(operation_id)


# エンドポイントに対応
@dataclass
class Operation:
    operation_id: str
    path: str
    method: str
    # リクエストボディのContent-Typeのリスト
    media_types: List[str] = field(default_factory=list)

    def validate_media_type(self, media_type):
        # Content-Typeが不要なら、指定されていても無視する
        if not self._is_media_type_required():
            return

        if not media_type:
            message = f"Content-type required."
            logger.info(message)
            raise HttpUnsupportedMediaTypeError(message)

        if not self._is_supported_media_type(media_type):
            message = f"Content-type '{media_type}' not supported."
            logger.info(message)
            raise HttpUnsupportedMediaTypeError(message)

    def _is_media_type_required(self):
        return bool(self.media_types)

    def _is_supported_media_type(self, media_type):
        return media_type in self.media_types


_open_api_spec_instance = OpenApiSpec()


def get_operation(operation_id):
    operation = _open_api_spec_instance.get_operation(operation_id)
    if operation:
        return operation
    raise ValueError(f"Operation '{operation_id}' not found.")


def load_open_api_spec(open_api_spec_file):
    OpenApiSpec.from_yaml(file_path=open_api_spec_file)

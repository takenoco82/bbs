import yaml


# OpenAPI Spec のディクショナリを受け取って、Operationsのコレクションに変換する
class OpenApiSpec:
    # OpenAPI Spec を読み込んで、Operationオブジェクトに変換する
    @classmethod
    def load(cls, file_path):
        with open(file_path, "r") as f:
            spec = yaml.load(f, yaml.SafeLoader)
        return OpenApiSpec(file_path, spec["openapi"], spec["info"], spec["paths"])

    def __init__(self, file_path, openapi, info, paths):
        self.file_path = file_path
        self.openapi = openapi
        self.info = info
        self.paths = paths
        # key: operation_id, value: Operation のディクショナリ
        self.operations = self._paths_to_operations()

    def _paths_to_operations(self):
        operations = {}

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


# TODO data_class？で書き換える
# エンドポイントに対応
class Operation:
    def __init__(self, operation_id, path, method, media_types):
        self.operation_id = operation_id
        self.path = path
        self.method = method
        # リクエストボディのContent-Typeのリスト
        self.media_types = media_types

    def __repr__(self):
        return (
            f"Operation("
            f"operation_id={self.operation_id!r}, "
            f"path={self.path!r}, "
            f"method={self.method!r}, "
            f"media_types={self.media_types!r})"
        )


if __name__ == "__main__":
    open_api_spec_file = "/workspace/docs/swagger_spec.yaml"
    open_api_spec = OpenApiSpec.load(open_api_spec_file)
    print(open_api_spec.operations)

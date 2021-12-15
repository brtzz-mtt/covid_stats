from json import dump, load

from .timestamp import Timestamp

class Json(Timestamp):
    __data = None
    __file_path = None

    def __init__(self,
        file_path: str,
        obj: object = {}
    ) -> None:
        super().__init__()
        self.__file_path = file_path
        if obj:
            self.set_data(obj)
        else:
            with open(self.__file_path) as file:
                self.__data = load(file)

    def get_data(self) -> object:
        return self.__data

    def save_data(self) -> 'Json':
        with open(self.__file_path, 'w+') as file:
            dump(self.__obj, file,
                indent = 4
            )
        return self

    def set_data(self,
        obj: object
    ) -> object:
        self.__obj = obj
        return self.__obj

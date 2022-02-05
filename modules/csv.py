from os import path
from requests import get
from csv import reader, writer

from .timestamp import Timestamp

class Csv(Timestamp):
    __data = []
    __file_path = None
    __has_headers = True

    def __init__(self,
        file_path: str,
        url: str = None,
        data: list = None
    ) -> None:
        super().__init__()
        self.__file_path = file_path
        if data:
            self.set_data(data).save_data()
        elif not self.exists(self.__file_path) and url:
            response = get(url)
            if response.status_code == 200:
                with open(self.__file_path, 'w') as file:
                    file.write(response.text)
        elif not self.exists(self.__file_path):
            file = open(self.__file_path, 'w')
        with open(self.__file_path) as file: # creates file if not exists..
            self.set_data(list(reader(file)))
    
    @staticmethod
    def exists(file_path: str):
        return path.exists(file_path)

    def get_data(self) -> list:
        return self.__data

    def get_data_raw(self) -> str:
        output = ''
        for i in range(len(self.__data)):
            output += ",".join([str(element) for element in self.__data[i]]) + "\n"
        return output

    def get_headers(self) -> list:
        if self.__has_headers:
            return self.__data[0]
        return False

    def save_data(self) -> 'Csv':
        with open(self.__file_path, 'w+') as file:
            writer(file).writerows(self.__data)
        return self

    def set_data(self,
        data: list
    ) -> 'Csv':
        self.__data = data
        return self

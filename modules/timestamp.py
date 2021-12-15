from datetime import datetime
from time import time

class Timestamp():
    def __init__(self) -> None:
        self.__unix_timestamp = time()

    def get_date(self) -> str:
        return datetime.fromtimestamp(self.__unix_timestamp).strftime('%Y-%m-%d')

    def get_timestamp(self) -> str:
        return datetime.fromtimestamp(self.__unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_now():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_today():
        return datetime.now().strftime('%Y-%m-%d')

def gn():
    return Timestamp.get_now()

def gt():
    return Timestamp.get_today()
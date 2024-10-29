
class UserRepoBaseException(Exception):
    def __init__(self, code: int, message: str | dict | list):
        self.code = code
        self.message = message


class UserServiceBaseException(Exception):
    def __init__(self, code: int, message: str | dict | list):
        self.code = code
        self.message = message


class AdvertisementRepoBaseException(Exception):
    def __init__(self, code: int, message: str | dict | list):
        self.code = code
        self.message = message


class AdvertisementServiceBaseException(Exception):
    def __init__(self, code: int, message: str | dict | list):
        self.code = code
        self.message = message


class SchemaValidationError(Exception):
    def __init__(self, code: int, message: str | dict | list):
        self.code = code
        self.message = message
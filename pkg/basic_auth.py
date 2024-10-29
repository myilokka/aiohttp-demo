import base64

from pydantic import BaseModel


class AuthException(Exception):
    def __init__(self, code: int, message: str | dict | list):
        self.code = code
        self.message = message


class BasicAuthCreds(BaseModel):
    email: str
    password: str


def basic_auth(headers: dict) -> BasicAuthCreds:
    auth_data = headers.get('Authorization')
    if not auth_data:
        raise AuthException(code=401, message='Authorization is missing')

    if not auth_data.startswith('Basic'):
        raise AuthException(code=401, message='Wrong authorization type')

    auth_data = auth_data.replace('Basic', '').strip(' ')
    auth_data = base64.b64decode(auth_data.encode('utf-8')).decode('utf-8')
    email, password = auth_data.split(':')

    return BasicAuthCreds(email=email, password=password)

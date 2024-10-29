import re
from typing import Optional
from typing_extensions import Self
from pydantic import BaseModel, model_validator

from app.ecxeptions import SchemaValidationError


class UserCreate(BaseModel):
    name: str
    email: str
    hashed_password: str


class UserUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    email: Optional[str] = None
    hashed_password: Optional[str] = None


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    advertisements: Optional[list["AdvertisementOut"]] = None


class PasswordValidation(BaseModel):
    password: Optional[str] = None
    confirm_password: Optional[str] = None

    @model_validator(mode='after')
    def check_password(self) -> Self:
        pw1 = self.password
        pw2 = self.confirm_password
        if pw1 != pw2:
            raise SchemaValidationError(code=412, message='Passwords do not match')
        if pw1 and not (len(pw1) >= 8 and re.search(r"\d", pw1) and re.search(r"[A-ZА-Я]", pw1)):
            raise SchemaValidationError(code=412,
                                        message="Password must be at least 8 characters long and contain at least one uppercase and one digit.")
        return self


class UserRegister(PasswordValidation):
    name: str
    email: str
    password: str
    confirm_password: str


class UserUpdateByUser(PasswordValidation):
    id: int
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None


class UserLogin(BaseModel):
    email: str
    password: str


########################################################################################################################

class AdvertisementCreate(BaseModel):
    title: str
    description: str
    user_id: int


class AdvertisementUpdate(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None


class AdvertisementOut(BaseModel):
    id: int
    title: str
    description: str
    user_id: int

import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from app.repo.user import UserRepo
from app.schema import UserRegister, UserOut, UserCreate, UserUpdateByUser, UserUpdate
from pkg.basic_auth import BasicAuthCreds, AuthException


class UserService:

    async def register(self, data: UserRegister, session: AsyncSession) -> UserOut:
        hashed_password = self._hash_password(data.password)
        create_data = UserCreate(
            name=data.name,
            email=data.email,
            hashed_password=hashed_password
        )
        return await UserRepo.create(create_data, session)

    async def update(self, data: UserUpdateByUser, creds: BasicAuthCreds, session: AsyncSession) -> UserOut:
        user = await self.authenticate(creds, session)
        if user.id != data.id:
            raise AuthException(code=403, message='Access denied')
        update_data = UserUpdate(
            id=data.id
        )
        if data.password:
            update_data.hashed_password = self._hash_password(data.password)
        if data.name:
            update_data.name = data.name
        if data.email:
            update_data.email = data.email
        return await UserRepo.update(update_data, session)

    async def get_list(self, session: AsyncSession) -> list[UserOut]:
        return await UserRepo.get_list(session)

    async def get_by_id(self, id_: int, session: AsyncSession) -> UserOut:
        return await UserRepo.get_by_id(id_, session)

    async def delete(self, id_: int, creds: BasicAuthCreds, session: AsyncSession) -> UserOut:
        user = await self.authenticate(creds, session)
        if user.id != id_:
            raise AuthException(code=403, message='Access denied')
        return await UserRepo.delete(id_, session)

    def _hash_password(self, password: str) -> str:
        password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password, salt).decode('utf-8')

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        password = password.encode('utf-8')
        hashed_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password, hashed_password)

    async def authenticate(self, creds: BasicAuthCreds, session: AsyncSession) -> UserOut:
        hashed_password = await UserRepo.get_password_by_email(creds.email, session)
        if not hashed_password:
            raise AuthException(code=401, message='Invalid email')
        if not self._verify_password(creds.password, hashed_password):
            raise AuthException(code=401, message='Invalid password')
        return await UserRepo.get_by_email(creds.email, session)

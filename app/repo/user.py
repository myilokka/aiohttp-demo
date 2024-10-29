from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from app.repo.advertisement import AdvertisementRepo
from app.models import User
from app.schema import UserUpdate, UserOut, UserCreate
from app.ecxeptions import UserRepoBaseException


class UserRepo:
    @staticmethod
    async def get_list(session: AsyncSession) -> list[UserOut]:
        users = await session.scalars(select(User).options(selectinload(User.advertisements)))
        return [UserRepo.to_schema(user) for user in users.all()]

    @staticmethod
    async def get_by_id(id_: int, session: AsyncSession) -> UserOut:
        user = (await session.scalars(
            select(User).where(User.id == id_).options(selectinload(User.advertisements)))).first()
        if user:
            return UserRepo.to_schema(user)
        else:
            raise UserRepoBaseException(code=404, message='User not found')

    @staticmethod
    async def get_by_email(email: str, session: AsyncSession) -> UserOut:
        user = (await session.scalars(
            select(User).where(User.email == email).options(selectinload(User.advertisements)))).first()
        if user:
            return UserRepo.to_schema(user)
        else:
            raise UserRepoBaseException(code=404, message='User not found')

    @staticmethod
    async def get_password_by_email(email: str, session: AsyncSession) -> str:
        hashed_password = await session.scalars(select(User.hashed_password).filter(User.email == email))
        if hashed_password:
            return hashed_password.first()
        else:
            raise UserRepoBaseException(code=404, message='User not found')

    @staticmethod
    async def create(data: UserCreate, session: AsyncSession) -> UserOut:
        user = User(
            name=data.name,
            email=data.email,
            hashed_password=data.hashed_password
        )
        try:
            session.add(user)
            await session.commit()
        except IntegrityError as e:
            raise UserRepoBaseException(code=409, message=str(e))
        user = (await session.scalars(
            select(User).where(User.id == user.id).options(selectinload(User.advertisements)))).first()
        return UserRepo.to_schema(user)

    @staticmethod
    async def update(data: UserUpdate, session: AsyncSession) -> UserOut:
        user = await session.get(User, data.id)
        if user is None:
            raise UserRepoBaseException(code=404, message='User not found')
        if data.name:
            user.name = data.name
        if data.email:
            user.email = data.email
        if data.hashed_password:
            user.hashed_password = data.hashed_password
        try:
            await session.commit()
        except IntegrityError as e:
            raise UserRepoBaseException(code=409, message=str(e))
        user = (await session.scalars(
            select(User).where(User.id == user.id).options(selectinload(User.advertisements)))).first()
        return UserRepo.to_schema(user)

    @staticmethod
    async def delete(id_: int, session: AsyncSession) -> UserOut:
        user = (await session.scalars(
            select(User).where(User.id == id_).options(selectinload(User.advertisements)))).first()
        if user is None:
            raise UserRepoBaseException(code=404, message='User not found')
        await session.delete(user)
        await session.commit()
        return UserRepo.to_schema(user)

    @staticmethod
    def to_schema(obj: User) -> UserOut:
        user = UserOut(
            id=obj.id,
            name=obj.name,
            email=obj.email
        )
        if obj.advertisements:
            advertisements = []
            for adv in obj.advertisements:
                advertisements.append(AdvertisementRepo.to_schema(adv))
            user.advertisements = advertisements
        return user

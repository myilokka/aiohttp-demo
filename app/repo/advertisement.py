from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Advertisement
from app.schema import AdvertisementUpdate, AdvertisementOut, AdvertisementCreate
from app.ecxeptions import AdvertisementRepoBaseException


class AdvertisementRepo:

    @staticmethod
    async def get_by_id(id_: int, session: AsyncSession) -> AdvertisementOut:
        adv = await session.get(Advertisement, id_)
        if adv is not None:
            return AdvertisementRepo.to_schema(adv)
        else:
            raise AdvertisementRepoBaseException(code=404, message='Advertisement not found')

    @staticmethod
    async def get_list(session: AsyncSession) -> list[AdvertisementOut]:
        advs = await  session.scalars(select(Advertisement))
        return [AdvertisementRepo.to_schema(adv) for adv in advs]

    @staticmethod
    async def create(data: AdvertisementCreate, session: AsyncSession) -> AdvertisementOut:
        adv = Advertisement(
            title=data.title,
            description=data.description,
            user_id=data.user_id
        )
        session.add(adv)
        try:
            await session.commit()
        except IntegrityError:
            raise AdvertisementRepoBaseException(code=409, message='Advertisement already exists')
        return AdvertisementRepo.to_schema(adv)

    @staticmethod
    async def update(data: AdvertisementUpdate, session: AsyncSession) -> AdvertisementOut:
        adv = await session.get(Advertisement, data.id)
        if adv is None:
            raise AdvertisementRepoBaseException(code=404, message='Advertisement not found')
        if data.title:
            adv.title = data.title
        if data.description:
            adv.description = data.description
        await session.commit()
        return AdvertisementRepo.to_schema(adv)

    @staticmethod
    async def delete(id_: int, session: AsyncSession) -> AdvertisementOut:
        adv = await session.get(Advertisement, id_)
        if adv is None:
            raise AdvertisementRepoBaseException(code=404, message='Advertisement not found')
        await session.delete(adv)
        await session.commit()
        return AdvertisementRepo.to_schema(adv)

    @staticmethod
    def to_schema(obj: Advertisement) -> AdvertisementOut:
        return AdvertisementOut(
            id=obj.id,
            title=obj.title,
            description=obj.description,
            created=obj.created,
            user_id=obj.user_id
        )

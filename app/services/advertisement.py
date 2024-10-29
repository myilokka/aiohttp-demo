from sqlalchemy.ext.asyncio import AsyncSession

from app.repo.advertisement import AdvertisementRepo
from app.schema import AdvertisementOut, AdvertisementCreate, AdvertisementUpdate
from app.services.user import UserService
from pkg.basic_auth import BasicAuthCreds, AuthException


class AdvertisementService:
    def __init__(self):
        self.user_service = UserService()

    async def create(self, data: AdvertisementCreate, creds: BasicAuthCreds, session: AsyncSession) -> AdvertisementOut:
        user = await self.user_service.authenticate(creds, session)
        if user.id != data.user_id:
            raise AuthException(code=403, message='Access denied')
        return await AdvertisementRepo.create(data, session)

    async def update(self, data: AdvertisementUpdate, creds: BasicAuthCreds, session: AsyncSession) -> AdvertisementOut:
        user = await self.user_service.authenticate(creds, session)
        ad = await AdvertisementRepo.get_by_id(data.id, session)
        if user.id != ad.user_id:
            raise AuthException(code=403, message='Access denied')
        update_data = AdvertisementUpdate(
            id=data.id
        )
        if data.title:
            update_data.title = data.title
        if data.description:
            update_data.description = data.description
        return await AdvertisementRepo.update(update_data, session)

    async def get_list(self, session: AsyncSession) -> list[AdvertisementOut]:
        return await AdvertisementRepo.get_list(session)

    async def get_by_id(self, id_: int, session: AsyncSession) -> AdvertisementOut:
        return await AdvertisementRepo.get_by_id(id_, session)

    async def delete(self, id_: int, creds: BasicAuthCreds, session: AsyncSession) -> AdvertisementOut:
        user = await self.user_service.authenticate(creds, session)
        ad = await AdvertisementRepo.get_by_id(id_, session)
        if user.id != ad.user_id:
            raise AuthException(code=403, message='Access denied')
        return await  AdvertisementRepo.delete(id_, session)

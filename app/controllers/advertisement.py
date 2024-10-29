import pydantic
from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema import AdvertisementCreate, AdvertisementUpdate
from app.services.advertisement import AdvertisementService
from pkg.basic_auth import basic_auth, AuthException
from app.ecxeptions import AdvertisementRepoBaseException, SchemaValidationError, UserRepoBaseException
from pkg.error_handlers import get_http_error


class AdvertisementView(web.View):
    service = AdvertisementService()

    @property
    def id_(self):
        return int(self.request.match_info["id_"])

    @property
    def session(self) -> AsyncSession:
        return self.request.session

    async def get(self):
        try:
            advertisements = await self.service.get_list(self.session)
            return web.json_response([ad.model_dump() for ad in advertisements])
        except SchemaValidationError as e:
            raise get_http_error(e.code, e.message)
        except UserRepoBaseException as e:
            raise get_http_error(e.code, e.message)
        except AuthException as e:
            raise get_http_error(e.code, e.message)
        except pydantic.ValidationError as e:
            raise get_http_error(412, str(e))
        except AdvertisementRepoBaseException as e:
            raise get_http_error(e.code, e.message)

    async def post(self):
        try:
            creds = basic_auth(self.request.headers)
            json_data = await self.request.json()
            data = AdvertisementCreate(**json_data)
            adv = await self.service.create(data, creds, self.session)
            return web.json_response(adv.model_dump())
        except SchemaValidationError as e:
            raise get_http_error(e.code, e.message)
        except UserRepoBaseException as e:
            raise get_http_error(e.code, e.message)
        except pydantic.ValidationError as e:
            raise get_http_error(412, str(e))
        except AdvertisementRepoBaseException as e:
            raise get_http_error(e.code, e.message)
        except AuthException as e:
            raise get_http_error(e.code, e.message)

    async def patch(self):
        try:
            creds = basic_auth(self.request.headers)
            json_data = await self.request.json()
            data = AdvertisementUpdate(**json_data)
            adv = await self.service.update(data, creds, self.session)
            return web.json_response(adv.model_dump())
        except AdvertisementRepoBaseException as e:
            raise get_http_error(e.code, e.message)
        except SchemaValidationError as e:
            raise get_http_error(e.code, e.message)
        except UserRepoBaseException as e:
            raise get_http_error(e.code, e.message)
        except AuthException as e:
            raise get_http_error(e.code, e.message)
        except pydantic.ValidationError as e:
            raise get_http_error(412, str(e))

    async def delete(self):
        try:
            creds = basic_auth(self.request.headers)
            user = await self.service.delete(self.id_, creds, self.session)
            return web.json_response(user.model_dump())
        except SchemaValidationError as e:
            raise get_http_error(e.code, e.message)
        except UserRepoBaseException as e:
            raise get_http_error(e.code, e.message)
        except AuthException as e:
            raise get_http_error(e.code, e.message)
        except pydantic.ValidationError as e:
            raise get_http_error(412, str(e))
        except AdvertisementRepoBaseException as e:
            raise get_http_error(e.code, e.message)

# @app.route('/advertisement/<int:id_>/', methods=["GET"])
# def get_advertisement(id_: int) -> dict:
#     try:
#         return service.get_by_id(id_).model_dump()
#     except SchemaValidationError as e:
#         raise HttpError(code=e.code, message=e.message)
#     except AdvertisementRepoBaseException as e:
#         raise HttpError(code=e.code, message=e.message)
#     except pydantic.ValidationError as e:
#         raise HttpError(code=412, message=str(e))
#     except UserRepoBaseException as e:
#         raise HttpError(code=e.code, message=e.message)

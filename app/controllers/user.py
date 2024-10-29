import pydantic
from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema import UserRegister, UserUpdateByUser
from app.services.user import UserService
from pkg.basic_auth import basic_auth, AuthException
from app.ecxeptions import UserRepoBaseException, SchemaValidationError
from pkg.error_handlers import get_http_error


class UserView(web.View):
    service = UserService()

    @property
    def id_(self):
        id_ = self.request.match_info.get("id_")
        if id_:
            return int(id_)


    @property
    def session(self) -> AsyncSession:
        return self.request.session

    async def get(self):
        try:
            if self.id_:
                user = await self.service.get_by_id(self.id_, self.session)
                return web.json_response(user.model_dump())
            else:
                users = await self.service.get_list(self.session)
                return web.json_response([user.model_dump() for user in users])
        except SchemaValidationError as e:
            raise get_http_error(e.code, e.message)
        except UserRepoBaseException as e:
            raise get_http_error(e.code, e.message)
        except pydantic.ValidationError as e:
            raise get_http_error(412, str(e))

    async def post(self):
        try:
            user_data = await self.request.json()
            data = UserRegister(**user_data)
            user = await self.service.register(data, self.session)
            return web.json_response(user.model_dump())
        except SchemaValidationError as e:
            raise get_http_error(e.code, e.message)
        except UserRepoBaseException as e:
            raise get_http_error(e.code, e.message)
        except pydantic.ValidationError as e:
            raise get_http_error(412, str(e))

    async def patch(self):
        try:
            creds = basic_auth(self.request.headers)
            json_data = await self.request.json()
            data = UserUpdateByUser(**json_data)
            user = await self.service.update(data, creds, self.session)
            return web.json_response(user.model_dump())
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

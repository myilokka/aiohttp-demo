from aiohttp import web

from app.middlwares import session_middleware
from database import orm_context

app = web.Application()

app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)
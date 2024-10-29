from aiohttp import web

from app import app, routers

web.run_app(app)

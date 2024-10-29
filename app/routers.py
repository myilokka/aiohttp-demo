from aiohttp import web

from app import app
from app.controllers.advertisement import AdvertisementView
from app.controllers.user import UserView

app.add_routes(
    [
        web.post("/user/", UserView),
        web.get("/user/{id_:\d+}/", UserView),
        web.get("/user/", UserView),
        web.patch("/user/", UserView),
        web.delete("/user/{id_:\d+}/", UserView),
    ]
)
app.add_routes(
    [
        web.post("/advertisement/", AdvertisementView),
        web.get("/advertisement/", AdvertisementView),
        web.patch("/advertisement/", AdvertisementView),
        web.delete("/advertisement/{id_:\d+}/", AdvertisementView),
    ]
)

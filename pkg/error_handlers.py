import json

from aiohttp.web_exceptions import HTTPBadRequest, HTTPNotFound, HTTPConflict, HTTPForbidden, HTTPUnauthorized, \
    HTTPPreconditionFailed


def get_http_error(code: int, msg: str | dict | list):
    exp_class = HTTPBadRequest
    if code == 404:
        exp_class = HTTPNotFound
    elif code == 409:
        exp_class = HTTPConflict
    elif code == 403:
        exp_class = HTTPForbidden
    elif code == 401:
        exp_class = HTTPUnauthorized
    elif code == 412:
        exp_class = HTTPPreconditionFailed
    return exp_class(
        text=json.dumps(
            {"status": "error",
             "error": msg},
        ),
        content_type="application/json",
    )

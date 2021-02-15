import os
from pprint import pprint

from sanic import Sanic
from sanic.response import json

import user

app = Sanic("architect_hw_2_app")
app.blueprint(user.users)


def server_error_handler(request, exception):
    pprint(exception)
    status_code = getattr(exception, 'status_code', 500)
    msg = str(exception) or "Oops, server error"
    return json({"error": msg, "status": status_code})


app.error_handler.add(Exception, server_error_handler)


@app.route("/health/")
async def health(request):
    return json({"status": "OK"})


@app.route("/")
async def root(request):
    return json({'result': 'Hello world from ' + os.environ['HOSTNAME'] + '!'})

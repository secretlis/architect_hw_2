import os
from pprint import pprint

from sanic import Sanic
from sanic.response import json
from sanic_prometheus import monitor
from user import users
from db import db, DATABASE_URI

app = Sanic("architect_hw_2_app")
app.blueprint(users)

monitor(app).expose_endpoint()


@app.listener('before_server_start')
async def connect_to_db(app, loop):
    print("Init gino")
    app.engine = await db.set_bind(DATABASE_URI)
    print(app.engine)


@app.listener('after_server_stop')
async def rm_db_connection(app, loop):
    try:
        await db.pop_bind().close()
    except:
        pass


def server_error_handler(request, exception):
    pprint(exception)
    status_code = getattr(exception, 'status_code', 500)
    msg = str(exception) or "Oops, server error"
    return json({"error": msg, "status": status_code}, status=status_code)


app.error_handler.add(Exception, server_error_handler)


@app.route("/health/")
async def health(request):
    return json({"status": "OK"})


@app.route("/")
async def root(request):
    return json({'result': 'Hello world from ' + os.environ['HOSTNAME'] + '!'})

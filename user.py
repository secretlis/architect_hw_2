from sanic import Blueprint
from sanic.exceptions import InvalidUsage, NotFound
from sanic.response import json

from db import User

users = Blueprint('user', url_prefix='/user')


@users.route("/<user_id>", methods=["GET"])
async def get_user(request, user_id):
    user = await User.get(int(user_id))
    if not user:
        raise NotFound(message='User not found')
    return json({"result": user.to_dict()})


@users.route("/<user_id>", methods=["PUT"])
async def update_user(request, user_id):
    name = request.form.get('name')
    user = await User.get(int(user_id))
    if not user:
        raise NotFound(message='User not found')
    if name:
        await user.update(name=name).apply()
    return json({"result": user.to_dict()})


@users.route("/", methods=["POST"])
async def create_user(request):
    if not request.form.get('name'):
        raise InvalidUsage(message="name not found in %s" % str(request.form))
    name = request.form.get('name')
    user = await User.create(name=name)
    return json({"result": user.to_dict()})


@users.route("/<user_id>", methods=["DELETE"])
async def rm_user(request, user_id):
    user = await User.get(int(user_id))
    if not user:
        raise NotFound(message='User not found')
    await user.delete()
    return json({"result": 'ok'})


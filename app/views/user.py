"""
user 视图
"""

from flask import request, g

from app.libs.rest import RestView
from app.models.user import User
from app.serializers.user import UserSchema
from app.libs.error import RestError

from .decorators import ObjectMustBeExist, TokenAuthenticate


class UserList(RestView):
    """
    获取用户列表，添加用户
    """

    def get(self):
        users = User.query.all()
        return UserSchema().dump(users, many=True).data

    def post(self):
        data = request.get_json()
        user, errors = UserSchema().load(data)
        if errors:
            return errors, 400
        user.save()
        data = {'ok': True, 'message': 'success'}
        return data, 201


class UserDetail(RestView):
    """
    获取用户详情，更新用户，删除用户
    """

    method_decorators = (TokenAuthenticate(), ObjectMustBeExist(User))

    def get(self, id):
        print('#### get self: ', self)

        data, _ = UserSchema().dump(g.instance)
        return data

    def put(self, id):
        schema = UserSchema(context={'instance': g.instance})
        data = request.get_json()
        user, errors = schema.load(data, partial=True)
        if errors:
            return errors, 400
        user.save()
        data = {'ok': True, 'message': 'success'}
        return data

    def delete(self, id):
        # 删除的时候要判断是否还有管理员账号
        c = User.query.filter(User.is_admin == 1).count()
        if c == 1:
            raise RestError(400, 'must have one administrator')

        g.instance.delete()
        data = {'ok': True, 'message': 'success'}
        return data, 204
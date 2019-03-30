"""
用户登录认证视图
"""

from datetime import datetime
from flask import request

from app.libs.rest import RestView
from app.libs.error import AuthenticationError
from app.models.user import User

# from flask.views import MethodView


class AuthView(RestView):
    """
     用户可以通过用户名或邮箱登录，登录成功后返回用于后续认证的 token
    """

    def post(self):
        data = request.get_json()
        if data is None:
            return {'ok', False}

        identifier = data.get('identifier')
        password = data.get('password')

        if not identifier or not password:
            raise AuthenticationError(403, 'username or password is required')

        user = User.authenticate(identifier, password)
        user.login_at = datetime.utcnow()
        user.save()

        return {'ok': 'True', 'token': user.generate_token()}

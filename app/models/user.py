"""
用户相关模型
"""

from datetime import datetime, timedelta
from calendar import timegm

import jwt
from flask import current_app

from app.extensions import db
from .base import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from app.libs.error import AuthenticationError, InvalidTokenError


class User(BaseModel):
    """ 用户模型 """

    __tablename__ = "user"

    username = db.Column(db.String(32), unique=True)
    realname = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    _password = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    login_at = db.Column(db.DateTime)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        """ 设置密码 """
        self._password = generate_password_hash(password)

    def verify_passwork(self, password):
        """ 检查密码 """
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, identifier, password):
        """ 认证用户 用户名或邮箱登录"""
        user = cls.query.filter(db.or_(cls.username == identifier,
                                       cls.email == identifier)).first()
        if not user or not user.verify_passwork(password):
            raise AuthenticationError(403, 'authentication failed')

        return user

    @classmethod
    def create_admin(cls):
        """ 创建管理员账号 """
        username = 'admin'

        # 检查管理员账号是否存在
        admin = cls.query.filter_by(username=username).first()
        if admin:
            return admin.username, ''

        # 不存在则创建
        password = '123456'
        admin = User(username=username,
                     email='admin@xxoo.com',
                     is_admin=True)
        admin.password = password
        admin.save()
        return username, password

    def generate_token(self):
        """ 生成 json web token
        生成 token，有效期为 1 天，过期后十分钟内可以使用老 token 刷新获取新的token
        """

        # token 过期时间，默认有效期为1天
        exp_time = datetime.utcnow() + timedelta(days=1)

        # token 过期后10分钟内，可以使用老的token进行刷新，得到新的token
        refresh_exp = timegm((exp_time + timedelta(seconds=60 * 10)).utctimetuple())

        try:

            payload = {
                'uid': self.id,
                'is_admin': self.is_admin,
                'exp': exp_time,
                'refresh_exp': refresh_exp
            }

            return jwt.encode(payload, current_app.secret_key, algorithm='HS512').decode('utf-8')
        except Exception as e:
            return e

    @classmethod
    def verify_token(cls, token, verify_exp=True):
        """ 验证token """

        now = datetime.utcnow()

        if verify_exp:
            options = None
        else:
            options = {'verify_exp': False}

        try:
            payload = jwt.decode(token, current_app.secret_key, verify=True,
                                 algorithm=['HS512'], options=options, require_exp=True)
        except jwt.InvalidTokenError as e:
            raise InvalidTokenError(403, str(e))

        if any(('is_admin' not in payload,
                'refresh_exp' not in payload,
                'uid' not in payload)):
            raise InvalidTokenError(403, 'invalid token')

        # 如果刷新时间过期，则认为 token 无效
        if payload['refresh_exp'] < timegm(now.utctimetuple()):
            raise InvalidTokenError(403, 'invalid token')

        user = cls.query.get(payload.get('uid'))
        if user is None:
            raise InvalidTokenError(403, 'user not exist.')

        return user

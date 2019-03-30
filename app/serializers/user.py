"""
模型对象序列化类
"""

from marshmallow import (Schema, fields, validate, post_load,
                         validates_schema, ValidationError)

from app.models.user import User
from app.extensions import db


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(4, 32))
    realname = fields.String(required=True, validate=validate.Length(4, 32))
    email = fields.Email(required=True, validate=validate.Length(8, 64))
    password = fields.String(load_only=True, validate=validate.Length(5, 20))
    is_admin = fields.Boolean()
    login_at = fields.DateTime(dump_only=True)

    create_time = fields.DateTime(dump_only=True)
    # update_time = fields.DateTime(dump_only=True)
    # remark = fields.String()

    @validates_schema
    def validate_schema(self, data):
        """
        检查数据
        """

        instance = self.context.get('instance', None)
        user = User.query.filter(db.or_(User.username == data.get('username'),
                                        User.email == data.get('email'))).first()
        if user is None:
            return

        # 创建用户时调用
        if instance is None:
            field = 'username' if user.username == data['username'] else 'email'
            raise ValidationError('{} user already exist'.format(user.username))

        # 更新用户时调用

    @post_load
    def create_or_update(self, data):
        """
        数据加载成功后自动创建 User
        """

        instance = self.context.get('instance', None)

        # 创建用户
        if instance is None:
            user = User()
        # 更新用户
        else:
            user = instance

        for key in data:
            setattr(user, key, data[key])

        return user
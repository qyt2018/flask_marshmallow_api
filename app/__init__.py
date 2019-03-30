"""
该模块主要实现了 app 创建函数
"""

from flask import Flask

from app.config import DevConfig, ProductConfig, config
from app.extensions import init_ext

from app.urls import api

from app.models.user import User


def create_app():
    """ 创建并初使化 Flask app """

    app = Flask(__name__)

    app.config.from_object(DevConfig)

    # 初使化第三方扩展插件
    init_ext(app=app)

    # 加载db模型
    from app import models

    # 创建一个默认的管理员账号
    # with app.app_context():
    #     User.create_admin()

    # 注册蓝图，加载路由
    app.register_blueprint(api)

    return app

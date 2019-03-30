"""
配置文件
"""


class DevConfig:
    """ 开发环境配置 """

    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = 'mlhrjuv0qz1mm=cfinicja1dSzjbtcwvpvyf4vo0zss5vvcC44'

    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/flask_marshmallow?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductConfig:
    """ 生产环境配置 """
    SECRET_KEY = 'lmamn6zytky8xC9g28gix;swii4sDqjxybiyr6rsjrnx0qmsht'

    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/flask_marshmallow_prod?charset=utf8'


config = {
    'dev': DevConfig,
    'pro': ProductConfig,
    'default': DevConfig
}

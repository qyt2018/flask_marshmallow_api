"""
项目所有的第三方扩展包
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def init_ext(app):
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)

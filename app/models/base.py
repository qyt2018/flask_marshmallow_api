"""
模型基类
"""

from datetime import datetime

from app.extensions import db


class BaseModel(db.Model):
    """
    通过设置 __abstract__ 属性，成为 SQLAlchemy 抽象基类，不再映射到数据库中
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow())
    update_time = db.Column(db.DateTime, default=datetime.utcnow())
    remark = db.Column(db.String(256), default='')

    def __repr__(self):
        try:
            identifier = self.name
        except AttributeError:
            identifier = self.id
        return "<{} {}>".format(self.__class__.__name__, identifier)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

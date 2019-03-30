"""
定义所有 API 对应的 URL
"""

from flask import Blueprint

from app.views.index import IndexView
from app.views.auth import AuthView
from app.views.user import UserList, UserDetail


api = Blueprint('api', __name__)

# 主页
api.add_url_rule('/', view_func=IndexView.as_view('index'))

# 登录
api.add_url_rule('/login', view_func=AuthView.as_view('login'))

# 用户管理
api.add_url_rule('/users/', view_func=UserList.as_view('user_list'))
api.add_url_rule('/users/<int:id>',
                 view_func=UserDetail.as_view('user_detail'))
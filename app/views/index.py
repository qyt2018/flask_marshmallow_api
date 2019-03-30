"""
首页视图
"""

from flask.views import MethodView


class IndexView(MethodView):
    """首页视图
    """

    def get(self):
        return "hello word......"

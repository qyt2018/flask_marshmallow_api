

后端环境：
```
Python 3.6
Flask 1.0.2
marshmallow 2.19.1
PyJWT

```



项目目录结构：
```
├── app                     # 项目app总目录
│   ├── __init__.py         # 初使化文件
│   ├── config.py           # 配置文件   
│   ├── extensions.py       # 第三方扩展插件
│   ├── libs                # 共同类，函数包
│   ├── models              # 数据库模型包
│   ├── serializers         # 序列化包
│   ├── urls.py             # 视图路由url文件
│   └── views               # 业务处理视图包
├── manage.py               # 程序入口文件
├── migrations              # 数据库模型等变更
│   ├── README
│   ├── __pycache__
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── readme.md
├── requirements.txt

```

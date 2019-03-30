"""
项目入口
"""

import pymysql
pymysql.install_as_MySQLdb()

from flask_migrate import MigrateCommand
from flask_script import Manager

from app import create_app

app = create_app()

manager = Manager(app=app)
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()

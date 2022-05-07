# coding: UTF-8

from ihome import create_app, db
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate

# 创建app
# 参数为 Develop,或 Product
app = create_app('Develop')
manager = Manager(app)

Migrate(app, db)
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()

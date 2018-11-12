from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from app import app
from extensions import db

from models import Admin,Category,Post,Comment

manager=Manager(app)
migrate=Migrate(app,db)

manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()
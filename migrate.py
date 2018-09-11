from run_setup import app
from app.v1.models.db_connection import DB
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, DB)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def initialize():
    """
     Initialize application by inserting required roles for creating users.
    """
    from flask_migrate import upgrade
    upgrade()



if __name__ == '__main__':
    manager.run()
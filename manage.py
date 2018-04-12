"""
Provides a command line utility for interacting with the
application to perform interactive debugging and setup
"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import remembrallapi.config
from remembrallapi.application import create_app
from remembrallapi.models import db, User, Pay, Plan, PlanUser

app = create_app()
DATABASE_URI = getattr(remembrallapi.config, "SQLALCHEMY_DATABASE_URI", "")
is_sqlite = DATABASE_URI.startswith("sqlite:")
migrate = Migrate(app, db, render_as_batch=is_sqlite)
manager = Manager(app)

# Provide a migration utility command
manager.add_command("db", MigrateCommand)

# Provide a migration shell with application context


@manager.shell
def shell_ctx():
    return dict(app=app, db=db, User=User, Pay=Pay, Plan=Plan, plan_user=plan_user)


if __name__ == "__main__":
    manager.run()

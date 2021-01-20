import os

from flask_migrate import Migrate
from app.models.content import Content
from app.models.entity import Entity
from app.models.user import User

from app import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Content=Content, Entity=Entity, User=User)

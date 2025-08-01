from flask.cli import FlaskGroup
from app import create_app
from extensions import db

app = create_app()
cli = FlaskGroup(create_app=create_app)

if __name__ == '__main__':
    cli()

# With this, run:
#  $ flask db init
#  $ flask db migrate -m "Initial migration"
#  $ flask db upgrade
#  $ flask seed

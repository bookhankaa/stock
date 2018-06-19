from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from config import Config

import connexion

app = connexion.App(__name__, specification_dir='./', debug=True)

app.app.config.from_object(Config)
db = SQLAlchemy(app.app)
migrate = Migrate(app.app, db)
login = LoginManager(app.app)
login.login_view = 'login'

app.add_api('swagger.yml')


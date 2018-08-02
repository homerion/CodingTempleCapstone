from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# from flask_wtf.csrf import CSRFProtect

app=Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
# csrf.init_app(app)
login = LoginManager(app)
login.login_view = 'login'
login.init_app(app)

from app import routes, models

bootstrap=Bootstrap(app)

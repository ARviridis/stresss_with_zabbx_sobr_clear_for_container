import os
import config1 as cfg
from flask import Flask
from flask_login import LoginManager
from app import info
from app import timemon as tm

from static.flask_bootstrap import Bootstrap

app = Flask(cfg.server_name)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config.from_object(cfg)

UPL = os.path.dirname('static')
app.secret_key = 'szypkiwonsz'
login = LoginManager(app)
login.login_view = 'login2'

print("Starting time monitor for", cfg.time_step, "s period")
tm.start()
print("Starting web server", cfg.server_name)

from . import database
database.init_app(app)

bootstrap = Bootstrap(app)
from app import routes, monitor,routes2,upl,zabbx




from flask import Flask
from app.database import db,migrate
from flask_restx import Api
from app.routes.user import User_api
from app.routes.login import Login_api
from app.routes.diet import Diet_api
from app.config import config
from app.models.user import User
from app.models.recomended import Recommended
from app.models.diet import Diet

app=Flask(__name__)
api=Api(app)
api.add_namespace(User_api,'/users')
api.add_namespace(Login_api,'/login')
api.add_namespace(Diet_api,'/Diet')

def create_app(env):
    app.config.from_object(config[env])
    db.init_app(app)
    migrate.init_app(app, db)
    return app


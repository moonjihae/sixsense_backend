from flask import Flask
from app.database import db,migrate
from flask_restx import Api
from app.routes.user import User_api
from app.routes.login import Login_api
from app.routes.diet import Diet_api
from app.routes.predict import Predict_api
from app.config import config
from app.models.user import User
from app.models.recomended import Recommended
from app.models.diet import Diet
from app.models.like import Like
from app.models.daily_nutrition import Daily_nutrition
from app.utils.custom_exception import *

app=Flask(__name__)
api=Api(app)
api.add_namespace(User_api,'/users')
api.add_namespace(Login_api,'/login')
api.add_namespace(Diet_api,'/diets')
api.add_namespace(Predict_api,'/predict')

def create_app(env):
    app.config.from_object(config[env])
    db.init_app(app)
    migrate.init_app(app, db,render_as_batch=True)
    return app

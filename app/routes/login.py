from app.models.user import User
from flask import request
from flask_restx import Namespace,Resource
from app.database import db
Login_api=Namespace('Login_api')

@Login_api.route('/')
class Login(Resource):
    def get(self):
        data = request.get_json()
        email=data['email']
        user_name=data['user_name']
        user=User.query.filter_by(email=email).first()
        #회원추가
        if user is None:
            user=User(email=email,user_name=user_name)
            print(user)
            db.session.add(user)
            db.session.commit()
        return {"user_id":user.user_id}






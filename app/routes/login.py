from app.models.user import User
from flask import request
from flask_restx import Namespace,Resource
from app.database import db
from app.utils.custom_exception import CustomUserError
Login_api=Namespace('Login_api')

@Login_api.route('/')
class Login(Resource):
    def post(self):
        data = request.get_json()
        email=data['email']
        user_name=data['user_name']
        if len(email)==0 or len(user_name)==0:
            return CustomUserError(error_message="email,user name을 확인해주세요.", status_code=500).to_dict()
        else:
            user=User.query.filter_by(email=email).first()
            #회원추가
            if user is None:
                user=User(email=email,user_name=user_name)
                db.session.add(user)
                db.session.commit()

            # session['user_id']=user.user_id
            return {"user_id":user.user_id}






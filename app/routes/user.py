from app.models.user import User
from app.models.recomended import Recommended
from app.models.daily_nutrition import Daily_nutrition
from flask import request,session,jsonify
from flask_restx import Namespace,Resource
from app.database import db
from app.utils.calculator import calculate_nutrition
from app.utils import validator
from app.utils.custom_exception import CustomUserError
User_api=Namespace('User_api')
@User_api.route('/')
class Profile(Resource):
    """회원정보 수정"""
    def put(self):
        # if 'user_id' not in session:
        #     return CustomUserError(error_message="로그인을 먼저해주세요.", status_code=500).to_dict()

        data=request.get_json()
        user_id = data['user_id']
        validator.is_valid(user_id=user_id)
        user = User.query.filter_by(user_id=user_id).first()
        if user is None:
            return CustomUserError(error_message="회원등록을 먼저 해주세요.", status_code=500).to_dict()

        else:
            check_recommended=Recommended.query.filter_by(user_id=user.user_id).first()
            if check_recommended:
                # recommended 테이블에 데이터 변경

                check_recommended.cal, check_recommended.carbs,check_recommended.protein, fat = calculate_nutrition(data['gender'],
                                                                                                   data['age'],
                                                                                                   data['weight'],
                                                                                                   data['height'],
                                                                                                   data['activity_level'])
                db.session.add(check_recommended)
            else:
                #recommended 테이블에 데이터 추가
                cal,carbs,protein,fat=calculate_nutrition(data['gender'],data['age'],data['weight'],data['height'], data['activity_level'])
                recommended=Recommended(user_id=user.user_id,cal=cal,carbs=carbs,protein=protein,fat=fat)
                db.session.add(recommended)
            # 회원 정보 입력
            user.age = data['age']
            user.gender = data['gender']
            user.height = data['height']
            user.weight = data['weight']
            user.activity_level = data['activity_level']
            db.session.add(user)
            db.session.commit()
            return{
                'message':"success"
            }

@User_api.route('/account')
class Delete_account(Resource):
    def delete(self):
        # if 'user_id' not in session:
        #     return CustomUserError(error_message="로그인을 먼저해주세요.", status_code=500).to_dict()
        user_id=request.args['user_id']
        validator.is_valid("",user_id)
        user=User.query.filter_by(user_id=user_id).first()

        if user is None:
            return CustomUserError(error_message="존재하지 않는 회원입니다.", status_code=500).to_dict()
        else:
            db.session.delete(user)
            db.session.commit()
            return{"message":"success"}

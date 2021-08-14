from app.models.user import User
from app.models.recomended import Recommended
from flask import request
from flask_restx import Namespace,Resource
from app.database import db
User_api=Namespace('User_api')
@User_api.route('/')
class Write_Profile(Resource):

    def post(self):
        data=request.get_json()
        user_id = data['user_id']
        user = User.query.filter_by(user_id=user_id).first()
        if user is None:
            return {"msg":"userID를 확인하세요."}
        else:
            #회원 정보 입력
            user.age = data['age']
            user.gender = data['gender']
            user.height = data['height']
            user.weight = data['weight']
            user.activity_level=data['activity_level']
            db.session.add(user)
            db.session.commit()


            #recommended 테이블에 데이터 추가
            cal,carbs,protein,fat=calculate_nutrition(data['gender'],data['age'],data['weight'],data['height'],data['activity_level'])
            recommended=Recommended(user_id=user.user_id,cal=cal,carbs=carbs,protein=protein,fat=fat)
            db.session.add(recommended)
            db.session.commit()

            return{
                'message':"success"
            }
    def put(self):
        data = request.get_json()
        user_id = data['user_id']
        user = User.query.filter_by(user_id=user_id).first()
        if user is None:
            return {"msg": "회원등록먼저 해주세요"}
        else:
            # 회원 정보 입력
            user.age = data['age']
            user.gender = data['gender']
            user.height = data['height']
            user.weight = data['weight']
            db.session.add(user)
            db.session.commit()

            # recommended 테이블에 데이터 변경
            recommended = Recommended.query.filter_by(user_id=user_id).first()
            recommended.cal, recommended.carbs, recommended.protein, fat = calculate_nutrition(data['gender'], data['age'], data['weight'], data['height'],
                                                           data['activity_level'])
            db.session.add(recommended)
            db.session.commit()

            return {
                'message': "success"
            }

def calculate_nutrition(gender,age,weight,heihgt,activity_level):

    #여성일 경우
    if gender==1:
        #비활동적
        if activity_level==0:
            activity_point=1.0
        #저활동적
        elif activity_level==1:
            activity_point = 1.12
        #활동적
        elif activity_level == 2:
            activity_point = 1.27
        #매우 활동적
        elif activity_level == 3:
            activity_point = 1.45
        height=heihgt*0.01
        cal=354-6.91*age+activity_point*(9.36*weight+726*height)

    elif gender==2:

        # 비활동적
        if activity_level == 0:
            activity_point = 1.0
        # 저활동적
        elif activity_level == 1:
            activity_point = 1.11
        # 활동적
        elif activity_level == 2:
            activity_point = 1.25
        # 매우 활동적
        elif activity_level == 3:
            activity_point = 1.48
        height=heihgt*0.01
        cal = 662 - 9.53 * age + activity_point * (15.91 * weight + 539.6 * height)
    carbs=cal*0.5/4
    protein=cal*0.2/4
    fat=cal*0.3/9
    return cal,carbs,protein,fat
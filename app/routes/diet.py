from app.models.diet import Diet as Diet_obj
from app.models.daily_nutrition import Daily_nutrition
from app.models.recomended import Recommended
from app.models.like import Like
from app.models.user import User
from flask import request,jsonify
from flask_restx import Namespace,Resource
from app.database import db
import datetime
from dateutil.parser import parse
import pandas as pd
import json
from app.utils import validator,search,compare
from app.utils.custom_exception import CustomUserError


Diet_api=Namespace('Diet_api')
@Diet_api.errorhandler(CustomUserError)
def Custom_user_error(e):
    return jsonify(e.to_dict())

@Diet_api.route('/')
class Diet(Resource):
    """개별 식단 조회"""
    def get(self):
        # if 'user_id' not in session:
        #     return jsonify({"message": "로그인을 먼저해주세요"})
        diet_id = request.args.get('diet_id',default=None,type=int)


        diet= Diet_obj.query.filter_by(diet_id=diet_id).first()

        if diet is None:
            return CustomUserError(error_message="식단기록이 존재하지 않습니다.", status_code=500).to_dict()

        return_data={"diet_id":diet.diet_id,"img_path":diet.img_path,"food_info":diet.food_info
                     ,"created_at":str(diet.created_at),"meal":diet.meal,"cal":diet.cal}
        return return_data

    """식단 입력"""
    def post(self):
        # if 'user_id' not in session:
        #     return jsonify({"message":"로그인을 먼저해주세요"})

        # f=request.files['file']
        # f.save(secure_filename(f.filename))
        data=request.get_json()
        user_id=data['user_id']
        ###임의 데이터###
        ###추후에 open api 연결해서 cal, protein,carbs,fat 받아와야함
        created_at=data['created_at']
        meal=data['meal']
        food_names =data['food_list']
        total_cal=0
        total_carbs=0
        total_protein=0
        total_fat=0

        food_info=[]
        ##만약 해당 날짜+ 아점저 기록있으면 이미 작성한 식단입니다라고 해줘야함
        check_is_exist = Diet_obj.query.filter_by(user_id=user_id, created_at=created_at, meal=meal).first()
        if check_is_exist is not None:
            return CustomUserError(error_message="이미 식단 기록이 존재합니다.", status_code=500).to_dict()

        elif check_is_exist is None:
            """영양정보 db에서 음식 검색"""
            for food in food_names:

                food_list = search.search_food(food['name'], "write")

                if not food_list:

                    return CustomUserError(error_message="음식정보가 존재하지 않습니다.", status_code=500).to_dict()

                else:
                    food_info.append(
                        {"no": food_list[0][0], "name": food_list[0][1], "cal": food_list[0][2], "amount": food['amount']})
                    total_cal += food_list[0][2] * food['amount']
                    total_carbs += food_list[0][3] * food['amount']
                    total_protein += food_list[0][4] * food['amount']
                    total_fat += food_list[0][5] * food['amount']

            diet=Diet_obj(user_id=user_id,food_info=food_info,created_at=created_at,meal=meal,img_path="img_path",cal=total_cal)
            dn=Daily_nutrition.query.filter_by(user_id=user_id,created_at=created_at).first()
            if dn is None:
                dn=Daily_nutrition(user_id=user_id,total_cal=total_cal,total_carbs=total_carbs,
                                   total_protein=total_protein,total_fat=total_fat,created_at=created_at)
                db.session.add(dn)

            else:
                dn.total_cal+=total_cal
                dn.total_carbs+=total_carbs
                dn.total_protein+=total_protein
                dn.total_fat+=total_fat
                dn.updated_at=datetime.datetime.now()

            db.session.add(diet)
            db.session.commit()

            return {"diet_id":diet.diet_id}


    """식단수정"""
    def put(self):
        # if 'user_id' not in session:
        #     return CustomUserError(error_message="로그인을 먼저해주세요.", status_code=500).to_dict()
        data=request.get_json()
        user_id=data['user_id']
        diet_id=data['diet_id']
        validator.is_valid(diet_id,user_id)
        food_info=data['food_info']

        diet=Diet_obj.query.filter_by(user_id=user_id,diet_id=diet_id).first()
        if diet is None:
            return CustomUserError(error_message="식단기록이 존재하지 않습니다.", status_code=500).to_dict()
        else:
            old_cal = 0
            old_carbs = 0
            old_protein = 0
            old_fat = 0
            food_list=diet.food_info
            if not food_list:
                pass
            else:
                for food in food_list:
                    no = food['no']
                    nutri_list = search.search_food(no, 'modify')
                    old_cal += nutri_list[0][2]*food['amount']
                    old_carbs += nutri_list[0][3]*food['amount']
                    old_protein += nutri_list[0][4]*food['amount']
                    old_fat += nutri_list[0][5]*food['amount']
            new_cal = 0
            new_carbs = 0
            new_protein = 0
            new_fat = 0

            for food in food_info:
                no = food['no']
                nutri_list = search.search_food(no, 'modify')
                new_cal += nutri_list[0][2]*food['amount']
                new_carbs += nutri_list[0][3]*food['amount']
                new_protein += nutri_list[0][4]*food['amount']
                new_protein += nutri_list[0][5]*food['amount']
            dn = Daily_nutrition.query.filter_by(user_id=user_id, created_at=diet.created_at).first()
            dn.total_cal=dn.total_cal-old_cal+new_cal
            dn.total_carbs=dn.total_carbs-old_carbs+new_carbs
            dn.total_protein = dn.total_protein - old_protein + new_protein
            dn.total_fat = dn.total_fat - old_fat + new_fat

            diet.food_info = food_info
            diet.cal=new_cal
            db.session.commit()

            return jsonify({"message":"식단기록이 수정되었습니다."})

    """개별 식단 삭제"""
    def delete(self):
        # if 'user_id' not in session:
        #     return CustomUserError(error_message="로그인을 먼저해주세요.", status_code=500).to_dict()
        args=request.args
        diet_id=args.get('diet_id')
        user_id=args.get('user_id')
        validator.is_valid(diet_id,user_id)

        diet=Diet_obj.query.filter_by(diet_id=diet_id ,user_id=user_id).first()
        if diet is None:
            return CustomUserError(error_message="해당 식단 기록이 존재하지 않습니다.", status_code=500).to_dict()
        total_cal = 0
        total_carbs = 0
        total_protein = 0
        total_fat = 0
        food_info = diet.food_info
        if not food_info:
            pass
        else:
            for food in food_info:
                no=food['no']
                nutri_list=search.search_food(no,'delete')
                total_cal+=nutri_list[0][2]
                total_carbs+=nutri_list[0][3]
                total_protein+=nutri_list[0][4]
                total_fat+=nutri_list[0][5]
            dn=Daily_nutrition.query.filter_by(user_id=user_id,created_at=diet.created_at).first()
            dn.total_cal-=total_cal
            dn.total_carbs-=total_carbs
            dn.total_protein-=total_protein
            dn.total_fat-=total_fat


        db.session.delete(diet)
        db.session.commit()
        return jsonify({"message":"삭제 되었습니다."})

@Diet_api.route('/search')
class Diet_search(Resource):
    """음식 이름 검색 """
    def get(self):
        # if 'user_id' not in session:
        #     return CustomUserError(error_message="로그인을 먼저해주세요.", status_code=500).to_dict()
        args=request.args
        food_name=args.get('food_name')
        food_info=search.search_food(food_name,'search')
        if not food_info:
            return jsonify({"result":""})
        return jsonify({"result":search.search_food(food_name,'search')})


@Diet_api.route('/list')
class Diet_list(Resource):
    """ 메인화면 (식단 목록 조회) """
    def post(self):
        # if 'user_id' not in session:
        #     return CustomUserError(error_message="로그인을 먼저해주세요.", status_code=500).to_dict()
        data = request.get_json(force=True)
        user_id = data['user_id']
        meal = data['meal']
        created_at = data['created_at']
        if meal==4:
            diet_list = Diet_obj.query.filter_by(user_id=user_id, created_at=created_at)
        else:
            diet_list = Diet_obj.query.filter_by(user_id=user_id, meal=meal, created_at=created_at)

        if len(diet_list.all())==0:
            return CustomUserError(error_message="식단 기록이 존재하지 않습니다.", status_code=500).to_dict()

        else:
            df=pd.read_sql(diet_list.statement,diet_list.session.bind)

            result={"diet_list":(json.loads(df.to_json(orient='records',date_format='iso')))}

        return result



@Diet_api.route('/grape')
class Diet_grape(Resource):
    """영양소 그래프 조회"""
    def post(self):
        # if 'user_id' not in session:
        #     return CustomUserError(error_message="로그인을 먼저해주세요.", status_code=500).to_dict()
        data=request.get_json()
        user_id=data['user_id']
        start_date=parse(data['start_date'])
        end_date=parse(data['end_date'])
        nutritions_list=Daily_nutrition.query.filter_by(user_id=user_id).\
                            filter(Daily_nutrition.created_at >=start_date).filter(Daily_nutrition.created_at<=end_date)
        if len(nutritions_list.all())==0:
            return CustomUserError(error_message="식단 등록을 먼저해주세요",status_code=500).to_dict()
        else:

            df = pd.read_sql(nutritions_list.statement,nutritions_list.session.bind)
            recommended_cal=Recommended.query.filter_by(user_id=user_id).first().cal
            result = {"nutrition_list": (json.loads(df.to_json(orient='records', date_format='iso'))),"recommended_cal":recommended_cal}
            return result

@Diet_api.route('/recommend')
class Diet_grape(Resource):
    """식단 추천"""
    def get(self):
        # if 'user_id' not in session:
        #     return CustomUserError(error_message="로그인을 먼저해주세요.", status_code=500).to_dict()
        args=request.args
        user_id = args.get('user_id')
        validator.is_valid("",user_id)
        diet=Diet_obj.query.filter_by(user_id=user_id).order_by(Diet_obj.created_at.desc()).first()
        if diet is None:
            return CustomUserError(error_message="식단 기록을 먼저 해주세요.", status_code=500).to_dict()

        recommend = Recommended.query.filter_by(user_id=user_id).first()


        today = datetime.date.today()
        yesterday = datetime.date.today() - datetime.timedelta(1)

        recommend_carbs = recommend.carbs
        recommend_protein = recommend.protein
        recommend_fat = recommend.fat
        """ 사용자가 아침때 조회 또는 마지막 기록이 오늘 이나 어제가 아닐때"""
        if diet.meal == 3 or not (diet.created_at == yesterday or diet.created_at == today):
            recommend_carbs = recommend_carbs / 3
            recommend_protein = recommend_protein / 3
            recommend_fat = recommend_fat / 3
            result = search.search_food(purpose='recommend', carbs=recommend_carbs, protein=recommend_protein,
                                        fat=recommend_fat)
            if len(result)>=4:
                result=result[0:3]
            return jsonify({"food_list": result})

        nutritions_list = Daily_nutrition.query.filter_by(user_id=user_id).order_by(Daily_nutrition.created_at.desc()).first()

        last_carbs = nutritions_list.total_carbs
        last_protein =nutritions_list.total_protein
        last_fat = nutritions_list.total_fat

        nutri_list=[]
        """사용자가 점심때 조회"""
        if diet.meal==1:
            nutri_list.append(compare.compareAwithB(recommend_carbs, last_carbs))
            nutri_list.append(compare.compareAwithB(recommend_protein, last_protein))
            nutri_list.append(compare.compareAwithB(recommend_fat, last_fat))
            recommend_carbs = nutri_list[0] / 2
            recommend_protein =nutri_list[1]/ 2
            recommend_fat = nutri_list[2] / 2
            result = search.search_food(purpose='recommend', carbs=recommend_carbs, protein=recommend_protein,
                                        fat=recommend_fat)
            if result==0:
                recommend_carbs = recommend.carbs / 3
                recommend_protein = recommend.protein / 3
                recommend_fat = recommend.fat / 3
                result = search.search_food(purpose='recommend', carbs=recommend_carbs, protein=recommend_protein,
                                            fat=recommend_fat)

            if len(result)>=4:
                result=result[0:3]
            return jsonify({"food_list": result})

        """사용자가 저녁때 조회"""
        if diet.meal==2:
            nutri_list.append(compare.compareAwithB(recommend.carbs, last_carbs))
            nutri_list.append(compare.compareAwithB(recommend.protein, last_protein))
            nutri_list.append(compare.compareAwithB(recommend.fat, last_fat))
            result = search.search_food(purpose='recommend', carbs=nutri_list[0], protein=nutri_list[1],
                                        fat=nutri_list[2])
            if result==0:
                recommend_carbs = recommend.carbs / 3
                recommend_protein = recommend.protein / 3
                recommend_fat = recommend.fat / 3
                result = search.search_food(purpose='recommend', carbs=recommend_carbs, protein=recommend_protein,
                                            fat=recommend_fat)
            if len(result)>=4:
                result=result[0:3]
            return jsonify({"food_list": result})

@Diet_api.route('/recommend/like')
class preference(Resource):
    def get(self):
        # if 'user_id' not in session:
        #     return CustomUserError(error_message="로그인을 먼저해주세요.", status_code=500).to_dict()
        user_id=request.args['user_id']
        no=request.args['no']
        validator.is_valid(user_id=user_id,param=no)
        user=User.query.filter_by(user_id=user_id).first()
        if not user:
            return CustomUserError(error_message="존재하지 않는 회원입니다.", status_code=500).to_dict()
        if search.search_food('like',no=no)==False:
            return CustomUserError(error_message="해당하는 음식명이 존재하지 않습니다.", status_code=500).to_dict()

        like=Like(user_id=user_id,no=no)
        db.session.add(like)
        db.session.commit()
        return {"message":"success"}








        








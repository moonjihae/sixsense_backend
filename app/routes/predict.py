from flask_restx import Namespace,Resource,reqparse
from app.utils import search
from app.utils.custom_exception import CustomUserError
from flask import request,jsonify
from app.s3_connection import s3_connection,get_bucket_name
from datetime import datetime
from app.utils.validator import is_valid
from app.utils.inference import image_preprocessing,load_model
import cv2
import numpy as np
from app.utils.class_info import class_name
Predict_api=Namespace('Predict_api')
@Predict_api.route('')
class Predict(Resource):
    def post(self):
        args=request.form
        image_file = request.files['file']
        user_id=args['user_id']
        is_valid(user_id=user_id,param=image_file)

        image=image_file.read()
        image=cv2.imdecode(np.fromstring(image,dtype=np.uint8),cv2.IMREAD_COLOR)
        origin_image,input=image_preprocessing(image,(416,416))
        predicted_result,predicted_img=load_model(origin_image,input)
        if predicted_result is None:
            return jsonify({""})
        else:
            """이미지 s3에 저장"""
            predicted_img= cv2.imencode('.png', predicted_img)[1].tostring()

            s3=s3_connection()
            s3_path=f'{user_id}_{datetime.now()}'
            s3.put_object(
                Bucket=get_bucket_name(),
                Body=predicted_img,
                Key=s3_path,
                ContentType=image_file.content_type
            )
            location = s3.get_bucket_location(Bucket=get_bucket_name())['LocationConstraint']
            image_url = f'https://{get_bucket_name()}.s3.{location}.amazonaws.com/{s3_path}'

            food_info=[]

            for food in predicted_result:
                food_list = search.search_food(food['name'],"write")
                food_info.append(
                    {"no": food_list[0][0], "name": food_list[0][1], "cal": food_list[0][2], "amount": 1})

            if not food_info:
                return CustomUserError(error_message="사진을 다시 찍어주세요.", status_code=500).to_dict()
            else:

                return jsonify({"food":food_info,"img_url":image_url})



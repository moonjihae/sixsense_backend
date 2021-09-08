from app.models.user import User
from flask import request,session
from flask_restx import Namespace,Resource,reqparse
from app.database import db
from app.utils.custom_exception import CustomUserError
from flask import request,jsonify
from app.s3_connection import s3_connection,get_bucket_name
from datetime import datetime
Predict_api=Namespace('Predict_api')
@Predict_api.route('')
class Predict(Resource):
    def post(self):
        # parse = reqparse.RequestParser()
        # parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        # args = parse.parse_args()
        args=request.form
        image_file = request.files['file']
        user_id=args['user_id']
        s3=s3_connection()
        s3_path=f'{user_id}_{datetime.now()}'
        s3.put_object(
            Bucket=get_bucket_name(),
            Body=image_file,
            Key=s3_path,
            ContentType=image_file.content_type
        )
        location = s3.get_bucket_location(Bucket=get_bucket_name())['LocationConstraint']
        image_url = f'https://{get_bucket_name()}.s3.{location}.amazonaws.com/{s3_path}'
        return jsonify({"image_url":image_url})



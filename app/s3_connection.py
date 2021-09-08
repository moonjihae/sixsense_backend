import boto3
from app.config import AWS_SECRET_KEY,AWS_ACCESS_KEY,BUCKET_NAME
def get_bucket_name():
    return BUCKET_NAME

def s3_connection():
    try:

        s3=boto3.client('s3',aws_access_key_id=AWS_ACCESS_KEY,
                        aws_secret_access_key=AWS_SECRET_KEY)
    except Exception as e:
        print(e)
        exit()
    else:
        return s3
from app.database import db
from datetime import datetime

class User(db.Model):
    __tablename__='User'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    user_id = db.Column(db.Integer, primary_key=True, unique=True,autoincrement=True)
    user_name = db.Column(db.String(30))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    age=db.Column(db.Integer)
    gender=db.Column(db.Integer)
    activity_level=db.Column(db.Integer)
    email=db.Column(db.String(30))
    recommended = db.relationship("Recommended", uselist=False, backref="user")
    diets=db.relationship('Diet',backref='user')

    def __init__(self,  user_name, email):

        self.user_name = user_name
        self.email=email


    def __repr__(self):
        return 'user_id : %s, user_name : %s, profile_url : %s' % (self.user_id, self.user_name, self.profile_url)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}


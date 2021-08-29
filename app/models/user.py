from app.database import db

class User(db.Model):
    __tablename__='user'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    user_id = db.Column(db.Integer, primary_key=True, unique=True,autoincrement=True)
    user_name = db.Column(db.String(30))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    age=db.Column(db.Integer)
    gender=db.Column(db.Integer)
    activity_level=db.Column(db.Integer)
    email=db.Column(db.String(30))
    recommended = db.relationship("Recommended", cascade="delete, merge, save-update", backref="user")
    diets=db.relationship('Diet',backref='user',cascade="delete, merge, save-update")
    daily_nutrition=db.relationship('Daily_nutrition',backref='user',cascade="delete, merge, save-update")
    like=db.relationship('Like',backref='user',cascade="delete, merge, save-update")


    def __init__(self,  user_name, email):

        self.user_name = user_name
        self.email=email


    def __repr__(self):
        return f'user_id : {self.user_id}, user_name :{self.user_name}'

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}

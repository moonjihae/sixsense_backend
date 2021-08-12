from app.database import db
from datetime import datetime

class Diet(db.Model):
    __tablename__='Diet'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    diet_id = db.Column(db.Integer, primary_key=True, unique=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('User.user_id'),nullable=False)
    meal = db.Column(db.Integer)
    created_at = db.Column(db.DATETIME)
    food_info=db.Column(db.JSON)
    cal=db.Column(db.Integer)
    img_path=db.Column(db.String(320))


    def __init__(self,user_id,meal,food_info,cal):
        self.user_id = user_id

        self.cal=cal
        self.meal=meal
        self.food_info=food_info
        self.created_at=datetime.now()

    def __repr__(self):
        return 'diet_id : %s, user_id : %s' % (self.diet_id, self.user_id)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}


from app.database import db

class Recommended(db.Model):
    __tablename__='recommended'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    rec_id = db.Column(db.Integer, primary_key=True, unique=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False,unique=True)
    cal = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fat=db.Column(db.Float)
    protein=db.Column(db.Float)


    def __init__(self,user_id, cal,carbs,fat,protein):
        self.user_id = user_id

        self.cal=cal
        self.carbs=carbs
        self.fat=fat
        self.protein=protein

    def __repr__(self):
        return 'rec_id : %s, user_id : %s' % (self.rec_id, self.user_id)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}


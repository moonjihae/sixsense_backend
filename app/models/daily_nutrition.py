from app.database import db
from datetime import date,datetime

class Daily_nutrition(db.Model):
    __tablename__='daily_nutrition'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    dn_id = db.Column(db.Integer, primary_key=True, unique=True,autoincrement=True)
    """다대다 관계"""
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False)
    total_cal = db.Column(db.Float)
    total_carbs = db.Column(db.Float)
    total_protein=db.Column(db.Float)
    total_fat=db.Column(db.Float)
    created_at = db.Column(db.DATETIME)
    updated_at = db.Column(db.DATETIME)

    def __init__(self,user_id,total_cal,total_carbs,total_protein,total_fat,created_at):
        self.user_id = user_id
        self.total_cal=total_cal
        self.total_carbs=total_carbs
        self.total_protein=total_protein
        self.total_fat=total_fat
        self.created_at=created_at
        self.updated_at=datetime.now()

    def __repr__(self):
        return f'dn_id : {self.dn_id}, total_cal :{self.total_cal},total_carbs :{self.total_carbs},total_protein :{self.total_protein},total_fat : {self.total_fat},'

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}



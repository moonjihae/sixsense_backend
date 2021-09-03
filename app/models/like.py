from app.database import db

class Like(db.Model):
    __tablename__='like'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    like_id = db.Column(db.Integer, primary_key=True, unique=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False)
    no = db.Column(db.Integer)

    def __init__(self,user_id,no):
        self.user_id = user_id
        self.no=no

    def __repr__(self):
        return f' like_id :  {self.like_id}, user_id:{self.user_id}, no:{self.no}'

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}
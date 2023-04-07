from config import db, ma


class DongleReceptorBase(db.Model):
    __abstract__ = True
    __tablename__ = "Dongle_Receptor"
    Id = db.Column(db.Integer, primary_key=True, nullable=False)
    Name = db.Column(db.String, unique=True, nullable=False)


    def serialize(self):
            return{
                'Id': self.Id,
                'Name': self.Name,
            }
    
class DongleReceptor(DongleReceptorBase):
    pass

class DongleReceptorAux(DongleReceptorBase):
    __bind_key__ = 'auxDB'
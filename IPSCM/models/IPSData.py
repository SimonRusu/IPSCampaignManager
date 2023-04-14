from config import db, ma
from sqlalchemy.ext.declarative import declared_attr

class IPSMethods(db.Model):
    __tablename__ = "IPS_Data"
    Id = db.Column(db.Integer, nullable=False, primary_key=True)

''' @declared_attr
    def Id_campaign(cls):
         return db.Column(db.Integer, db.ForeignKey('Campaign.Id'), nullable=False)
    
    @declared_attr
    def Id_IPS_data(cls):
         return db.Column(db.Integer, db.ForeignKey('IPS_Data.Id'), nullable=False)
    
    Method = db.Column(db.String, nullable=False)

def serialize(self):
        return{
            'Id': self.Id,
            'Id_campaign': self.Id_campaign,
            'Id_IPS_data': self.Id_IPS_data,
            'Method': self.Method
        }
'''
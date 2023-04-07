from config import db, ma
from sqlalchemy.ext.declarative import declared_attr

class BeaconConfigurationBase(db.Model):
    __abstract__ = True
    __tablename__ = "Beacon_Configuration"
    Id = db.Column(db.Integer, nullable=False, primary_key=True)
    Mac = db.Column(db.VARCHAR(50), nullable=False)
    Power = db.Column(db.Integer)
    Calibrated_power = db.Column(db.Integer)
    Update_frequency = db.Column(db.Integer)
    Identificator = db.Column(db.VARCHAR(32))


    
class BeaconConfiguration(BeaconConfigurationBase):
    @declared_attr
    def Id_campaign(cls):
         return db.Column(db.Integer, db.ForeignKey('Campaign.Id'), nullable=False)
    
    def serialize(self):
        return{
            'Id': self.Id,
            'Id_campaign': self.Id_campaign,
            'Mac': self.Mac,
            'Power': self.Power,
            'Calibrated_power': self.Calibrated_power,
            'Update_frequency': self.Update_frequency,
            'Identificator': self.Identificator
        }

class BeaconConfigurationAux(BeaconConfigurationBase):
    __bind_key__ = 'auxDB'

    def serialize(self):
        return{
            'Id': self.Id,
            'Mac': self.Mac,
            'Power': self.Power,
            'Calibrated_power': self.Calibrated_power,
            'Update_frequency': self.Update_frequency,
            'Identificator': self.Identificator
        }
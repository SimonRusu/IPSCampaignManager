from config import db, ma

class BeaconConfigurationBase(db.Model):
    __abstract__ = True
    __tablename__ = "Beacon_Configuration"
    Id = db.Column(db.Integer, nullable=False, primary_key=True)
    Mac = db.Column(db.VARCHAR(50), nullable=False)
    Power = db.Column(db.Integer)
    Calibrated_power = db.Column(db.Integer)
    Update_frequency = db.Column(db.Integer)
    Identificator = db.Column(db.VARCHAR(32))

    def serialize(self):
        return{
            'Id': self.Id,
            'Mac': self.Mac,
            'Power': self.Power,
            'Calibrated_power': self.Calibrated_power,
            'Update_frequency': self.Update_frequency,
            'Identificator': self.Identificator
        }

class BeaconConfiguration(BeaconConfigurationBase):
    pass


class BeaconConfigurationAux(BeaconConfigurationBase):
    __bind_key__ = 'auxDB'

from config import db, ma
from sqlalchemy.ext.declarative import declared_attr

class MethodPredata(db.Model):
    __tablename__ = "Method_Predata"
    Id = db.Column(db.Integer, nullable=False, primary_key=True)

    @declared_attr
    def Id_campaign(cls):
         return db.Column(db.Integer, db.ForeignKey('Campaign.Id'), nullable=False)
    
    Channel = db.Column(db.VARCHAR(50), nullable=False)
    Mac = db.Column(db.VARCHAR(50), nullable=False)
    Dongle_rotation = db.Column(db.REAL, nullable=False)
    Protocol = db.Column(db.VARCHAR(50), nullable=False)
    RSSI = db.Column(db.Integer, nullable=False)
    Position_x = db.Column(db.REAL, nullable=False)
    Position_y = db.Column(db.REAL, nullable=False)
    Position_z = db.Column(db.REAL, nullable=False)

def serialize(self):
        return{
            'Id': self.Id,
            'Id_campaign': self.Id_campaign,
            'Channel': self.Channel,
            'Mac': self.Mac,
            'Dongle_rotation': self.Dongle_rotation,
            'Protocol': self.Protocol,
            'RSSI': self.RSSI,
            'Position_x': self.Position_x,
            'Position_y': self.Position_y,
            'Position_z': self.Position_z
        }

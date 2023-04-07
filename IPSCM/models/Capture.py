from config import db, ma
from sqlalchemy.ext.declarative import declared_attr

class CaptureBase(db.Model):
    __abstract__ = True
    __tablename__ = "Capture"
    Id = db.Column(db.Integer, nullable=False, primary_key=True)
    

    Date = db.Column(db.DateTime,nullable=False)
    Light = db.Column(db.REAL, nullable=False)
    Temperature = db.Column(db.REAL, nullable=False)
    Relative_humidity = db.Column(db.REAL, nullable=False)
    Absolute_humidity = db.Column(db.REAL, nullable=False)
    Position_x = db.Column(db.REAL, nullable=False)
    Position_y = db.Column(db.REAL, nullable=False)
    Position_z = db.Column(db.REAL, nullable=False)
    Platform_angle = db.Column(db.REAL, nullable=False)
    Dongle_rotation = db.Column(db.REAL, nullable=False)

    
class Capture(CaptureBase):
    @declared_attr
    def Id_campaign(cls):
         return db.Column(db.Integer, db.ForeignKey('Campaign.Id'), nullable=False)
    
    def serialize(self):
        return{
            'Id': self.Id,
            'Id_campaign': self.Id_campaign,
            'Date': self.Date,
            'Light': self.Light,
            'Temperature': self.Temperature,
            'Relative_humidity': self.Relative_humidity,
            'Absolute_humidity': self.Absolute_humidity,
            'Position_x': self.Position_x,
            'Position_y': self.Position_y,
            'Position_z': self.Position_z,
            'Platform_angle': self.Platform_angle,
            'Dongle_rotation': self.Dongle_rotation,
        }

class CaptureAux(CaptureBase):
    __bind_key__ = 'auxDB'

    def serialize(self):
        return{
            'Id': self.Id,
            'Date': self.Date,
            'Light': self.Light,
            'Temperature': self.Temperature,
            'Relative_humidity': self.Relative_humidity,
            'Absolute_humidity': self.Absolute_humidity,
            'Position_x': self.Position_x,
            'Position_y': self.Position_y,
            'Position_z': self.Position_z,
            'Platform_angle': self.Platform_angle,
            'Dongle_rotation': self.Dongle_rotation,
        }

from config import db, ma
from sqlalchemy.ext.declarative import declared_attr

class IPSMethods(db.Model):
    __tablename__ = "Method_Prediction"
    Id = db.Column(db.Integer, nullable=False, primary_key=True)

    @declared_attr
    def Id_campaign(cls):
         return db.Column(db.Integer, db.ForeignKey('Campaign.Id'), nullable=False)
    
    Method = db.Column(db.VARCHAR(50), nullable=False)
    Protocol = db.Column(db.VARCHAR(50), nullable=False)
    Channel = db.Column(db.VARCHAR(50), nullable=False),
    RSSI = db.Column(db.Integer, nullable=False),
    RSSI_samples = db.Column(db.Integer, nullable=False),
    K = db.Column(db.Integer, nullable=False)
    Predicted_x = db.Column(db.REAL, nullable=False)
    Predicted_y = db.Column(db.REAL, nullable=False)
    Predicted_z = db.Column(db.REAL, nullable=False)

def serialize(self):
        return{
            'Id': self.Id,
            'Id_campaign': self.Id_campaign,
            'Method': self.Method,
            'Protocol': self.Protocol,
            'Channel': self.Channel,
            'RSSI': self.RSSI,
            'RSSI_samples': self.RSSI_samples,
            'K': self.K,
            'Predicted_x': self.Predicted_x,
            'Predicted_y': self.Predicted_y,
            'Predicted_z': self.Predicted_z
        }
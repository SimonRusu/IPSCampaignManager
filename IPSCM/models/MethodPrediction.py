from sqlalchemy import Text
from config import db
from sqlalchemy.ext.declarative import declared_attr

class MethodPrediction(db.Model):
    __tablename__ = "Method_Prediction"
    Id = db.Column(db.Integer, nullable=False, primary_key=True)

    @declared_attr
    def Id_campaign(cls):
         return db.Column(db.Integer, db.ForeignKey('Campaign.Id'), nullable=False)
    
    Method = db.Column(db.VARCHAR(50), nullable=False)
    Protocol = db.Column(db.VARCHAR(50), nullable=False)
    Channel = db.Column(db.VARCHAR(50), nullable=False)
    RSSI_samples = db.Column(db.Integer, nullable=False)
    Ks_range  = db.Column(db.String(10), nullable=False)
    Predicted_points = db.Column(Text, nullable=False)
    Mean_error = db.Column(Text, nullable=False)

    def serialize(self):
            return{
                'Id': self.Id,
                'Id_campaign': self.Id_campaign,
                'Method': self.Method,
                'Protocol': self.Protocol,
                'Channel': self.Channel,
                'RSSI_samples': self.RSSI_samples,
                'Ks_range': self.Ks_range,
                'Predicted_points': self.Predicted_points
            }
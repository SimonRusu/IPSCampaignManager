from sqlalchemy import Text
from config import db
from sqlalchemy.ext.declarative import declared_attr

class MethodPrediction(db.Model):
    __tablename__ = "Method_Prediction"
    Id = db.Column(db.Integer, nullable=False, primary_key=True)

    @declared_attr
    def Id_campaign(cls):
         return db.Column(db.Integer, db.ForeignKey('Campaign.Id'), nullable=False)
    
    Method_description = db.Column(Text, nullable=False)
    Predicted_points = db.Column(Text, nullable=False)
    Mean_error = db.Column(Text, nullable=False)

    def serialize(self):
            return{
                'Id': self.Id,
                'Id_campaign': self.Id_campaign,
                'Method_description': self.Method_description,
                'Predicted_points': self.Predicted_points,
                'Mean_error': self.Mean_error
            }
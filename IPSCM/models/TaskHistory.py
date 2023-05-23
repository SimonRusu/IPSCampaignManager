from sqlalchemy import Text
from config import db
from sqlalchemy.ext.declarative import declared_attr

class TaskHistory(db.Model):
    __tablename__ = "Task_History"
    Id = db.Column(db.Integer, nullable=False, primary_key=True)

    @declared_attr
    def Id_campaign(cls):
         return db.Column(db.Integer, db.ForeignKey('Campaign.Id'), nullable=False)
    
    Status = db.Column(db.VARCHAR(50), nullable=False)
    Task_description = db.Column(Text, nullable=False)
    Datetime_start = db.Column(db.db.DateTime, nullable=False)
    Datetime_end = db.Column(db.db.DateTime)
    
    def serialize(self):
            return{
                'Id': self.Id,
                'Id_campaign': self.Id_campaign,
                'Status': self.Status,
                'Task_description': self.Task_description,
                'Datetime_start': self.Datetime_start,
                'Datetime_end': self.Datetime_end
            }
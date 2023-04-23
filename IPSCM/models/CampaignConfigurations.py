from config import db, ma
from sqlalchemy.ext.declarative import declared_attr

class CampaignConfigurations(db.Model):
    __tablename__ = "Campaign_Configurations"
    Id = db.Column(db.Integer, primary_key=True, nullable=False)

    @declared_attr
    def Id_campaign(cls):
         return db.Column(db.Integer, db.ForeignKey('Campaign.Id'), nullable=True)
    
    @declared_attr
    def Id_beacon_configuration(cls):
         return db.Column(db.Integer, db.ForeignKey('Beacon_Configuration.Id'), nullable=True)
    
    Name = db.Column(db.String(32), nullable=False)

    def serialize(self):
            return{
                'Id': self.Id,
                'Id_campaign': self.Id_campaign,
                'Id_beacon_configuration': self.Id_beacon_configuration,
                'Name': self.Name
            }
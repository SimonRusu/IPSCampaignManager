from datetime import datetime
from config import db, ma
from sqlalchemy.ext.declarative import declared_attr


class Campaign(db.Model):
    __tablename__ = "Campaign"
    Id = db.Column(db.Integer, nullable=False, primary_key=True)

    @declared_attr
    def Id_related_campaign(cls):
         return db.Column(db.Integer, db.ForeignKey('Campaign.Id'), nullable=True)

    @declared_attr
    def Id_dongle(cls):
         return db.Column(db.Integer, db.ForeignKey('Dongle_Receptor.Id'), nullable=False)
    
    @declared_attr
    def Id_campaign_sequence(cls):
         return db.Column(db.Integer, db.ForeignKey('Campaign_Sequence.Id'), nullable=False)

    Name = db.Column(db.String(32), nullable=False)
    Description = db.Column(db.String(500))
    Date = db.Column(db.DateTime, nullable=False)
    Images_ref = db.Column(db.String(50))
    Manufacturer = db.Column(db.String(50))
    Chipset = db.Column(db.String(50))
    Bluetooth_protocol = db.Column(db.String(50))


    def serialize(self):
        return {
            'Id': self.Id,
            'Id_related_campaign': self.Id_related_campaign, 
            'Id_dongle': self.Id_dongle,
            'Id_campaign_sequence': self.Id_campaign_sequence,
            'Name': self.Name,
            'Description': self.Description,
            'Date': self.Date,
            'Images_ref': self.Images_ref,
            'Manufacturer': self.Manufacturer,
            'Chipset': self.Chipset,
            'Bluetooth_protocol': self.Bluetooth_protocol,
            
        }
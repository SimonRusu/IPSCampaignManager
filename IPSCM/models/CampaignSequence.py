from config import db
    
    
class CampaignSequence(db.Model):
    __tablename__ = "Campaign_Sequence"

    Id = db.Column(db.Integer, nullable=False, primary_key=True)
    Dongle_receptor = db.Column(db.Integer, nullable=False)
    Beacon_configuration = db.Column(db.Integer, nullable=False)
    Capture = db.Column(db.Integer, nullable=False)
    Beacon_BLE_Signal = db.Column(db.Integer, nullable=False)
    
    def serialize(self):
            return{
                'Id': self.Id,
                'Dongle_receptor': self.Dongle_receptor,
                'Beacon_configuration': self.Beacon_configuration,
                'Capture': self.Capture,
                'Beacon_BLE_Signal': self.Beacon_BLE_Signal
            }

class CampaignSequenceAux(db.Model):
    __tablename__ = "sqlite_sequence"
    __bind_key__ = 'auxDB'

    Name = db.Column(db.VARCHAR(50), primary_key=True, nullable=False)
    Seq = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return{
            'Name': self.Name,
            'Seq': self.Seq
        }

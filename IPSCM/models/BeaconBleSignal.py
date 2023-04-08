from config import db, ma
from sqlalchemy.ext.declarative import declared_attr


class BeaconBleSignalBase(db.Model):
    __abstract__ = True
    __tablename__ = "Beacon_BLE_Signal"
    Id = db.Column(db.Integer, nullable=False, primary_key=True)

    @declared_attr
    def Id_capture(cls):
         return db.Column(db.Integer, db.ForeignKey('Capture.Id'), nullable=False)

    N_reading = db.Column(db.Integer, nullable=False)
    Date_hour = db.Column(db.VARCHAR(50), nullable=False)
    Mac = db.Column(db.VARCHAR(50), nullable=False)
    Pack_size = db.Column(db.Integer, nullable=False)
    Channel = db.Column(db.Integer, nullable=False)
    RSSI = db.Column(db.Integer, nullable=False)
    PDU_type = db.Column(db.VARCHAR(50), nullable=False)
    CRC = db.Column(db.VARCHAR(50), nullable=False)
    Protocol = db.Column(db.VARCHAR(50), nullable=False)
    Identificator = db.Column(db.VARCHAR(32), nullable=False)


    def serialize(self):
            return{
                'Id': self.Id,
                'Id_capture': self.Id_capture,
                'N_reading': self.N_reading,
                'Date_hour': self.Date_hour,
                'Mac': self.Mac,
                'Pack_size': self.Pack_size,
                'Channel': self.Channel,
                'RSSI': self.RSSI,
                'PDU_type': self.PDU_type,
                'CRC': self.CRC,
                'Protocol': self.Protocol,
                'Identificator': self.Identificator
            }
    
class BeaconBleSignal(BeaconBleSignalBase):
    pass

class BeaconBleSignalAux(BeaconBleSignalBase):
    __bind_key__ = 'auxDB'
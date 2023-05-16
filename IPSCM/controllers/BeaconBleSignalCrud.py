from flask import jsonify
from controllers.CaptureCrud import getCaptureIdsByCampaignId
from models.BeaconBleSignal import BeaconBleSignal, BeaconBleSignalAux
from models.Capture import Capture
from config import db

def createBeaconBleSignal():
    db.create_all()
    beaconBleSignalAux = BeaconBleSignalAux.query.all()
    captureIndex = Capture.query.count()

    for i in beaconBleSignalAux:
        beaconBleSignal = BeaconBleSignal()
        beaconBleSignal.Id_capture = i.Id_capture + captureIndex
        beaconBleSignal.N_reading = i.N_reading
        beaconBleSignal.Date_hour = i.Date_hour
        beaconBleSignal.Mac = i.Mac
        beaconBleSignal.Pack_size = i.Pack_size
        beaconBleSignal.Channel = i.Channel
        beaconBleSignal.RSSI = i.RSSI
        beaconBleSignal.PDU_type = i.PDU_type
        beaconBleSignal.CRC = i.CRC
        beaconBleSignal.Protocol = i.Protocol
        beaconBleSignal.Identificator = i.Identificator
        db.session.add(beaconBleSignal)
    
    db.session.commit()
    db.session.remove()


def getBeaconBleSignalByCampaignId(campaignId:int):
    captureIds = getCaptureIdsByCampaignId(campaignId)
    return jsonify([signal.serialize() for signal in BeaconBleSignal.query.filter(BeaconBleSignal.Id_capture.in_(captureIds))])

def getBeaconBleSignalIdentificatorByCampaignId(campaignId:int):
    captureIds = getCaptureIdsByCampaignId(campaignId)
    beaconBleSignals = BeaconBleSignal.query.filter(BeaconBleSignal.Id_capture.in_(captureIds)).all()
    return list(set(signal.Identificator for signal in beaconBleSignals))

def getBeaconBleSignalByIdChannelMacAndProtocol(id, channel, mac, protocol):
    return BeaconBleSignal.query.filter(
        BeaconBleSignal.Id_capture == id,
        BeaconBleSignal.Channel == channel,
        BeaconBleSignal.Mac.in_(mac),
        BeaconBleSignal.Protocol == protocol,
    ).all()

def getBeaconBleSignalById(id):
    return BeaconBleSignal.query.filter(
        BeaconBleSignal.Id_capture == id
    ).all()

def getBeaconBleSignalsByCaptureIds(captureIds):
    return BeaconBleSignal.query.filter(BeaconBleSignal.Id_capture.in_(captureIds)).all()


def deleteBeaconBleSignalByCampaignId(campaignId:int):
    captureIds = getCaptureIdsByCampaignId(campaignId)
    BeaconBleSignal.query.filter(BeaconBleSignal.Id_capture.in_(captureIds)).delete()
    db.session.commit()



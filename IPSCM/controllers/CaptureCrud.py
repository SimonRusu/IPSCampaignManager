from flask import jsonify
from models.Capture import Capture,CaptureAux
from models.Campaign import Campaign
from config import db
from sqlalchemy import desc
from sqlalchemy import func

def createCapture():
    db.create_all()
    captureAux = CaptureAux.query.all()
    campaignId = Campaign().query.order_by(desc(Campaign.Id)).first().Id

    for i in captureAux:
        capture = Capture()
        capture.Id_campaign = campaignId
        capture.Date = i.Date
        capture.Light = i.Light
        capture.Temperature = i.Temperature
        capture.Relative_humidity = i.Relative_humidity
        capture.Absolute_humidity = i.Absolute_humidity
        capture.Position_x = i.Position_x
        capture.Position_y = i.Position_y
        capture.Position_z = i.Position_z
        capture.Platform_angle = i.Platform_angle
        capture.Dongle_rotation = i.Dongle_rotation
        db.session.add(capture)
    
    db.session.commit()
    db.session.remove()


def getCaptureIdsByCampaignId(campaignId):
    return [capture.Id for capture in Capture.query.filter_by(Id_campaign=campaignId).all()]

def getCapturesByCampaignId(campaignId):
    return jsonify([capture.serialize() for capture in Capture.query.filter_by(Id_campaign=campaignId).all()])

def getCapturesByIdAndRotation(id):
    return Capture.query.filter(
        Capture.Id.in_(id)
    ).all()

def deleteCaptureByCampaignId(campaignId):
    existingCapture = Capture().query.filter_by(Id_campaign=campaignId).delete()

    if existingCapture:
        db.session.commit()
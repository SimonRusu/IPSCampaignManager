from flask import jsonify
from datetime import datetime
from config import db
from controllers.BeaconBleSignalCrud import deleteBeaconBleSignalByCampaignId
from models.DongleReceptor import DongleReceptor, DongleReceptorAux
from models.Campaign import Campaign
from models.CampaignSequence import CampaignSequence
from controllers.CampaignSequenceCrud import deleteCampaignSequenceByCampaignId
from controllers.CaptureCrud import deleteCaptureByCampaignId
from sqlalchemy import desc
from services.ImageService import deleteZipImages, sendZipImages
from models.MethodPredata import MethodPredata

def createMethodPredataBatch(batch_data):
    db.create_all()

    methodPredata_objects = [
        MethodPredata(
            Id_campaign=campaignId,
            Channel=channel,
            Mac=mac,
            Dongle_rotation=rotation,
            Protocol=protocol,
            RSSI=rssi,
            Position_x=positionX,
            Position_y=positionY,
            Position_z=positionZ
        )
        for campaignId, channel, mac, rotation, protocol, rssi, positionX, positionY, positionZ in batch_data
    ]

    db.session.bulk_save_objects(methodPredata_objects)
    db.session.commit()


def getCampaigns():
    campaigns = Campaign.query.filter(Campaign.Id_related_campaign != None).all()
    return jsonify([campaign.serialize() for campaign in campaigns])

def getRelatedCampaignById(relatedCampaignId):
    campaign = Campaign.query.filter_by(Id=relatedCampaignId).first()
    return jsonify(campaign.serialize())

def getCampaignImagesById(campaignId):
    campaign = Campaign.query.filter_by(Id=campaignId).first()

    if campaign.Images_ref is None:
        return {'message': 'Campaign has no image'}, 404

    response = sendZipImages(campaign.Images_ref)
    return response

def deleteCampaignById(campaignId):
    campaign = Campaign().query.filter_by(Id=campaignId).first()
    relatedCampaign = Campaign().query.filter_by(Id=campaign.Id_related_campaign).first()

    if campaign:
        deleteCampaignSequenceByCampaignId(campaignId)
        deleteCampaignSequenceByCampaignId(relatedCampaign.Id)

        deleteBeaconBleSignalByCampaignId(campaignId)
        deleteBeaconBleSignalByCampaignId(relatedCampaign.Id)

        deleteCaptureByCampaignId(campaignId)
        deleteCaptureByCampaignId(relatedCampaign.Id)

        if campaign.Images_ref is not None:
            deleteZipImages(campaign.Images_ref)

        db.session.delete(campaign)
        db.session.delete(relatedCampaign)
        db.session.commit()

        return {'message': 'Campaign successfully deleted'}, 200
    else:
        return {'message', 'Campaign not found'}, 404
    
def getLastInsertedCampaignId():
    return Campaign.query.order_by(Campaign.Id.desc()).first().Id
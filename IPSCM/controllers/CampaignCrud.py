from flask import jsonify
from datetime import datetime
from config import db
from controllers.BeaconBleSignalCrud import deleteBeaconBleSignalByCampaignId
from controllers.BeaconConfigurationCrud import deleteBeaconConfigurationByCampaignId
from models.DongleReceptor import DongleReceptor, DongleReceptorAux
from models.Campaign import Campaign
from models.CampaignSequence import CampaignSequence
from controllers.CampaignSequenceCrud import deleteCampaignSequenceByCampaignId
from controllers.CaptureCrud import deleteCaptureByCampaignId
from sqlalchemy import desc
from services.ImageService import deleteZipImages, sendZipImages


def createCampaign(name, date, description, images, relatedCampaignId):
    db.create_all()
    auxDongleName = DongleReceptorAux().query.first().Name
    dongleId = DongleReceptor().query.filter_by(Name=auxDongleName).first().Id
    campaignSequenceId = CampaignSequence().query.order_by(desc(CampaignSequence.Id)).first().Id
    formattedDate = datetime.strptime(date, '%Y-%m-%d').date()
    
    campaign = Campaign()
    campaign.Id_related_campaign = relatedCampaignId
    campaign.Id_dongle = dongleId
    campaign.Id_campaign_sequence = campaignSequenceId
    campaign.Name = name
    campaign.Description = description
    campaign.Date = formattedDate
    campaign.Images_ref = images

    db.session.add(campaign)

    db.session.commit()
    db.session.remove()


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
    existingCampaign = Campaign().query.filter_by(Id=campaignId).first()

    if existingCampaign:
        deleteCampaignSequenceByCampaignId(campaignId)
        deleteBeaconConfigurationByCampaignId(campaignId)
        deleteBeaconBleSignalByCampaignId(campaignId)
        deleteCaptureByCampaignId(campaignId)
        if existingCampaign.Images_ref is not None:
            deleteZipImages(existingCampaign.Images_ref)

        db.session.delete(existingCampaign)
        db.session.commit()

        return {'message': 'Campaign successfully deleted'}, 200
    else:
        return {'message', 'Campaign not found'}, 404
    
def getLastInsertedCampaignId():
    return Campaign.query.order_by(Campaign.Id.desc()).first().Id
import mimetypes
import os
from flask import jsonify, send_file
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
import zipfile


def createCampaign(name, date, description, images):
    db.create_all()
    auxDongleName = DongleReceptorAux().query.first().Name
    dongleId = DongleReceptor().query.filter_by(Name=auxDongleName).first().Id
    campaignSequenceId = CampaignSequence().query.order_by(desc(CampaignSequence.Id)).first().Id
    formattedDate = datetime.strptime(date, '%Y-%m-%d').date()
    
    campaign = Campaign()
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
    campaigns = Campaign.query.all()
    return jsonify([campaign.serialize() for campaign in campaigns])


def getCampaignImagesById(campaignId):
    campaign = Campaign.query.filter_by(Id=campaignId).first()
    images_directory = 'db/campaign_images/'
    image_directory = images_directory + campaign.Images_ref
    image_names = os.listdir(image_directory)
    if campaign.Images_ref is None:
        return {'message': 'Campaign has no image'}, 404
    

    zip_filename = f"{campaign.Images_ref}.zip"
    with zipfile.ZipFile(zip_filename, "w") as zip:
        for image_name in image_names:
            image_path = os.path.join(image_directory, image_name)
            zip.write(image_path, arcname=image_name)

    return send_file(
        zip_filename,
        mimetype='application/zip',
        as_attachment=True,
        download_name=zip_filename
    )




def deleteCampaignById(campaignId):
    existingCampaign = Campaign().query.filter_by(Id=campaignId).first()

    if existingCampaign:
        deleteCampaignSequenceByCampaignId(campaignId)
        deleteBeaconConfigurationByCampaignId(campaignId)
        deleteBeaconBleSignalByCampaignId(campaignId)
        deleteCaptureByCampaignId(campaignId)
        db.session.delete(existingCampaign)
        db.session.commit()

        return {'message': 'Campaign successfully deleted'}, 200
    else:
        return {'message', 'Campaign not found'}, 404
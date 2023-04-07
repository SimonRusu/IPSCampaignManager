import mimetypes
import os
from flask import jsonify, send_from_directory
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


def createCampaign(name, date, description, image):
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
    campaign.Image_ref = image
    db.session.add(campaign)

    db.session.commit()
    db.session.remove()


def getCampaigns():
    campaigns = Campaign.query.all()
    return jsonify([campaign.serialize() for campaign in campaigns])


def getCampaignImageById(campaignId):
    campaign = Campaign.query.filter_by(Id=campaignId).first()
    
    if campaign.Image_ref is None:
        return {'message': 'Campaign has no image'}, 404
    try:
        fileExtension = os.path.splitext(campaign.Image_ref)[1]
        mimeType = mimetypes.types_map.get(fileExtension, 'image/jpeg')
        return send_from_directory('db/campaign_images', campaign.Image_ref, mimetype=mimeType)
    except FileNotFoundError:
        return {'message': 'Image not found'}, 404


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


'''
def read_all():
    people = Person.query.all()
    return people_schema.dump(people)


def create(person):
    lname = person.get("lname")
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person is None:
        new_person = person_schema.load(person, session=db.session)
        db.session.add(new_person)
        db.session.commit()
        return person_schema.dump(new_person), 201
    else:
        abort(406, f"Person with last name {lname} already exists")


def read_one(lname):
    person = Person.query.filter(Person.lname == lname).one_or_none()

    if person is not None:
        return person_schema.dump(person)
    else:
        abort(404, f"Person with last name {lname} not found")


def update(lname, person):
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person:
        update_person = person_schema.load(person, session=db.session)
        existing_person.fname = update_person.fname
        db.session.merge(existing_person)
        db.session.commit()
        return person_schema.dump(existing_person), 201
    else:
        abort(404, f"Person with last name {lname} not found")


def delete(lname):
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person:
        db.session.delete(existing_person)
        db.session.commit()
        return make_response(f"{lname} successfully deleted", 200)
    else:
        abort(404, f"Person with last name {lname} not found")
'''
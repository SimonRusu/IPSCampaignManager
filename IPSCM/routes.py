from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename
from uuid import uuid4
from controllers.BeaconBleSignalCrud import getBeaconBleSignalByCampaignId
from controllers.BeaconConfigurationCrud import getBeaconConfigurationByCampaignId
from controllers.CampaignSequenceCrud import getCampaignSequence
from controllers.CaptureCrud import getCapturesByCampaignId
from services.DatabaseGeneration import insert_data
from controllers.CampaignCrud import *
from controllers.DongleReceptorCrud import getDongleReceptor
import os
import pathlib

class GetCampaigns(Resource):
    def get(self):
        return getCampaigns()

class GetCampaignImagesById(Resource):
    def get(self, campaignId):
        return getCampaignImagesById(campaignId)
    
class GetDongleReceptor(Resource):
    def get(self, dongleId):
        return getDongleReceptor(dongleId)
    
class GetCampaignSequence(Resource):
    def get(self, sequenceId):
        return getCampaignSequence(sequenceId)
    
class GetCapturesByCampaignId(Resource):
    def get(self, campaignId):
        return getCapturesByCampaignId(campaignId)
    
class GetBeaconBleSignalByCampaignId(Resource):
    def get(self, campaignId):
        return getBeaconBleSignalByCampaignId(campaignId)

class GetBeaconConfigurationByCampaignId(Resource):
    def get(self, campaignId):
        return getBeaconConfigurationByCampaignId(campaignId)
    
class UploadCampaign(Resource):
    def post(self):
        name = request.form.get('name')
        date = request.form.get('date')
        file = request.files['file']
        description = None

        if 'description' in request.form:
            description = request.form.get('description')

        if 'image' in request.files:
            ranFolder = str(uuid4())
            basedir = pathlib.Path(__file__).parent.resolve()
            imagesFolder = os.path.join(basedir, 'db/campaign_images', ranFolder)
            os.makedirs(imagesFolder)

            images = request.files.getlist('image')

            for i in images:
                filename = secure_filename(i.filename)
                extension = os.path.splitext(filename)[1]
                ranFilename = str(uuid4()) + extension
                secRanFilename = secure_filename(ranFilename)
                i.save(os.path.join('db/campaign_images',imagesFolder, secRanFilename))
        else:
            secRanFilename = None
        
        if file:
            filename = secure_filename("auxDB.sqlite3")
            file.save(os.path.join('db', filename))
            insert_data(name, date, description, ranFolder)
            os.remove('db/auxDB.sqlite3')
    
class DeteteCampaignById(Resource):
    def delete(self, campaignId):
        return deleteCampaignById(campaignId)

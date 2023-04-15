from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename
from controllers.BeaconBleSignalCrud import getBeaconBleSignalByCampaignId
from controllers.BeaconConfigurationCrud import getBeaconConfigurationByCampaignId
from controllers.CampaignSequenceCrud import getCampaignSequence
from controllers.CaptureCrud import getCapturesByCampaignId
from services.DatabaseService import insert_data
from controllers.CampaignCrud import *
from controllers.DongleReceptorCrud import getDongleReceptor
import os

from services.ImageService import generateZipWithImages


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
        zipRef = None

        if 'description' in request.form:
            description = request.form.get('description')

        if 'image' in request.files:
            images = request.files.getlist('image')
            zipRef = generateZipWithImages(images)
        
        if file:
            filename = secure_filename("auxDB.sqlite3")
            file.save(os.path.join('db', filename))
            insert_data(name, date, description, zipRef)
            os.remove('db/auxDB.sqlite3')
    
class DeteteCampaignById(Resource):
    def delete(self, campaignId):
        return deleteCampaignById(campaignId)

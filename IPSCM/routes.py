from flask import request
from flask_restful import Resource
from controllers.CampaignCrud import *
from controllers.BeaconBleSignalCrud import getBeaconBleSignalByCampaignId
from controllers.BeaconConfigurationCrud import getBeaconConfigurationByCampaignId
from controllers.CampaignSequenceCrud import getCampaignSequence
from controllers.CaptureCrud import getCapturesByCampaignId
from controllers.DongleReceptorCrud import getDongleReceptor
from services.DatabaseService import insertIntoDatabase
from services.ImageService import generateZipImages


class GetCampaigns(Resource):
    def get(self):
        return getCampaigns()

class GetCampaignImagesById(Resource):
    def get(self, campaignId):
        return getCampaignImagesById(campaignId)
    
class GetRelatedCampaignById(Resource):
    def get(self, relatedCampaignId):
        return getRelatedCampaignById(relatedCampaignId)
    
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
        conf = request.form.get('conf')
        description = None
        imagesRef = None
        files = request.files

        if 'description' in request.form:
            description = request.form.get('description')

        if 'images' in request.files:
            images = request.files.getlist('images')
            imagesRef = generateZipImages(images)
        
        files = request.files.getlist('files')
        conf = request.files.get('conf')
        insertIntoDatabase(name, date, description, imagesRef, files, conf)
    
class DeteteCampaignById(Resource):
    def delete(self, campaignId):
        return deleteCampaignById(campaignId)

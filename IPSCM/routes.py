from flask import request
from flask_restful import Resource
from controllers.CampaignCrud import *
from controllers.BeaconBleSignalCrud import getBeaconBleSignalByCampaignId
from controllers.BeaconConfigurationCrud import getJsonBeaconConfigurationByCampaignId
from controllers.CampaignSequenceCrud import getCampaignSequence
from controllers.CaptureCrud import getCapturesByCampaignId
from controllers.DongleReceptorCrud import getDongleReceptor
from controllers.MethodPredictionCrud import getPredictionsByCampaignId
from controllers.TaskHistoryCrud import getTaskHistory
from services.DataProcessService import dataProcessing
from services.UploadService import uploadCampaign
from services.ImageService import generateZipImages

class ServerStatus(Resource):
    def get(self):
        return {"status": "Server is running"}

class GetCampaigns(Resource):
    def get(self):
        return getCampaigns()
    
class GetTaskHistory(Resource):
    def get(self):
        return getTaskHistory()

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
        return getJsonBeaconConfigurationByCampaignId(campaignId)
    
class GetPredictionsByCampaignId(Resource):
    def get(self, campaignId):
        return getPredictionsByCampaignId(campaignId)   
    
class DataProcessing(Resource):
    def post(self):
        params = request.form.get('params')
        data =  json.loads(params)
        return dataProcessing(data)
    
class UploadCampaign(Resource):
    def post(self):
        name = request.form.get('name')
        date = request.form.get('date')
        imagesRef = None

        description = request.form.get('description')
        if description=='null':
            description = "No hay descripción"
        
        if 'images' in request.files:
            images = request.files.getlist('images')
            imagesRef = generateZipImages(images)
        
        files = request.files.getlist('files')
        confs = request.files.getlist('confs')

        return uploadCampaign(name, date, description, imagesRef, files, confs)
    
class DeteteCampaignById(Resource):
    def delete(self, campaignId):
        return deleteCampaignById(campaignId)
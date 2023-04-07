from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename
from uuid import uuid4
from services.DatabaseGeneration import insert_data
from controllers.CampaignCrud import *
import os

class UploadCampaign(Resource):
    def post(self):
        name = request.form.get('name')
        date = request.form.get('date')
        file = request.files['file']
        description = None

        if 'description' in request.form:
            description = request.form.get('description')

        if 'image' in request.files:
            image = request.files['image']
            filename = secure_filename(image.filename)
            extension = os.path.splitext(filename)[1]
            ranFilename = str(uuid4()) + extension
            secRanFilename = secure_filename(ranFilename)
            image.save(os.path.join('db/campaign_images', secRanFilename))
        else:
            secRanFilename = None
        
        if file:
            filename = secure_filename("auxDB.sqlite3")
            file.save(os.path.join('db', filename))
            insert_data(name, date, description, secRanFilename)
            os.remove('db/auxDB.sqlite3')


class GetCampaigns(Resource):
    def get(self):
        return getCampaigns()

class GetCampaignImageById(Resource):
    def get(self, campaignId):
        return getCampaignImageById(campaignId)
    
class DeteteCampaignById(Resource):
    def delete(self, campaignId):
        return deleteCampaignById(campaignId)



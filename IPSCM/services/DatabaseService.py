import os
from werkzeug.utils import secure_filename
from controllers.BeaconConfigurationCrud import createBeaconConfiguration
from controllers.DongleReceptorCrud import createDongleReceptor
from controllers.BeaconBleSignalCrud import createBeaconBleSignal
from controllers.CaptureCrud import createCapture
from controllers.CampaignCrud import createCampaign, getLastInsertedCampaignId
from controllers.CampaignSequenceCrud import createCampaignSequence

def insertIntoDatabase(name, date, description, imagesRef, files):

    filename = secure_filename("auxDB.sqlite3")
    relatedCampaignId = None
    images = None


    for i,data in enumerate(files):
        files[i].save(os.path.join('db', filename))
        
        if(i == 1):
            relatedCampaignId = getLastInsertedCampaignId()
            images = imagesRef

        createCampaignSequence()
        createDongleReceptor()
        createCampaign(name, date, description, images, relatedCampaignId)
        createBeaconConfiguration()
        createBeaconBleSignal()
        createCapture()
        os.remove('db/auxDB.sqlite3')

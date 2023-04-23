import os
from werkzeug.utils import secure_filename
from controllers.BeaconConfigurationCrud import createBeaconConfiguration
from controllers.CampaignConfigurationsCrud import getLastInsertedBeaconConfName
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
        lastBeaconConfName = getLastInsertedBeaconConfName()

        if(i == 1):
            relatedCampaignId = getLastInsertedCampaignId()
            images = imagesRef

        createCampaignSequence()
        createDongleReceptor()
        createCampaign(name, date, description, images, relatedCampaignId)
    
        lastCampaignId = getLastInsertedCampaignId()
        beaconConfName = getNextBeaconConfName(lastCampaignId, lastBeaconConfName)

        createBeaconConfiguration(lastCampaignId, beaconConfName)
        createBeaconBleSignal()
        createCapture()
        os.remove('db/auxDB.sqlite3')


def getNextBeaconConfName(lastCampaignId, lastBeaconConfName):
    if lastBeaconConfName is not None:
        beaconConf = lastBeaconConfName[:-1]
        try:
            index = int(lastBeaconConfName[-1])
            index +=1
        except:
            index = lastCampaignId
        
        return beaconConf + str(index)
    else:
        return "___Configuración___0"
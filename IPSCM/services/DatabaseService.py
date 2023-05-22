import os
from werkzeug.utils import secure_filename
from controllers.BeaconConfigurationCrud import createBeaconConfiguration
from controllers.CampaignConfigurationsCrud import getLastInsertedBeaconConfName
from controllers.DongleReceptorCrud import createDongleReceptor
from controllers.BeaconBleSignalCrud import createBeaconBleSignal
from controllers.CaptureCrud import createCapture
from controllers.CampaignCrud import createCampaign, getLastInsertedCampaignId
from controllers.CampaignSequenceCrud import createCampaignSequence
from services.ConfigReaderService import readBLEConf, readAlePointsConf, readRefPointsConf
from services.DataProcessService import generatePredata

def insertIntoDatabase(name, date, description, imagesRef, files, confs):
    relatedCampaignId = None
    images = None

    filename = secure_filename("auxDB.sqlite3")

    campaignParams = readBLEConf(confs[0])
    alePointsJson = readAlePointsConf(confs[1])
    refPointsJson = readRefPointsConf(confs[2])

    for i,data in enumerate(files):
        files[i].save(os.path.join('db', filename))
        lastBeaconConfName = getLastInsertedBeaconConfName()

        if(i == 1):
            relatedCampaignId = getLastInsertedCampaignId()
            images = imagesRef

        createCampaignSequence()
        createDongleReceptor()
        createCampaign(name, date, description, images, relatedCampaignId, campaignParams, alePointsJson, refPointsJson)
    
        lastCampaignId = getLastInsertedCampaignId()
        beaconConfName = getNextBeaconConfName(lastCampaignId, lastBeaconConfName)

        createBeaconBleSignal()
        createCapture()
        
        createBeaconConfiguration(lastCampaignId, beaconConfName)
        generatePredata(lastCampaignId)

        os.remove('db/auxDB.sqlite3')


def getNextBeaconConfName(lastCampaignId, lastBeaconConfName):
    if lastBeaconConfName is not None:
        beaconConf = lastBeaconConfName.split('_')[:-1]
        try:
            index = int(lastBeaconConfName.split('_')[-1])
            index += 1
            if index >= 10:
                beaconConf.append(str(index))
            else:
                beaconConf.append('0' + str(index))
        except:
            index = lastCampaignId
            beaconConf.append('0' + str(index))
        
        return '_'.join(beaconConf)
    else:
        return "___Configuración___00"
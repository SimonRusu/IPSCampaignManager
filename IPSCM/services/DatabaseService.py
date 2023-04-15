from controllers.BeaconConfigurationCrud import createBeaconConfiguration
from controllers.DongleReceptorCrud import createDongleReceptor
from controllers.BeaconBleSignalCrud import createBeaconBleSignal
from controllers.CaptureCrud import createCapture
from controllers.CampaignCrud import createCampaign
from controllers.CampaignSequenceCrud import createCampaignSequence


def insert_data(name, data, description, image):
    createCampaignSequence()
    createDongleReceptor()
    createCampaign(name, data, description, image)
    createBeaconConfiguration()
    createBeaconBleSignal()
    createCapture()
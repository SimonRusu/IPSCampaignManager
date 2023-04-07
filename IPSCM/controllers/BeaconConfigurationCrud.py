from controllers.BeaconBleSignalCrud import getBeaconBleSignalIdentificatorByCampaignId
from models.BeaconConfiguration import BeaconConfiguration, BeaconConfigurationAux
from config import db
from sqlalchemy import desc
from models.Campaign import Campaign

def createBeaconConfiguration():
    db.create_all()
    beaconConfigurationAux = BeaconConfigurationAux.query.all()
    campaignId = Campaign().query.order_by(desc(Campaign.Id)).first().Id
    
    for i in beaconConfigurationAux:
        beaconConfiguration = BeaconConfiguration()
        beaconConfiguration.Id_campaign = campaignId
        beaconConfiguration.Mac = i.Mac
        beaconConfiguration.Power = i.Power
        beaconConfiguration.Calibrated_power = i.Calibrated_power
        beaconConfiguration.Update_frequency = i.Update_frequency
        beaconConfiguration.Identificator = i.Identificator
        db.session.add(beaconConfiguration)
    
    db.session.commit()
    db.session.remove()

def getBeaconConfigurationByCampaignId(campaignId:int):
    identificators = getBeaconBleSignalIdentificatorByCampaignId(campaignId)
    print(len(identificators))

def deleteBeaconConfigurationByCampaignId(campaignId):
    existingCapture = BeaconConfiguration().query.filter_by(Id_campaign=campaignId).delete()

    if existingCapture:
        db.session.commit()

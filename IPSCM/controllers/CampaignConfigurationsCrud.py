from models.CampaignConfigurations import CampaignConfigurations
from config import db

def createCampaignConfigurations(campaignId, beaconConfId, beaconConfName):
    db.create_all()
    existingRecord = CampaignConfigurations.query.filter_by(Id_campaign=campaignId, Id_beacon_configuration=beaconConfId, Name=beaconConfName).first()
    if existingRecord is None:
        campaignConfiguration = CampaignConfigurations()
        campaignConfiguration.Id_campaign = campaignId
        campaignConfiguration.Id_beacon_configuration = beaconConfId
        campaignConfiguration.Name = beaconConfName
        db.session.add(campaignConfiguration)
    
    db.session.commit()

def getLastInsertedBeaconConfName():
    db.create_all()
    confName = CampaignConfigurations.query.filter(CampaignConfigurations.Name.like('%___Configuración___%')).order_by(CampaignConfigurations.Name.desc()).first()

    if confName is not None:
        return confName.Name
    else:
        return None
    
def getCampaignBeaconConfigurationIdsByCampaignId(campaignId):
    configurations = CampaignConfigurations.query.filter_by(Id_campaign=campaignId).all()
    ids = [configuration.Id_beacon_configuration for configuration in configurations]
    return ids

def deleteConfigurationsByCampaignId(campaignId):
    existingConfiguration = CampaignConfigurations().query.filter_by(Id_campaign=campaignId).delete()

    if existingConfiguration:
        db.session.commit()
from models.CampaignSequence import CampaignSequence, CampaignSequenceAux
from config import db

def createCampaignSequence():
    db.create_all()
    campaignSequenceAux = CampaignSequenceAux.query.all()

    campaignSequence = CampaignSequence()
    campaignSequence.Dongle_receptor = campaignSequenceAux[0].Seq
    campaignSequence.Beacon_configuration = campaignSequenceAux[1].Seq
    campaignSequence.Capture = campaignSequenceAux[2].Seq
    campaignSequence.Beacon_BLE_Signal = campaignSequenceAux[3].Seq
    db.session.add(campaignSequence)
    
    db.session.commit()
    db.session.remove()

def deleteCampaignSequenceByCampaignId(sequenceId):
    existingSequence = CampaignSequence().query.filter_by(Id=sequenceId).first()

    if existingSequence:
        db.session.delete(existingSequence)
        db.session.commit()

def getCampaignSequence(id:int):
    return CampaignSequence().query.filter_by(Id=id).first().serialize()
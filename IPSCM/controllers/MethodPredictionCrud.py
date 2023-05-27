from config import db
from models.MethodPrediction import MethodPrediction

def createMethodPrediction(campaignId, method, protocol, channel, rssi_samples, ks_range, predicted_points, mean_error):

    methodPrediction = MethodPrediction()
    methodPrediction.Id_campaign = campaignId
    methodPrediction.Method = method
    methodPrediction.Protocol = protocol
    methodPrediction.Channel = channel 
    methodPrediction.RSSI_samples = rssi_samples
    methodPrediction.Ks_range = ks_range
    methodPrediction.Predicted_points = predicted_points
    methodPrediction.Mean_error = mean_error

    db.session.add(methodPrediction)
    
    db.session.commit()
    db.session.remove()


def checkExistingMethodPredictionByParams(campaignId, method, protocol, channel, rssi_samples, ks_range):
    existing_entry = MethodPrediction.query.filter_by(
    Id_campaign=campaignId,
    Method=method,
    Protocol=protocol,
    Channel=channel,
    RSSI_samples=rssi_samples,
    Ks_range=ks_range
    ).first()

    if existing_entry:
        return True
    else:
        return False
    

def getPredictionsByCampaignId(campaignId:int):
    result = MethodPrediction.query.filter_by(Id_campaign=campaignId).all()
    predictions = [prediction.serialize() for prediction in result]

    return predictions


def deleteMethodPredictionByCampaignId(campaignId):
    existingPrediction = MethodPrediction().query.filter_by(Id_campaign=campaignId).delete()

    if existingPrediction:
        db.session.commit()
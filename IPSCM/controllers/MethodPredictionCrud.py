from config import db
from models.MethodPrediction import MethodPrediction

def createMethodPrediction(campaignId, method, protocol, channel, rssi_samples, ks_range, predicted_points):

    methodPrediction = MethodPrediction()
    methodPrediction.Id_campaign = campaignId
    methodPrediction.Method = method
    methodPrediction.Protocol = protocol
    methodPrediction.Channel = channel 
    methodPrediction.RSSI_samples = rssi_samples
    methodPrediction.Ks_range = ks_range
    methodPrediction.Predicted_points = predicted_points

    db.session.add(methodPrediction)
    
    db.session.commit()
    db.session.remove()
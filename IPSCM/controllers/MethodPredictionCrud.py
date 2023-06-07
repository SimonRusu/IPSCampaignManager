from config import db
from models.MethodPrediction import MethodPrediction

def createMethodPrediction(campaignId, method_description, predicted_points, mean_error):

    methodPrediction = MethodPrediction()
    methodPrediction.Id_campaign = campaignId
    methodPrediction.Method_description = method_description
    methodPrediction.Predicted_points = predicted_points
    methodPrediction.Mean_error = mean_error

    db.session.add(methodPrediction)
    
    db.session.commit()
    db.session.remove()

def checkExistingMethodPrediction(campaignId, description):
    existing_entry = MethodPrediction.query.filter_by(
    Id_campaign=campaignId,
    Method_description=description
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
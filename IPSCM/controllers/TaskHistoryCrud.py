import datetime
from flask import jsonify
from config import db
from models.TaskHistory import TaskHistory



def createTaskHistory(campaignId, campaignName, status, task_description, datetime_start):

    taskHistory = TaskHistory()
    taskHistory.Id_campaign = campaignId
    taskHistory.Name = campaignName
    taskHistory.Status = status
    taskHistory.Task_description = task_description

    formatted_date = datetime.datetime.strftime(datetime_start, '%d/%m/%Y %H:%M:%S')
    taskHistory.Datetime_start = formatted_date 

    db.session.add(taskHistory)
    db.session.commit()


def getTaskHistory():
    taskHistory = TaskHistory.query.all()
    return jsonify([task.serialize() for task in taskHistory])


def updateTaskHistory(campaignId, task_description, status, datetime_end=None):
    existing_entry = TaskHistory.query.filter_by(
        Id_campaign=campaignId, 
        Task_description=task_description).first()
    
    if existing_entry:
        setattr(existing_entry, 'Status', status)

        if datetime_end is not None:
            formatted_date = datetime.datetime.strftime(datetime_end, '%d/%m/%Y %H:%M:%S')
            setattr(existing_entry, 'Datetime_end', formatted_date)

        db.session.flush()
        db.session.commit()


def deleteTaskHistoryByCampaignId(campaignId):
    existingPrediction = TaskHistory().query.filter_by(Id_campaign=campaignId).delete()

    if existingPrediction:
        db.session.commit()
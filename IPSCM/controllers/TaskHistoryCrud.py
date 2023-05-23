import datetime
from flask import jsonify
from config import db
from models.TaskHistory import TaskHistory


def createTaskHistory(campaignId, status, task_description, datetime_start):
    formattedDate = datetime.strptime(datetime_start, '%Y-%m-%d').date()

    taskHistory = TaskHistory()
    taskHistory.Id_campaign = campaignId
    taskHistory.Status = status
    taskHistory.Task_description = task_description
    taskHistory.Datetime_start = formattedDate 

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
            formattedDate = datetime.strptime(datetime_end, '%Y-%m-%d').date()
            setattr(existing_entry, 'Datetime_end', formattedDate)

        db.session.flush()
        db.session.commit()


def deleteTaskHistoryByCampaignId(campaignId):
    existingPrediction = TaskHistory().query.filter_by(Id_campaign=campaignId).delete()

    if existingPrediction:
        db.session.commit()
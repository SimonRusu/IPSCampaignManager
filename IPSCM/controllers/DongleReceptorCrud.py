from flask import jsonify
from models.DongleReceptor import DongleReceptor, DongleReceptorAux
from config import db

def createDongleReceptor():
    db.create_all()
    dongleReceptorAux = DongleReceptorAux.query.all()

    for i in dongleReceptorAux:
        exists = DongleReceptor().query.filter_by(Name=i.Name).first()
        if exists is None:
            dongleReceptor = DongleReceptor()
            dongleReceptor.Name = i.Name
            db.session.add(dongleReceptor)
    
    db.session.commit()
    db.session.remove()

def getDongleReceptor(id:int):
    return jsonify(DongleReceptor().query.filter_by(Id=id).first().Name)


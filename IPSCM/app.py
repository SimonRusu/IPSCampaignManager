from config import app
from flask_restful import Api
from flask_cors import CORS
from routes import *


with app.app_context():

    api = Api(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    #Recursos de la api.
    api.add_resource(UploadCampaign, '/api/upload_campaign')
    api.add_resource(GetCampaigns, '/api/campaigns')
    api.add_resource(GetCampaignImagesById, '/api/campaignImages/<int:campaignId>')
    api.add_resource(DeteteCampaignById, '/api/deleteCampaign/<int:campaignId>')
    api.add_resource(GetDongleReceptor, '/api/dongleReceptor/<int:dongleId>')
    api.add_resource(GetCampaignSequence, '/api/campaignSequence/<int:sequenceId>')
    api.add_resource(GetCapturesByCampaignId, '/api/capturesByCampaign/<int:campaignId>')
    api.add_resource(GetBeaconBleSignalByCampaignId, '/api/signalsByCampaign/<int:campaignId>')
    api.add_resource(GetBeaconConfigurationByCampaignId, '/api/configsByCampaign/<int:campaignId>')
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
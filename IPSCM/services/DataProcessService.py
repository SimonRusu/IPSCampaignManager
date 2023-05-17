from controllers.BeaconBleSignalCrud import getBeaconBleSignalById
from controllers.BeaconConfigurationCrud import getBeaconConfigurationByCampaignId
from controllers.CampaignCrud import getPointsByCampaignId
from controllers.CaptureCrud import getCaptureIdsByCampaignId, getCapturesByIdAndRotation
from controllers.MethodPredataCrud import createMethodPredataBatch, getFilteredPredataSamples

def generatePredata(campaignId):
    captureIds = getCaptureIdsByCampaignId(campaignId)
    filteredCapture = getCapturesByIdAndRotation(captureIds)

    batch_data = []

    for capture in filteredCapture:
        filteredSignals = getBeaconBleSignalById(capture.Id)
        for signal in filteredSignals:
            batch_data.append((campaignId, capture.Date, signal.Channel, signal.Mac, capture.Dongle_rotation, signal.Protocol,
                             signal.RSSI, capture.Position_x, capture.Position_y, capture.Position_z))
    
    createMethodPredataBatch(batch_data)

def parsePredata():
    campaignId = 2
    protocol = 'Eddystone'
    channel = 37
    rssi_samples = 10

    alebeaconMacs = getBeaconConfigurationByCampaignId(campaignId-1)
    refbeaconMacs = getBeaconConfigurationByCampaignId(campaignId)
    configPoints = getPointsByCampaignId(2)
    ale_points = configPoints['Ale_points']
    ref_points = configPoints['Ref_points']
    
    aleRSSIList = getAlePointsRSSIList(ale_points, alebeaconMacs, campaignId-1, protocol, channel, rssi_samples)
    refRSSIList = getRefPointsRSSIList(ref_points, refbeaconMacs, campaignId, protocol, channel, rssi_samples)
        

def getAlePointsRSSIList(points, beaconMacs, campaignId, protocol, channel, rssi_samples):
  
    for point_name, point_values in points.items():
        x = float(point_values['X'])
        y = float(point_values['Y'])
        z = float(point_values['Z'])
        rotation = float(point_values['Rotation'])
        print(f"{point_name} has X={x}, Y={y}, Z={z}, Rotation={rotation}")


        for mac in beaconMacs:
            matchSamples = getFilteredPredataSamples(campaignId, rssi_samples, rotation, mac, protocol, channel, x, y, z)
            print("entro_ale")

            for i in matchSamples:

                print("Id:", i.Id)
                print("Id_campaign:", i.Id_campaign)
                print("Date:", i.Date)
                print("Channel:", i.Channel)
                print("Mac:", i.Mac)
                print("Dongle_rotation:", i.Dongle_rotation)
                print("Protocol:", i.Protocol)
                print("RSSI:", i.RSSI)
                print("Position_x:", i.Position_x)
                print("Position_y:", i.Position_y)
                print("Position_z:", i.Position_z)
                print("-----------------------")

def getRefPointsRSSIList(points, beaconMacs, campaignId, protocol, channel, rssi_samples):
    for point_name, point_values in points.items():
        x = float(point_values['X'])
        y = float(point_values['Y'])
        z = float(point_values['Z'])
        rotations = point_values['Rotations']
        print(f"{point_name} has X={x}, Y={y}, Z={z}, Rotations:")
        for rotation in rotations:
            for mac in beaconMacs:
                matchSamples = getFilteredPredataSamples(campaignId, rssi_samples, float(rotation), mac, protocol, channel, x, y, z)
                print("entro_ale")

                for i in matchSamples:

                    print("Id:", i.Id)
                    print("Id_campaign:", i.Id_campaign)
                    print("Date:", i.Date)
                    print("Channel:", i.Channel)
                    print("Mac:", i.Mac)
                    print("Dongle_rotation:", i.Dongle_rotation)
                    print("Protocol:", i.Protocol)
                    print("RSSI:", i.RSSI)
                    print("Position_x:", i.Position_x)
                    print("Position_y:", i.Position_y)
                    print("Position_z:", i.Position_z)
                    print("-----------------------")
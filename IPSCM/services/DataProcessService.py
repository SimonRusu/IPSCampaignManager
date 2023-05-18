from controllers.BeaconBleSignalCrud import getBeaconBleSignalById, getMacsByCampaignId
from controllers.BeaconConfigurationCrud import getBeaconConfigurationByCampaignId
from controllers.CampaignCrud import getPointsByCampaignId
from controllers.CaptureCrud import getCaptureIdsByCampaignId, getCapturesByIdAndRotation
from controllers.MethodPredataCrud import createMethodPredataBatch, getFilteredPredataSamples, getUniqueCoordinatesByCampaignId
import numpy as np


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
    macsUniq=getMacsByCampaignId(1)
    print(macsUniq)
    aleBeaconMacs = getBeaconConfigurationByCampaignId(campaignId-1)
    refBeaconMacs = getBeaconConfigurationByCampaignId(campaignId)
    configPoints = getPointsByCampaignId(campaignId)

    ale_points_conf = configPoints['Ale_points']
    ref_points_conf = configPoints['Ref_points']
    
    ale_points = getUniqueCoordinatesByCampaignId(campaignId-1, len(ale_points_conf))
    ref_points = getUniqueCoordinatesByCampaignId(campaignId, len(ref_points_conf))

    aleRSSIList = getAlePointsRSSIList(ale_points, ale_points_conf, aleBeaconMacs, campaignId-1, protocol, channel, rssi_samples)
   # refRSSIList = getRefPointsRSSIList(ref_points, ref_points_conf, refBeaconMacs, campaignId, protocol, channel, rssi_samples)
        

def getAlePointsRSSIList(points, points_conf, beaconMacs, campaignId, protocol, channel, rssi_samples):
    
    cols = len(beaconMacs)
    rows = len(points)

    alePointsMatrix = np.full((rows, cols), -np.inf)
    
    for point_name, point_values in points_conf.items():
        rotation = float(point_values['Rotation'])
        print(f"{point_name} has Rotation={rotation}")

        for i, point in enumerate(points):
            for j, mac in enumerate(beaconMacs):
                print(mac)
                print(j)
                matchSamples = getFilteredPredataSamples(campaignId, rssi_samples, rotation, mac, protocol, channel, point['x'], point['y'], point['z'])
                print(campaignId, rssi_samples, rotation, mac, protocol, channel, point['x'], point['y'], point['z'])
                print(matchSamples)
                if matchSamples:
                    max_sample = max(matchSamples, key=lambda sample: sample.RSSI)
                    if max_sample.RSSI > alePointsMatrix[i,j]:
                        alePointsMatrix[i,j] = max_sample.RSSI
                    #elif i > 0:
                    #    alePointsMatrix[i,j] = max(alePointsMatrix[i-1,j], alePointsMatrix[i,j])

    print(alePointsMatrix)


def getRefPointsRSSIList(points, points_conf, beaconMacs, campaignId, protocol, channel, rssi_samples):
    print(points)
    print(len(points))
    for point_name, point_values in points_conf.items():
        rotations = point_values['Rotations']
        print(f"{point_name}  Rotations:")
        for rotation in rotations:
            for mac in beaconMacs:
                for point in points:
                    matchSamples = getFilteredPredataSamples(campaignId, rssi_samples, float(rotation), mac, protocol, channel, point['x'], point['y'], point['z'])
                    #print("entro_ale")

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


def recorrerPuntos():
    for point_name, point_values in points.items():
        x = float(point_values['X'])
        y = float(point_values['Y'])
        z = float(point_values['Z'])
        rotation = float(point_values['Rotation'])
        print(f"{point_name} has X={x}, Y={y}, Z={z}, Rotation={rotation}")

    for point_name, point_values in points.items():
        x = float(point_values['X'])
        y = float(point_values['Y'])
        z = float(point_values['Z'])
        rotations = point_values['Rotations']
        print(f"{point_name} has X={x}, Y={y}, Z={z}, Rotations:")
        
        for rotation in rotations:
            return

    
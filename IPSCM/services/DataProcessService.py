from controllers.BeaconBleSignalCrud import getBeaconBleSignalById, existsBeaconWithProtocol
from controllers.BeaconConfigurationCrud import getBeaconConfigurationByCampaignId
from controllers.CampaignCrud import getPointsByCampaignId
from controllers.CaptureCrud import getCaptureIdsByCampaignId, getCapturesByIdAndRotation
from controllers.MethodPredataCrud import createMethodPredataBatch, getFilteredPredataSamples, getUniqueCoordinatesByCampaignId
from services.MethodsService import applyMethod
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

def dataProcessing(params):
    campaignId = 2
    method = 1
    protocol = 'Eddystone'
    channel = 39
    rssiSamples = 10
    ksRange = (1, 10)

    aleBeaconMacs, refBeaconMacs = processBeaconMacs(campaignId, protocol)

    configPoints = getPointsByCampaignId(campaignId)

    ref_points_conf = configPoints['Ref_points']
    ale_points_conf = configPoints['Ale_points']
    
    ref_points = getUniqueCoordinatesByCampaignId(campaignId, len(ref_points_conf))
    ale_points = getUniqueCoordinatesByCampaignId(campaignId-1, len(ale_points_conf))
 
    refRSSIMatrix = getRefPointsMatrix(ref_points, ref_points_conf, refBeaconMacs, campaignId, protocol, channel, rssiSamples)
    aleRSSIMatrix= getAlePointsMatrix(ale_points, ale_points_conf, aleBeaconMacs, campaignId-1, protocol, channel, rssiSamples)

    applyMethod(refRSSIMatrix, aleRSSIMatrix, method, ksRange)
        

def getAlePointsMatrix(points, points_conf, beaconMacs, campaignId, protocol, channel, rssi_samples):
    coordinates = 3
    cols = len(beaconMacs) + coordinates
    rows = len(points)

    alePointsMatrix = np.full((rows, cols), -np.inf)
    
    for i, (point, point_values) in enumerate(zip(points, points_conf.values())):
        x = float(point_values['X'])
        y = float(point_values['Y'])
        z = float(point_values['Z'])
        rotation = float(point_values['Rotation'])
        
        for j, mac in enumerate(beaconMacs):
            matchSamples = getFilteredPredataSamples(campaignId, rssi_samples, rotation, mac, protocol, channel, point['x'], point['y'], point['z'])

            if matchSamples:
                max_sample = max(matchSamples, key=lambda sample: sample.RSSI)
                alePointsMatrix[i,j] = max_sample.RSSI

        alePointsMatrix[i,cols - 3] = x
        alePointsMatrix[i,cols - 2] = y
        alePointsMatrix[i,cols - 1] = z

    return alePointsMatrix


def getRefPointsMatrix(points, points_conf, beaconMacs, campaignId, protocol, channel, rssi_samples):
    coordinates = 3
    cols = len(beaconMacs) + coordinates
    rows = len(points)

    refPointsMatrix = np.full((rows, cols), -np.inf)

    for i, (point, point_values) in enumerate(zip(points, points_conf.values())):
        x = float(point_values['X'])
        y = float(point_values['Y'])
        z = float(point_values['Z'])
        rotations = point_values['Rotations']

        for j, mac in enumerate(beaconMacs):
            max_samples = []

            for k, rotation in enumerate(rotations):
                matchSamples = getFilteredPredataSamples(campaignId, 0, float(rotation), mac, protocol, channel, point['x'], point['y'], point['z'])

                if matchSamples:
                    max_sample = max(matchSamples, key=lambda sample: sample.RSSI)
                    max_samples.append(max_sample.RSSI)
                    

            avg_max_sample = sum(max_samples) / len(max_samples)
            refPointsMatrix[i,j] = avg_max_sample

        refPointsMatrix[i,cols - 3] = x
        refPointsMatrix[i,cols - 2] = y
        refPointsMatrix[i,cols - 1] = z

    return refPointsMatrix


def processBeaconMacs(campaignId, protocol):
    aleBeaconMacs = getBeaconConfigurationByCampaignId(campaignId-1)
    refBeaconMacs = getBeaconConfigurationByCampaignId(campaignId)

    aleBeaconsProcessed = []
    refBeaconsProcessed = []

    for mac in aleBeaconMacs:
        if existsBeaconWithProtocol(campaignId-1, mac, protocol) == True:
            aleBeaconsProcessed.append(mac)

    for mac in refBeaconMacs:
        if existsBeaconWithProtocol(campaignId, mac, protocol) == True:
            refBeaconsProcessed.append(mac)

    return aleBeaconsProcessed, refBeaconsProcessed
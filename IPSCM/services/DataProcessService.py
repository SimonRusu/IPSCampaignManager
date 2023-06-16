import json
import numpy as np
from datetime import datetime
from controllers.BeaconBleSignalCrud import getBeaconBleSignalById, existsBeaconWithProtocol
from controllers.BeaconConfigurationCrud import getBeaconConfigurationByCampaignId
from controllers.CampaignCrud import getPointsByCampaignId
from controllers.CaptureCrud import getCaptureIdsByCampaignId, getCapturesByIdAndRotation
from controllers.MethodPredataCrud import createMethodPredataBatch, getFilteredPredataSamples, getUniqueCoordinatesByCampaignId
from controllers.MethodPredictionCrud import checkExistingMethodPrediction, createMethodPrediction
from services.MethodsService import applyMethod, calculate_error
from controllers.TaskHistoryCrud import createTaskHistory, updateTaskHistory

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

def dataProcessing(data):
    campaignId = data['campaign']
    campaignName = data['campaignName']
    method = data['method']
    protocols = data['protocols']
    channels = data['channels']
    rssiSamples = data['sample']
    metrics = data['metrics']
    algorithms = data['algorithms']
    kernels = data['kernels']
    cs = data['cValues']
    gammas = data['gValues']
    nus = data['nuValues']
    Is = data['iValues']
    ksRange = []
    ksRange.append(data['kRangeStart'])

    configPoints = getPointsByCampaignId(campaignId)

    ref_points_conf = configPoints['Ref_points']
    ale_points_conf = configPoints['Ale_points']

    ref_points = getUniqueCoordinatesByCampaignId(campaignId, len(ref_points_conf))
    ale_points = getUniqueCoordinatesByCampaignId(campaignId-1, len(ale_points_conf))

    if(len(ref_points)) < data['kRangeEnd']:
        ksRange.append(len(ref_points))
    else:
        ksRange.append(data['kRangeEnd'])
    
    ksRangeJson = json.dumps(ksRange)

    for protocol in protocols:
        aleBeaconMacs, refBeaconMacs = processBeaconMacs(campaignId, protocol)
        for channel in channels:
            for metric in metrics:
                for algorithm in algorithms:
                    for kernel in kernels:

                        taskId = taskToJson(method, protocol, channel, rssiSamples, algorithm, metric, ksRangeJson, kernel, cs, gammas, nus, Is)
                        
                        if not checkExistingMethodPrediction(campaignId, taskId):

                            datetime_start = datetime.now()
                            createTaskHistory(campaignId, campaignName, "Obteniendo matriz de puntos de referencia...", taskId, datetime_start)
                            
                            refRSSIMatrix = getRefPointsMatrix(ref_points, ref_points_conf, refBeaconMacs, campaignId, protocol, channel, rssiSamples)

                            updateTaskHistory(campaignId, taskId, "Obteniendo matriz de puntos aleatorios...")

                            aleRSSIMatrix= getAlePointsMatrix(ale_points, ale_points_conf, aleBeaconMacs, campaignId-1, protocol, channel, rssiSamples)

                            updateTaskHistory(campaignId, taskId, "Aplicando método de posicionamiento...")

                            predicted_points = applyMethod(refRSSIMatrix, aleRSSIMatrix, method, metric, algorithm, ksRange, kernel, cs, gammas, nus, Is, taskId)

                            mean_error = calculate_error(aleRSSIMatrix, predicted_points)

                            createMethodPrediction(campaignId, taskId, json.dumps(predicted_points), json.dumps(mean_error))

                            datetime_end = datetime.now()
                            updateTaskHistory(campaignId, taskId, "Completado", datetime_end)

        

def getRefPointsMatrix(points, points_conf, beaconMacs, campaignId, protocol, channel, rssiSamples):
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
                matchSamples = getFilteredPredataSamples(campaignId, rssiSamples, float(rotation), mac, protocol, channel, point['x'], point['y'], point['z'])

                if matchSamples:
                    max_sample = max(matchSamples, key=lambda sample: sample.RSSI)
                    max_samples.append(max_sample.RSSI)
                    

            avg_max_sample = sum(max_samples) / len(max_samples)
            refPointsMatrix[i,j] = avg_max_sample

        refPointsMatrix[i,cols - 3] = x
        refPointsMatrix[i,cols - 2] = y
        refPointsMatrix[i,cols - 1] = z

    return refPointsMatrix


def getAlePointsMatrix(points, points_conf, beaconMacs, campaignId, protocol, channel, rssiSamples):

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
            matchSamples = getFilteredPredataSamples(campaignId, rssiSamples, rotation, mac, protocol, channel, point['x'], point['y'], point['z'])

            if matchSamples:
                max_sample = max(matchSamples, key=lambda sample: sample.RSSI)
                alePointsMatrix[i,j] = max_sample.RSSI

        alePointsMatrix[i,cols - 3] = x
        alePointsMatrix[i,cols - 2] = y
        alePointsMatrix[i,cols - 1] = z

    return alePointsMatrix

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


def taskToJson(methods, protocols, channels, rssiSamples, algorithm, metric, ksRange, kernel, cs, gammas, nus, Is):
    taskDescription = json.dumps({
    'method': methods,
    'protocol': protocols,
    'channel': channels,
    'rssiSample': rssiSamples,
    'algorithm': algorithm,
    'metric': metric,
    'ksRange': ksRange,
    'kernel': kernel,
    'cs': cs,
    'gammas': gammas,
    'nus': nus,
    'Is': Is
    })

    return taskDescription
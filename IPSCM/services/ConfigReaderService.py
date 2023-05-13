import configparser
import json
config = configparser.ConfigParser()

def readBLEConf(file):
    values = []

    content = file.read()
    content = content.decode('utf-8')
    config.read_string(content)
    duration = config.get('BLE', 'Duration')
    rotations = config.get('Orientator', 'Rotations')

    values.append(duration)
    values.append(rotations)

    return values

def readAlePointsConf(file):
    content = file.read()
    content = content.decode('utf-8')
    config.read_string(content)

    points = {}
    for section in config.sections():
        if section.startswith('POINT_'):
            point = {}
            point['X'] = config.get(section, 'X')
            point['Y'] = config.get(section, 'Y')
            point['Z'] = config.get(section, 'Z')
            point['Rotation'] = config.getfloat(section, 'Rotation')
            points[section] = point

    return json.dumps(points)


def readRefPointsConf(file):
    content = file.read()
    content = content.decode('utf-8')
    config.read_string(content)

    points = {}
    for section in config.sections():
        if section.startswith('POINT_'):
            point = {}
            point['X'] = config.get(section, 'X')
            point['Y'] = config.get(section, 'Y')
            point['Z'] = config.get(section, 'Z')
            rotations = config.get(section, 'Rotations')
            point['Rotations'] = [float(rotation) for rotation in rotations.split(',')]
            points[section] = point

    return json.dumps(points)


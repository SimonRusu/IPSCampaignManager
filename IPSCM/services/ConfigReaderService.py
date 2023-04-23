import configparser

def readBLEConf(file):
    values = []

    config = configparser.ConfigParser()
    content = file.read()
    content = content.decode('utf-8')
    config.read_string(content)
    duration = config.get('BLE', 'Duration')
    rotations = config.get('Orientator', 'Rotations')

    values.append(duration)
    values.append(rotations)

    return values

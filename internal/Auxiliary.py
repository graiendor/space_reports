import json


def check_coordinates(coordinates: list[str]):
    if len(coordinates) != 6:
        raise ValueError('Coordinates must be 6 values')
    try:
        [int(coordinate) for coordinate in coordinates[:1]]
        [int(coordinate) for coordinate in coordinates[3:4]]
    except ValueError:
        raise ValueError('Coordinates 1, 2, 4, 5 must be integers')
    try:
        float(coordinates[2])
        float(coordinates[5])
    except ValueError:
        raise ValueError('Coordinates 3, 6 must be floats')
    return True


def generate_json(response):
    data = json.loads(response)
    if data.get('armed') is None:
        data['armed'] = False
    data = json.dumps(data)
    return data

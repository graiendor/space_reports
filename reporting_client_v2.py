import sys

import google.protobuf.json_format as js

import grpc
import api_pb2_grpc as pb2_grpc
import api_pb2 as pb2

from internal.SpaceshipValidator import SpaceshipValidator
from internal.Spaceship import Spaceship
from internal.Auxiliary import check_coordinates, generate_json

class ReportClient(object):
    def __init__(self):
        self.host = 'localhost'
        self.server_port = 6666

    def get_spaceship(self, coordinates: list[str]):
        with grpc.insecure_channel('localhost:6666') as channel:
            stub = pb2_grpc.ReportStub(channel)
            if check_coordinates(coordinates):
                message = pb2.Coordinates(coordinate1=int(coordinates[0]), coordinate2=int(coordinates[1]),
                                          coordinate3=float(coordinates[2]), coordinate4=int(coordinates[3]),
                                          coordinate5=int(coordinates[4]), coordinate6=float(coordinates[5]))
                response = stub.GetSpaceship(message)
                reports = response.report
                for report in reports:
                    try:
                        officers = [{'first_name': officer.first_name, 'last_name': officer.last_name, 'rank': officer.rank} for officer in list(report.officers)]
                        spaceship = Spaceship(alignment=report.alignment, name=report.name, length=round(report.length, 2),
                                        vessel_class=report.vessel_class, size=report.size, armed=report.armed,
                                        officers=officers)
                        SpaceshipValidator(**spaceship.__dict__())
                        print(js.MessageToJson(report))
                    except ValueError as v:
                        print('Spaceship is not valid')


if __name__ == '__main__':
    client = ReportClient()
    coordinates = sys.argv[1:]
    print(coordinates)
    client.get_spaceship(coordinates)

import sys

import google.protobuf.json_format as js

import grpc
import api_pb2_grpc as pb2_grpc
import api_pb2 as pb2
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
                reports = stub.GetSpaceship(message)
                for report in reports:
                    print(js.MessageToJson(report))


if __name__ == '__main__':
    client = ReportClient()
    coordinates = sys.argv[1:]
    client.get_spaceship(coordinates)

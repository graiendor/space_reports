import sys

import google.protobuf.json_format as js
from typing import List, Dict, Optional

import grpc
import api_pb2_grpc as pb2_grpc
import api_pb2 as pb2

from internal.Spaceship import Spaceship
from internal.SpaceshipValidator import SpaceshipValidator
from internal.Recorder import Recorder
from internal.Auxiliary import check_coordinates, generate_json
from argparse import ArgumentParser, REMAINDER
import json


class ReportClient(object):
    def __init__(self):
        self.host = 'localhost'
        self.server_port = 6666
        self.recorder = Recorder()
        self.argument_parser = ArgumentParser()

    def parse_arguments(self):
        self.argument_parser.add_argument('option', choices=['scan', 'list_of_traitors'], nargs='?')
        self.argument_parser.add_argument('coordinates', nargs=REMAINDER, type=str, help='Coordinates')
        return self.argument_parser.parse_args()

    def run(self):
        arguments = self.parse_arguments()
        if not arguments.option and not arguments.option:
            self.get_spaceship(arguments.coordinates)
        elif arguments.option == 'scan':
            print('Scanning...')
            self.scan(arguments.coordinates)
            print('Scan completed')
        elif arguments.option == 'list_of_traitors':
            print('Traitors:')
            traitors = json.loads(self.list_of_traitors())
            for traitor in traitors:
                print(traitor)

    def get_spaceship(self, coordinates: List[str]):
        with grpc.insecure_channel('localhost:6666') as channel:
            stub = pb2_grpc.ReportStub(channel)
            if check_coordinates(coordinates):
                message = pb2.Coordinates(coordinate1=int(coordinates[0]), coordinate2=int(coordinates[1]),
                                          coordinate3=float(coordinates[2]), coordinate4=int(coordinates[3]),
                                          coordinate5=int(coordinates[4]), coordinate6=float(coordinates[5]))
                response = stub.GetSpaceship(message)
                reports = [report for report in response.report]
                for report in reports:
                    try:
                        officers = [
                            {'first_name': officer.first_name, 'last_name': officer.last_name, 'rank': officer.rank} for
                            officer in list(report.officers)]
                        spaceship = Spaceship(alignment=report.alignment, name=report.name,
                                              length=round(report.length, 2),
                                              vessel_class=report.vessel_class, size=report.size, armed=report.armed,
                                              officers=officers)
                        SpaceshipValidator(**spaceship.__dict__())
                        print(js.MessageToJson(report))
                        self.recorder.insert_spaceship(spaceship)
                    except ValueError as v:
                        print('Spaceship is not valid')

    def scan(self, coordinates: List[str]):
        with grpc.insecure_channel('localhost:6666') as channel:
            stub = pb2_grpc.ReportStub(channel)
            if check_coordinates(coordinates):
                message = pb2.Coordinates(coordinate1=int(coordinates[0]), coordinate2=int(coordinates[1]),
                                          coordinate3=float(coordinates[2]), coordinate4=int(coordinates[3]),
                                          coordinate5=int(coordinates[4]), coordinate6=float(coordinates[5]))
                response = stub.GetSpaceship(message)
                reports = [report for report in response.report]
                enemy_spaceships = []
                allied_spaceships = []
                for report in reports:
                    try:
                        officers = [
                            {'first_name': officer.first_name, 'last_name': officer.last_name, 'rank': officer.rank} for
                            officer in list(report.officers)]
                        spaceship = Spaceship(alignment=report.alignment, name=report.name,
                                              length=round(report.length, 2),
                                              vessel_class=report.vessel_class, size=report.size, armed=report.armed,
                                              officers=officers)
                        SpaceshipValidator(**spaceship.__dict__())
                        print(js.MessageToJson(report))
                        self.recorder.insert_spaceship(spaceship)

                        if spaceship.alignment == 2:
                            enemy_spaceships.append(json.loads(js.MessageToJson(report)))
                        elif spaceship.alignment == 1:
                            allied_spaceships.append(json.loads(js.MessageToJson(report)))
                    except ValueError as v:
                        print('Spaceship is not valid')

                self.add_traitors(enemy_spaceships, allied_spaceships)
                for enemy_spaceship in enemy_spaceships:
                    for allied_spaceship in allied_spaceships:
                        try:
                            for enemy_officer in enemy_spaceship['officers']:
                                for allied_officer in allied_spaceship['officers']:
                                    if enemy_officer['firstName'] == allied_officer['firstName'] and enemy_officer[
                                        'lastName'] == allied_officer['lastName']:
                                        self.recorder.insert_traitor(enemy_officer)
                        except KeyError as k:
                            pass

    def add_traitors(self, enemy_spaceships: List[Dict], allied_spaceships: List[Dict]):
        if len(enemy_spaceships) > 0 and len(allied_spaceships) > 0:
            allied_spaceships[0]['officers'] = enemy_spaceships[0]['officers']

    def list_of_traitors(self):
        traitors = [dict(traitor) for traitor in self.recorder.get_traitors()]
        return json.dumps(traitors)


if __name__ == '__main__':
    client = ReportClient()
    client.run()

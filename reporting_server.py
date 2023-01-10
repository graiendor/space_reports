import random

import grpc
from concurrent import futures
import api_pb2_grpc as pb2_grpc
import api_pb2 as pb2
from internal.Spaceship import Spaceship


class ReportService(pb2_grpc.ReportServicer):
    def GetSpaceship(self, request, context):
        report = [spaceship for spaceship in self.spaceship_generator()]
        result = {
            'report': [{'alignment': spaceship.alignment.value, 'name': spaceship.name, 'length': spaceship.length,
                        'vessel_class': spaceship.vessel_class.value, 'size': spaceship.size, 'armed': spaceship.armed,
                        'officers': spaceship.officers} for spaceship in report]}
        return pb2.SpaceshipReport(**result)

    def spaceship_generator(self):
        for _ in range(random.randint(1, 10)):
            alignment = random.choice([Spaceship.Alignment.Ally, Spaceship.Alignment.Enemy])
            with open('data/spaceship_names.txt', 'r') as f:
                names = f.readlines()
            name = random.choice(names).strip()
            length = round(random.uniform(0, 6000), 2)
            vessel_class = random.choice(list(Spaceship.Vessel_class))
            size = random.randint(0, 500)
            armed = random.choice([True, False])
            with open('data/known_officers.txt', 'r') as f:
                officers = f.readlines()
            officers = random.sample(officers, random.randint(1, 5))
            ranks = ['Captain', 'Lieutenant', 'Commander', 'Ensign', 'Admiral']
            officers = [{'first_name': officer.split()[0], 'last_name': officer.split()[1],
                         'rank': random.choice(ranks)} for officer in officers]
            yield Spaceship(alignment=alignment, name=name, length=length, vessel_class=vessel_class, size=size,
                            armed=armed, officers=officers)


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ReportServicer_to_server(ReportService(), server)
    server.add_insecure_port('[::]:6666')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    run()

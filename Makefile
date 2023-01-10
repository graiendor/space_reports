all: build

clean:
	rm -rf *_pb2*

venv:
	python3.10 -m venv venv
	. venv/bin/activate; pip install -r requirements.txt

build: clean venv
	. venv/bin/activate; python -m grpc_tools.protoc -I=./proto --python_out=. --grpc_python_out=. ./proto/api.proto

server: build
	python reporting_server.py

client_1: build
	python reporting_client_v1.py 1 2 3.4 4 5 6.1

client_2: build
	python reporting_client_v2.py 1 2 3.4 4 5 6.1

client_3: build
	python reporting_client_v3.py scan 1 2 3.4 4 5 6.1
	python reporting_client_v3.py list_of_traitors


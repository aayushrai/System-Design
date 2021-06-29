CONDA_NAME := grpc-server
PYTHON_VERSION := 3.6

DOCKER_TAG := python-grpc-server

build-docker:
	docker build . -t $(DOCKER_TAG)

run-docker:
	docker run --rm -d -p 50051:50051 --name grpc-server $(DOCKER_TAG)

create-conda:
	conda env create -f environment.yml -n $(CONDA_NAME)

delete-conda:
	conda env remove -y -n $(CONDA_NAME)


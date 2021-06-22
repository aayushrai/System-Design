
DOCKER_TAG := face-recog-flask-server

build-docker:
	docker build . -t $(DOCKER_TAG)

run-docker:
	docker run --rm -d -p 5000:5000 --name grpc-server $(DOCKER_TAG)

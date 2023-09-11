GITHUB_USER=flexchar
IMAGE_NAME=instructor-embedding-api
CONTAINER_NAME=instructor-embedding-api

CONTAINER_ID = $$(docker ps -f name=${CONTAINER_NAME} -q -n 1)

build:
	docker build --platform linux/amd64 -t $(IMAGE_NAME) .

build-local:
	docker build -t $(IMAGE_NAME) .

run:
	docker run --rm -p 8000:8000 --name $(CONTAINER_NAME) $(IMAGE_NAME)

debug-run:
	docker build -t $(IMAGE_NAME) . && docker run --rm -it -p 8000:8000 $(IMAGE_NAME)

push:
	docker tag $(IMAGE_NAME) ghcr.io/$(GITHUB_USER)/$(IMAGE_NAME)
	docker push ghcr.io/$(GITHUB_USER)/$(IMAGE_NAME)
tag:
	docker tag $(IMAGE_NAME) ghcr.io/$(GITHUB_USER)/$(IMAGE_NAME)

up:
	docker compose -p $(CONTAINER_NAME) up -d
	
up-build:
	docker compose -p $(CONTAINER_NAME) up -d --build

down:
	docker compose -p $(CONTAINER_NAME) down

shell:
	docker exec -it $(CONTAINER_ID) bash -l

logs:
	docker logs $(CONTAINER_ID) -f
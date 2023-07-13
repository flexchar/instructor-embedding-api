GITHUB_USER=flexchar
IMAGE_NAME=instructor-embedding-api
CONTAINER_NAME=instructor-embedding-api

build:
	docker build --platform amd64 -t $(IMAGE_NAME) .

run:
	docker run --rm -p 8000:8000 --name $(CONTAINER_NAME) $(IMAGE_NAME)

push:
	docker tag $(IMAGE_NAME) ghcr.io/$(GITHUB_USER)/$(IMAGE_NAME)
	docker push ghcr.io/$(GITHUB_USER)/$(IMAGE_NAME)
tag:
	docker tag $(IMAGE_NAME) ghcr.io/$(GITHUB_USER)/$(IMAGE_NAME)

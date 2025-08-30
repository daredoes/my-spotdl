DOCKER_IMAGE=spotdl
DOCKER_REPO=daredoes
TAG_NAME=$(shell date +%Y.%m.%d.%H.%M.%S)
PLATFORMS=linux/amd64,linux/arm64
TAG_NAME_TO_RUN=2025.08.30.00.11.28

run:
	docker run -d \
    --privileged \
    -v /Users/dare/Python/spotdl/music:/music \
    -v /Users/dare/Python/spotdl/data:/data/spotdl \
    $(DOCKER_REPO)/$(DOCKER_IMAGE):$(TAG_NAME_TO_RUN)

build:
	docker buildx build --platform=$(PLATFORMS) -t $(DOCKER_REPO)/$(DOCKER_IMAGE):$(TAG_NAME) .
push:
	make build && docker push $(DOCKER_REPO)/$(DOCKER_IMAGE):$(TAG_NAME)
push-premade:
	docker push $(DOCKER_REPO)/$(DOCKER_IMAGE):$(TAG_NAME_TO_RUN)

.PHONY: build push 

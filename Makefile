SNAME ?= FlaskApp
NAME ?= elswork/FlaskApp
PORT ?= 5000:5000
ARCH ?= amd64
ARCH2 ?= arm32v7

# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

# DOCKER TASKS
# Build the container
build: ## Build the container
	docker build --no-cache -t $(NAME):$(ARCH) --build-arg BUILD_DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"` \
	--build-arg VCS_REF=`git rev-parse --short HEAD` \
	--build-arg VERSION=$(ARCH)-`cat VERSION` . > ../builds/$(SNAME)_$(ARCH)_`date +"%Y%m%d_%H%M%S"`.txt
tag: ## Tag the container
	docker tag $(NAME):$(ARCH) $(NAME):$(ARCH)-`cat VERSION`
push: ## Push the container
	docker push $(NAME):$(ARCH)-`cat VERSION`
	docker push $(NAME):$(ARCH)	
deploy: build tag push
manifest: ## Manifest the container
	docker manifest create $(NAME):`cat VERSION` $(NAME):$(ARCH)-`cat VERSION` \
	$(NAME):$(ARCH2)-`cat VERSION-$(ARCH2)`
	docker manifest push --purge $(NAME):`cat VERSION`
	docker manifest create $(NAME):latest $(NAME):$(ARCH) $(NAME):$(ARCH2)
	docker manifest push --purge $(NAME):latest
start: ## Start the container
	docker run -it -p $(NAME) $(NAME):$(ARCH)

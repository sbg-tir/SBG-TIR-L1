SBG_VERSION=0.01
DOCKER_BASE_VERSION=20250214
AFIDS_CONDA_PACKAGE=/home/smyth/Local/afids-conda-package
SBG_SOURCE=/home/smyth/Local/sbg-l1
BASE_DOCKER=oraclelinux:8

# Create environment with base conda/geocal environment installed
create-base:
	docker run -t -d --cidfile=docker_run.id -v $(AFIDS_CONDA_PACKAGE):/home/afids-conda-package:Z -v $(SBG_SOURCE):/home/sbg-l1 $(BASE_DOCKER) /bin/bash
	docker exec $$(cat docker_run.id) bash --login -c "dnf install -y make csh && cd /home/sbg-l1/env && make ENV_DIR=/home/sbg-env CONDA_FIXED=yes CONDA_PACKAGE_DIR=/home/afids-conda-package/afids-conda-channel create-env && /home/sbg-env/bin/conda init"
	docker commit $$(cat docker_run.id) sbg-tir-l1/conda-base:$(DOCKER_BASE_VERSION)
	docker container stop $$(cat docker_run.id)
	rm docker_run.id

create-sbg:
	docker run -t -d --cidfile=docker_run.id -v $(SBG_SOURCE):/home/sbg-l1 sbg-tir-l1/conda-base:$(DOCKER_BASE_VERSION) /bin/bash
	docker exec $$(cat docker_run.id) bash --login -c "mkdir /home/sbg-l1-build && cd /home/sbg-l1-build && ../sbg-l1/configure --prefix=/home/sbg-env && make -j 20 all && make install && rm -r /home/sbg-l1-build /home/afids-conda-package"
	docker commit $$(cat docker_run.id) sbg-tir-l1/sbg-tir-l1:$(SBG_VERSION)
	docker container stop $$(cat docker_run.id)
	rm docker_run.id
	docker save sbg-tir-l1/sbg-tir-l1:$(SBG_VERSION) | pigz > sbg-tir-l1-docker-$(SBG_VERSION).tar.gz

# Rule to start a interactive docker instance, just so I don't need to
# remember the syntax
docker-start:
	docker run -it -v $(AFIDS_CONDA_PACKAGE):/home/afids-conda-package:Z -v $(SBG_SOURCE):/home/sbg-l1 $(BASE_DOCKER) /bin/bash

# Start the base version, with conda/geocal installed
docker-start2:
	docker run -it -v $(SBG_SOURCE):/home/sbg-l1 sbg-tir-l1/conda-base:$(DOCKER_BASE_VERSION) /bin/bash

# Start with installed version
docker-start3:
	docker run -it -v $(SBG_SOURCE):/home/sbg-l1 sbg-tir-l1/sbg-tir-l1:$(SBG_VERSION) /bin/bash

# When a failure occurs, can connect to the docker instance used in a rule
docker-connect:
	docker exec -it $$(cat docker_run.id) bash --login

# If we have a failure and want to start with a new container, this
# stops the old one and removes the docker_run.id file
docker-cleanup:
	docker container stop $$(cat docker_run.id)
	rm docker_run.id

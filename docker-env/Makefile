SBG_VERSION=0.01
DOCKER_BASE_VERSION=20250214
AFIDS_CONDA_PACKAGE=/home/smyth/Local/afids-conda-package
SBG_SOURCE=/home/smyth/Local/sbg-l1
BASE_DOCKER=oraclelinux:8

# Location of various datasets, just used to run docker image (no impact on docker
# image itself)
SBG_ANCILLARY=/home/smyth/sandbox/sbg_ancillary
AFIDS_DATA_ELEV_ROOT=$(SBG_ANCILLARY)/srtm_v3_dem_L2
AFIDS_DATA_LWM=$(SBG_ANCILLARY)/srtm_v3_lwm
AFIDS_DATA_SPICEDATA=$(SBG_ANCILLARY)/cspice
AFIDS_DATA_ORTHO=$(SBG_ANCILLARY)/ortho_lsat7
SBG_OSP_DIR=$(SBG_ANCILLARY)/l1_osp_dir

# Include a Makefile.local to override things, if found
-include Makefile.local

# Create environment with base conda/geocal environment installed
create-base:
	docker run -t -d --cidfile=docker_run.id -v $(AFIDS_CONDA_PACKAGE):/home/afids-conda-package:Z -v $(SBG_SOURCE):/home/sbg-l1:Z $(BASE_DOCKER) /bin/bash
	-cp ../env/Makefile.local ../env/Makefile.local.backup
	docker exec $$(cat docker_run.id) bash --login -c "dnf install -y make csh wget && cd /home/sbg-l1/env && cp /home/sbg-l1/docker-env/env_makefile.local Makefile.local && make create-env && /home/sbg-env/bin/conda init && mkdir -p /data/sbg_ancillary/srtm_v3_dem_L2 /data/sbg_ancillary/srtm_v3_dem_lwm /data/sbg_ancillary/cspice /data/sbg_ancillary/ortho_lsat7 /data/sbg_ancillary/l1_osp_dir && mkdir -p /opt/afids && ln -s /data/sbg_ancillary /opt/afids/data && mkdir -p /home/smyth/sandbox && ln -s /data/sbg_ancillary /home/smyth/sandbox && rm Makefile.local"
	-mv ../env/Makefile.local.backup ../env/Makefile.local
	docker commit $$(cat docker_run.id) sbg-tir-l1/conda-base:$(DOCKER_BASE_VERSION)
	docker container stop $$(cat docker_run.id)
	rm docker_run.id

create-sbg:
	docker run -t -d --cidfile=docker_run.id -v $(SBG_SOURCE):/home/sbg-l1:Z sbg-tir-l1/conda-base:$(DOCKER_BASE_VERSION) /bin/bash
	docker exec $$(cat docker_run.id) bash --login -c "mkdir /home/sbg-l1-build && cd /home/sbg-l1-build && ../sbg-l1/configure --prefix=/home/sbg-env && make -j 20 all && make install && rm -r /home/sbg-l1-build /home/afids-conda-package"
	docker commit $$(cat docker_run.id) sbg-tir-l1/sbg-tir-l1:$(SBG_VERSION)
	docker container stop $$(cat docker_run.id)
	rm docker_run.id
	docker save sbg-tir-l1/sbg-tir-l1:$(SBG_VERSION) | pigz > sbg-tir-l1-docker-$(SBG_VERSION).tar.gz

# Rule to start a interactive docker instance, just so I don't need to
# remember the syntax
docker-start:
	docker run -it -v $(AFIDS_CONDA_PACKAGE):/home/afids-conda-package:Z -v $(SBG_SOURCE):/home/sbg-l1:Z $(BASE_DOCKER) /bin/bash

# Start the base version, with conda/geocal installed
docker-start2:
	docker run -it -v $(SBG_SOURCE):/home/sbg-l1:Z sbg-tir-l1/conda-base:$(DOCKER_BASE_VERSION) /bin/bash

# Start with installed version
docker-start3:
	docker run -it -v $(SBG_SOURCE):/home/sbg-l1:Z -v $(AFIDS_DATA_ELEV_ROOT):/data/sbg_ancillary/srtm_v3_dem_L2:Z -v $(AFIDS_DATA_LWM):/data/sbg_ancillary/srtm_v3_dem_lwm -v $(AFIDS_DATA_SPICEDATA):/data/sbg_ancillary/cspice:Z -v $(AFIDS_DATA_ORTHO):/data/sbg_ancillary/ortho_lsat7:Z -v $(SBG_OSP_DIR):/data/sbg_ancillary/l1_osp_dir:Z sbg-tir-l1/sbg-tir-l1:$(SBG_VERSION) /bin/bash

# When a failure occurs, can connect to the docker instance used in a rule
docker-connect:
	docker exec -it $$(cat docker_run.id) bash --login

# If we have a failure and want to start with a new container, this
# stops the old one and removes the docker_run.id file
docker-cleanup:
	docker container stop $$(cat docker_run.id)
	rm docker_run.id

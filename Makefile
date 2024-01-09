APP_PORT := 5000
DOCKER_TAG := latest
DOCKER_IMAGE := planets

DEPLOY_HOST := demo_host
KEY_FILE := ~/.ssh/id_rsa
DVC_REMOTE_NAME := my_remote

.PHONY: *
run_app:
	python3 -m uvicorn app:create_app --host='0.0.0.0' --port=$(APP_PORT)

install:
	pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html

download_weights:
	dvc pull -R weights

run_unit_tests:
	PYTHONPATH=. pytest tests/unit/

run_integration_tests:
	PYTHONPATH=. pytest -s tests/integration/

run_all_tests:
	make run_unit_tests
	make run_integration_tests

generate_coverage_report:
	PYTHONPATH=. pytest --cov=src --cov-report html  tests/

lint:
	flake8 src/


build:
	docker build -f Dockerfile . --force-rm=true -t $(DOCKER_IMAGE):$(DOCKER_TAG)


deploy:
	ansible-playbook -i deploy/ansible/inventory.ini  deploy/ansible/deploy.yml --key-file ~/.ssh/id_rsa\
		-e host=$(DEPLOY_HOST) \
		-e docker_image=$(DOCKER_IMAGE) \
		-e docker_tag=$(DOCKER_TAG) \
		-e docker_registry_user=$(CI_REGISTRY_USER) \
		-e docker_registry_password=$(CI_REGISTRY_PASSWORD) \
		-e docker_registry=$(CI_REGISTRY) \


destroy:
	ansible-playbook -i deploy/ansible/inventory.ini deploy/ansible/destroy.yml --key-file ~/.ssh/id_rsa\
		-e host=$(DEPLOY_HOST)

install_dvc:
	pip install pygit2==1.10.1 pathspec==0.9.0
	pip install dvc[ssh]==2.5.4


init_dvc:
	dvc init --no-scm -f
	dvc remote add --default $(DVC_REMOTE_NAME) ssh://91.206.15.25/home/a.kondakov/dvc_files
	dvc remote modify $(DVC_REMOTE_NAME) user $(USERNAME)
	dvc config cache.type hardlink,symlink

install_c_libs:
	apt-get update && apt-get install -y --no-install-recommends gcc ffmpeg libsm6 libxext6
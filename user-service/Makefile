# Makefile - User Service (Flask Microservice)

SERVICE_NAME = user-service
IMAGE_NAME = bamolitho/$(SERVICE_NAME)
CONTAINER_NAME = $(SERVICE_NAME)-container

.PHONY: venv-setup venv-activate install run test docker-build docker-run docker-stop docker-clean github github-msg clean clean-pyc tree help

# ===========
# ENV SETUP
# ===========
venv-setup:
	python -m venv venv
	bash -c "source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt && pip freeze > requirements-dev.txt"

venv-activate:
	@echo "Pour activer le venv, exécutez:"
	@echo "source venv/bin/activate"

install:
	bash -c "source venv/bin/activate && pip install -r requirements.txt"

# ===========
# RUN & TEST
# ===========
run:
	bash -c "source venv/bin/activate && python app/app.py"

test:
	bash -c "source venv/bin/activate && pytest -v --disable-warnings"

# ===========
# DOCKER
# ===========
docker-build:
	docker build -t $(IMAGE_NAME):latest .

docker-run:
	docker run -d -p 5201:5201 --name $(CONTAINER_NAME) $(IMAGE_NAME):latest

docker-stop:
	docker stop $(CONTAINER_NAME) || true && docker rm $(CONTAINER_NAME) || true

docker-logs:
	docker logs -f $(CONTAINER_NAME)

docker-clean:
	docker rmi $(IMAGE_NAME):latest || true

# ===========
# GIT
# ===========
github:
	git add .
	git commit -m "Update $(SERVICE_NAME) microservice"
	git push

github-msg:
	@read -p "Message de commit: " msg; \
	git add .; \
	git commit -m "$$msg"; \
	git push

# ===========
# CLEANING
# ===========
clean:
	rm -rf venv requirements-dev.txt

clean-pyc:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

# ===========
# UTILS
# ===========
tree:
	@echo "Project Structure ($(SERVICE_NAME)):"
	@echo "===================================="
	@tree -I '__pycache__|*.pyc|venv|__init__.py' -L 5 2>/dev/null || \
	(ls -R | grep ":$$" | sed -e 's/:$$//' -e 's/[^-][^\/]*\//--/g' -e 's/^/   /' -e 's/-/|/')

help:
	@echo "Commandes disponibles pour $(SERVICE_NAME):"
	@echo "  make venv-setup     - Créer venv et installer dépendances"
	@echo "  make venv-activate  - Instructions pour activer venv"
	@echo "  make install        - Installer dépendances"
	@echo "  make run            - Lancer l'application Flask"
	@echo "  make test           - Lancer les tests Pytest"
	@echo "  make docker-build   - Construire l'image Docker"
	@echo "  make docker-run     - Démarrer le conteneur"
	@echo "  make docker-stop    - Arrêter/Supprimer le conteneur"
	@echo "  make docker-clean   - Supprimer l'image Docker"
	@echo "  make github         - Commit/push auto"
	@echo "  make github-msg     - Commit/push manuel"
	@echo "  make clean          - Supprimer le venv"
	@echo "  make clean-pyc      - Supprimer les fichiers Python"
	@echo "  make tree           - Afficher la structure"

# ====================================================
# Makefile - Global Orchestrator for all Microservices
# ====================================================

SERVICES = user-service product-service

.PHONY: help build-all run-all stop-all test-all clean-all docker-build-all docker-clean-all push-all tree github github-msg

# ===========
# GLOBAL COMMANDS
# ===========
help:
	@echo "Commandes globales disponibles :"
	@echo "  make build-all        - Construire tous les environnements virtuels (venv)"
	@echo "  make run-all          - Lancer tous les services Flask localement"
	@echo "  make stop-all         - Stopper tous les conteneurs Docker"
	@echo "  make test-all         - Lancer les tests de tous les services"
	@echo "  make docker-build-all - Construire toutes les images Docker"
	@echo "  make docker-clean-all - Supprimer toutes les images Docker"
	@echo "  make push-all         - Commit & push de tous les services"
	@echo "  make clean-all        - Nettoyer venv, pycache, images"
	@echo "  make tree             - Afficher la structure complète"
	@echo "  make github           - Pousser sur github avec le message par défaut"
	@echo "  make github-msg       - Pousser sur github avec un message personnalisé"

# ===========
# BUILD / INSTALL
# ===========
build-all:
	@for s in $(SERVICES); do \
		echo "⚙️  [$$s] Setup du venv et installation..."; \
		$(MAKE) -C $$s venv-setup; \
	done

# ===========
# RUN LOCALLY (dev mode)
# ===========
run-all:
	@echo "🚀 Lancement des microservices Flask..."
	@for s in $(SERVICES); do \
		echo "▶️  Démarrage de $$s..."; \
		( cd $$s && nohup bash -c "source venv/bin/activate && python app/app.py" > ../$$s.log 2>&1 & ); \
	done
	@echo "✅ Tous les services sont lancés. Consulte les logs *.log"

# ===========
# TESTS
# ===========
test-all:
	@for s in $(SERVICES); do \
		echo "🧪 [$$s] Exécution des tests..."; \
		$(MAKE) -C $$s test; \
	done

# ===========
# DOCKER
# ===========
docker-build-all:
	@for s in $(SERVICES); do \
		echo "🐳 [$$s] Construction de l'image Docker..."; \
		$(MAKE) -C $$s docker-build; \
	done

docker-clean-all:
	@for s in $(SERVICES); do \
		echo "🧹 [$$s] Suppression des images Docker..."; \
		$(MAKE) -C $$s docker-clean; \
	done

# ===========
# GIT
# ===========
push-all:
	@for s in $(SERVICES); do \
		echo "📤 [$$s] Commit & push..."; \
		$(MAKE) -C $$s github; \
	done

# ===========
# CLEANUP
# ===========
clean-all:
	@for s in $(SERVICES); do \
		echo "🧹 [$$s] Nettoyage des fichiers temporaires..."; \
		$(MAKE) -C $$s clean clean-pyc; \
	done

stop-all:
	@for s in $(SERVICES); do \
		echo "🛑 [$$s] Arrêt des conteneurs..."; \
		$(MAKE) -C $$s docker-stop; \
	done

# ===========
# UTILITAIRE
# ===========
tree:
	@echo "🗂 Structure complète du projet hello-microservices :"
	@echo "====================================================="
	@tree -I '__pycache__|venv|*.pyc|*.log|.git' -L 6 2>/dev/null || \
	(ls -R | grep ":$$" | sed -e 's/:$$//' -e 's/[^-][^\/]*\//--/g' -e 's/^/   /' -e 's/-/|/')

# Pousser sur github
github:
	git add .
	git commit -m "[PHASE 5] Tutos complet CI/CD ici 👉 https://github.com/Bamolitho/InsideCI-CD"
	git push

# Pousser avec message personnalisé
github-msg:
	@read -p "Message de commit: " msg; \
	git add .; \
	git commit -m "$$msg"; \
	git push


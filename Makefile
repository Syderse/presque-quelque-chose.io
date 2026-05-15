# File: Makefile
# Context: System Context Section 6 (Development Protocols)

# Raccourci de développement
# Charge les variables d'environnement depuis .env.local puis lance le Hugo épinglé du projet
# Utilise --disableFastRender pour garantir la génération JIT de Tailwind
dev:
	@bash -c 'if [ -f .env.local ]; then set -a; source .env.local; set +a; fi; pnpm exec hugo server --disableFastRender'

# Build de Production (Conforme Section 6)
# Note: Le minify CSS interne doit être désactivé dans layouts/partials/css.html
build:
	pnpm exec hugo --gc --minify

# Nettoyage profond (Utile si Tailwind semble "bloqué")
clean:
	rm -rf public resources
	pnpm exec hugo mod clean

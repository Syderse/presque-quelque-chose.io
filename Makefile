# File: Makefile
# Context: System Context Section 6 (Development Protocols)

# Raccourci de développement (correspond à votre "pnpm dev")
# Utilise --disableFastRender pour garantir la génération JIT de Tailwind
dev:
	hugo server --disableFastRender

# Build de Production (Conforme Section 6)
# Note: Le minify CSS interne doit être désactivé dans layouts/partials/css.html
build:
	hugo --gc --minify

# Nettoyage profond (Utile si Tailwind semble "bloqué")
clean:
	rm -rf public resources
	hugo mod clean
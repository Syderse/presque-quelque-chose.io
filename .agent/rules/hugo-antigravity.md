---
trigger: always_on
---

# Hugo Blox Rules (Antigravity)

## Source de Vérité
- **Toujours consulter** [system_context.md](cci:7://file:///Users/mathieu/Documents/presque-quelque-chose.io/system_context.md:0:0-0:0) avant d'agir.
- En cas de doute sur un fichier, analyser son contenu complet.

## Architecture Hugo
- **Logic** → `layouts/`
- **Contenu** → `content/` (Markdown)
- **Config** → `hugo.yaml`
- Respecter l'architecture en couches (Layers 0-3) du `baseof.html`.

## Tailwind v4 & CSS
- **Config** : Pas de `tailwind.config.js`. Utiliser `@theme` dans le CSS.
- **Syntaxe** : Nesting CSS natif, pas d'abus de `@apply`.
- **CRITIQUE** : Ne **jamais** appliquer `| minify` au pipe CSS en production.
- **Perf** : Cibler 60FPS — limiter les effets. 
## JavaScript
- Vanilla ES6+ uniquement.
- Scripts dans `assets/js/`, chargés via `js-loader.html`.

## Visuel
- Couleurs toujours visibles par défaut (pas seulement au hover).
- Thème : Catppuccin Mocha.
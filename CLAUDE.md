# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

`presque-quelque-chose` est un site personnel **Hugo** (français) : un « cabinet de curiosités » dense et littéraire — textes longs, carnets, recherches académiques, objets audio/vidéo, rhizome de liens, forum maison, almanach pataphysique. **Ce n'est pas un blog linéaire.** Le contenu est l'œuvre ; l'UI est au service du texte.

## Commands

```sh
# Dév local (charge .env.local, Hugo épinglé du projet). JAMAIS `hugo` global.
make dev            # = pnpm dev = pnpm exec hugo server --disableFastRender

# Build de prod
make build          # = pnpm exec hugo --gc --minify
pnpm exec hugo --gc --minify --cleanDestinationDir --printPathWarnings   # build de vérif complet

make clean          # rm -rf public resources && hugo mod clean (si Tailwind semble bloqué)

# Veille radiophonique (projet Python séparé, hors site)
cd antenne_radio && make test      # tests pytest ; make run ; make export-public
```

- Toujours commencer par `git status --short` ; le worktree peut contenir un chantier en cours.
- Vérifier le build après toute modification de gabarit/CSS/build.
- Hugo Extended `0.160.1` est épinglé via `pnpm exec hugo`. Netlify l'utilise aussi (pas de `HUGO_VERSION` dans `netlify.toml`).
- Privilégie toujours si possible les solutions hugoesques (hugo native) pour assurer la robustesse et la performance speedy lightweight.

## Architecture (le non-évident)

- **Sorties JSON custom = API statique.** Trois `outputFormats` dans `config/_default/hugo.yaml` produisent des endpoints consommés par du JS : `RANDOMIZER` → `/articles-aleatoires.json` (article au hasard), `RHIZOME` → `/rhizome-curieux/index.json` (graphe), `ALMANACH` → `/almanach/index.json`. **`ALMANACH` est déclaré uniquement dans `content/almanach/_index.md`** ; ne jamais le remettre dans `outputs.section`. Après build : `public/almanach/index.json` doit exister, `public/almanach/index.html` ne doit PAS exister.
- **Données build-time.** `data/almanach.yaml` et `static/data/*.json` (dom-story, pataphysique) sont lus au build/runtime ; `static/antenne-radio/index.json` est rendu côté serveur (`readFile | transform.Unmarshal`) — c'est une **whitelist auditée**, n'ajouter aucun champ.
- **Moteurs JS vanilla, chargés par page** (via `layouts/partials/functions/js-loader.html`), pas globalement : `PataphysicalDate.js`, `almanach.js`, `dom-engine.js`, `rhizome-engine.js` (+ D3), `patafoin.js` (+ Supabase), `antenne-radio.js`, `sidenote-adjuster.js`.
- **Sidenotes Tufte** via `layouts/shortcodes/sidenote.html` (variantes `note` / `comment`) — utilisées massivement dans le contenu. La syntaxe `{{< sidenote >}}` ne doit jamais casser.
- **Forum Patafoin** : Supabase (`HUGO_PARAMS_SUPABASE_URL` / `_KEY` via `.env.local`, fallback params). Tables `topics` / `posts`.
- **`_vendor/`** contient des correctifs locaux Hugo Blox : toute régénération peut les écraser, prudence.
- **`netlify.toml`** porte la CSP, les headers de sécurité/perf et les redirects SEO. Si un embed/API casse en prod, vérifier la CSP. Pagefind est indexé après build (étape Netlify).
- **`antenne_radio/`** (Python) est un projet séparé qui moissonne et exporte le JSON whitelisté — **hors périmètre du site** ; seul son rendu Hugo nous concerne.
- Doc de reprise détaillée : `docs/AGENTS.md` (config à ne pas casser), `docs/HISTORIQUE.md` (archéologie), `docs/CHANTIERS.md` (tâches).

## Direction & principes UI (LOI DURABLE)

Le site est en **refonte vers un idéal ultra-typographique** — esprit (souple, pas dogmatique) de bestmotherfucking.website. Le plan et les prompts vivent dans **`docs/refonte-typeheavy/`**. Décisions verrouillées (2026-06) :

| | Cible |
|---|---|
| Palette | **Fond clair, texte quasi-noir**, haut contraste |
| Corps | **Serif système** (Charter/Georgia/Times…) |
| CSS/build | **Un seul CSS écrit à la main** (`assets/css/site.css`), **sans Tailwind ni Hugo Blox** |
| Accueil | Index typographique pur |
| DOM | **Sacré** : le bouton-récit (000→999, `dom-story.json`, pierre tombale) reconverti, jamais supprimé |
| Layout | **Limité et centré** (`max-width: ~40em-45em`), respirant, responsive par défaut |

**Principes web/UI à respecter pour toute intervention sur l'UI** (et à ne PAS contredire en réintroduisant l'ancien maximalisme) :

1. **Contrastes francs, jamais de gris baveux.** Texte quasi-noir sur fond clair. Pour distinguer un texte secondaire : taille, graisse, italique, petites capitales, filets — **jamais** une couleur grise délavée.
2. **Aucune fonte distante.** Stacks système uniquement. Pas de `fonts.googleapis.com`, pas de `@import url(...)`.
3. **Léger et rapide, même rendu partout.** HTML sémantique, CSS minimal, JS quasi nul. Pas d'effets fragiles, de dépendances exotiques, de CDN si on peut auto-héberger.
4. **Rien ne doit gêner le texte.** Le texte est le héros ; tout le reste se tait.
5. **Sobriété d'animation.** Limiter aux `opacity`/`transform`/couleurs/bordures. Bannir animations infinies décoratives, `transition-all`, `will-change` permanent, gros `filter`/`backdrop-blur`/`drop-shadow`.
6. **Ne charger une image que si elle porte un contenu réel.** Préférer le CSS et la typographie.
7. **Confort de lecture strict.** Interlignage aéré (`line-height` ~1.5–1.6 pour le corps, ~1.2 pour les titres) et lignes courtes (max ~80 caractères) pour ne pas fatiguer l'œil.
8. **Cache et compression au cœur.** Configuration agressive des headers de cache et compression (Gzip/Brotli) via `netlify.toml` ; pas de gaspillage de bande passante.

Quand tu touches à l'UI : tends vers ces principes, n'en ré-éloigne pas le site. En cas de doute esthétique, choisis la version la plus simple, la plus lisible, la plus légère.

## Règles d'or quand tu édites

- **Le contenu est sacré.** Ne jamais modifier `content/**/*.md`, `data/`, `static/data/`, `static/antenne-radio/index.json` sauf demande explicite. On refond l'UI (layouts, CSS, JS, build), pas les textes. Préserver les URLs accentuées (`/blog_coree/`) et les front matters.
- **Préserver les endpoints & la discipline.** Sorties JSON (ALMANACH/RANDOMIZER/RHIZOME), RSS, whitelist antenne radio, redirects SEO, CSP. Si on retire un domaine (fonte, CDN), **adapter** la CSP de `netlify.toml`, ne pas la casser.
- **Mesurer avant/après** dès qu'on touche `static/`, `_vendor/`, le CSS généré, les embeds ou le pipeline : `du -sh .git static _vendor public`, poids CSS/JS, présence des endpoints.
- **Hugo récent** : `build` (pas `_build`), `cascade.target`, `files`, `locale`, `hugo.Data`, parcours via `hugo.Sites` (pas `site.AllPages`). Détails dans `docs/AGENTS.md` › « Configuration A Ne Pas Casser ».
- **Liens internes** : toujours `[texte](/chemin/de/contenu/#ancre)` — le render hook (`layouts/_markup/render-link.html`) résout via `GetPage` → permalien canonique (dé-accentuation, validation). Ne jamais écrire `{{< relref … >}}` ni de chemins relatifs `../`.
- **Commits** petits, testés, réversibles ; un sujet par commit. Ne jamais masquer un build ou un test échoué.
- **Style** : non catégorique aux emojis et aux tirets cadratins. Attention à la casse, évite de mettre des majuscules partout comme en anglais. 
- **Autant que possible** : fais des suggestions de modifications ou d'autres manières de faire qui te semblent meilleures par rapport à ma demande et suggère les en me posant des questions avant exécution si tu juges cela pertinent.

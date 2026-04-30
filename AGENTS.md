# System Context: presque-quelque-chose.io

**Version :** 7.0, reprise profonde  
**Dernier audit :** 2026-04-28  
**Stack local observee :** Hugo Extended `v0.160.1`, pnpm `10.14.0`, Tailwind CSS v4, Hugo Blox vendorie, D3.js, Supabase, ESBuild via Hugo Pipes  
**But du fichier :** servir de carte de reprise. Avant de changer le site, lire ce fichier, puis confirmer l'etat reel avec `git status --short` et les fichiers sources.

---

## 1. Intention Du Site

`presque-quelque-chose.io` est un site personnel construit comme un petit systeme d'exploration : textes longs, carnets, travaux academiques, objets audio/video, liens curieux, forum maison, almanach et tableau de bord vivant.

Le site n'est pas un blog lineaire seulement. Il fonctionne plutot comme :

- une vitrine textuelle dense ;
- un inventaire d'objets et de series ;
- un laboratoire d'interfaces un peu particulieres ;
- un espace ou les textes peuvent garder leurs details, leurs notes, leurs bizarreries et leurs chemins de traverse.

Rappel editorial local :

- quand le travail part de notes, ne pas perdre les idees originales ;
- rester proche de l'esprit des images, souvenirs, carnets et documents sources ;
- etoffer si utile, mais ne pas remplacer la precision par une pluie d'adjectifs ;
- montrer plutot que dire ;
- partir du concret ;
- remplacer le jugement par le detail ;
- faire confiance au lecteur ;
- privilegier les scenes, les actions, les contradictions et les details oddly specific ;
- utiliser les notes de bas de page pour expliquer simplement les references precises sans alourdir la scene.

---

## 2. Etat Technique Actuel

Le projet est une base Hugo Blox tres personnalisee. La structure Hugo Blox reste presente, mais les vues importantes sont maintenant locales dans `layouts/`, avec une direction graphique et des comportements propres au site.

Points importants au 2026-04-28 :

- Hugo local est recent : `hugo v0.160.1+extended+withdeploy`.
- Netlify est maintenant epingle dans `netlify.toml` sur `HUGO_VERSION = "0.160.1"`, aligne avec le poste local et au-dessus du correctif Hugo `0.159.2` pour CVE-2026-35166.
- Les corrections de deprecations Hugo recentes ont ete faites dans le code local et dans plusieurs fichiers du module vendorie Hugo Blox sous `_vendor/`.
- `content/almanach/_index.md` utilise maintenant `build`, pas `_build`.
- `cascade._target` est devenu `cascade.target`.
- `includeFiles` est devenu `files` dans les mounts de module.
- `languageCode` est devenu `locale`.
- Les usages locaux qui declenchaient les avertissements `.Site.Data` et `site.AllPages` ont ete remplaces par `hugo.Data` et un parcours via `hugo.Sites`.
- Le format `ALMANACH` n'est plus declare globalement pour toutes les sections. Il est porte uniquement par `content/almanach/_index.md`.
- `public/almanach/index.html` ne doit pas exister apres un build propre ; l'endpoint attendu est `public/almanach/index.json`.

Attention Git :

- Le dossier `content/solutions-imaginaires/blog_corée/` est actuellement non suivi dans Git lors de cet audit, mais Hugo le voit et le publie deja.
- L'alias `git save "message"` ajoute tout, commit, puis push. Il embarquera donc aussi ce dossier non suivi.

---

## 3. Carte Des Fichiers

Racines utiles :

- `config/_default/hugo.yaml` : configuration Hugo principale.
- `layouts/` : templates locaux qui prennent le dessus sur Hugo Blox.
- `assets/css/main.css` : point d'entree Tailwind v4 et CSS de tout le design.
- `assets/js/` : moteurs JS locaux charges par Hugo Pipes.
- `content/` : corpus Markdown.
- `data/almanach.yaml` : base de donnees de l'almanach.
- `static/media/` : images servies telles quelles.
- `static/data/dom-story.json` : donnees narratives du widget DOM.
- `hugo-blox/` : blocs locaux importes par mount.
- `_vendor/` : modules Hugo Blox vendories, avec quelques correctifs locaux de compatibilite Hugo.
- `netlify.toml` : build de production, headers, redirects et Pagefind.
- `Makefile` et `package.json` : commandes de dev/build.

Fichiers a lire en priorite avant une intervention :

- Shell global : `layouts/_default/baseof.html`
- Articles : `layouts/_default/single.html`
- Accueil : `layouts/index.html`
- CSS : `layouts/partials/css.html` et `assets/css/main.css`
- JS loader : `layouts/partials/functions/js-loader.html`
- SEO : `layouts/partials/seo.html`
- Sidebar/mobile : `layouts/partials/sidebar.html`, `layouts/partials/mobile-nav.html`
- Footer article : `layouts/partials/article-footer.html`
- Notes laterales : `layouts/shortcodes/sidenote.html`, `assets/js/sidenote-adjuster.js`

---

## 4. Configuration Hugo

Dans `config/_default/hugo.yaml` :

- `title`: `presque-quelque-chose`
- `baseURL`: `https://www.presque-quelque-chose.com/`
- `locale`: `fr-fr`
- `defaultContentLanguage`: `fr`
- `removePathAccents: true`, donc `blog_corée` devient `blog_coree` dans les URLs.
- `build.writeStats: true`, indispensable pour Tailwind JIT.
- `security.enableInlineShortcodes: true`.
- `minify.disableXML: true` et `minify.minifyOutput: true`.

Modules et mounts :

- mounts standards : `assets`, `layouts`, `content`, `static`.
- pas de mount pour `hugo_stats.json`, afin d'eviter les erreurs de cold build Netlify.
- mounts locaux Hugo Blox :
  - `hugo-blox/blox/community` vers `layouts/_partials/blox/community/`
  - `hugo-blox/blox/all-access` vers `layouts/_partials/blox/`
  - `hugo-blox/blox` vers `assets/dist/community/blox/`
- imports Go :
  - `github.com/HugoBlox/hugo-blox-builder/modules/blox-plugin-netlify`
  - `github.com/HugoBlox/hugo-blox-builder/modules/blox-tailwind`

Formats de sortie :

- `RANDOMIZER` genere `/articles-aleatoires.json`.
- `RHIZOME` genere `/rhizome-curieux/index.json`.
- `ALMANACH` genere `/almanach/index.json`.

Sorties globales :

- home : `HTML`, `RSS`, `RANDOMIZER`
- sections : `HTML`, `RSS`
- pages : `HTML`
- taxonomies et terms : `HTML`

`ALMANACH` est volontairement absent des sorties globales. Il est declare dans `content/almanach/_index.md`, avec :

```yaml
outputs: ["ALMANACH"]
build:
  render: always
  list: never
  publishResources: false
```

---

## 5. Shell Et Navigation

Le shell principal est dans `layouts/_default/baseof.html`.

Architecture :

- `body` en `h-screen w-screen overflow-hidden`.
- `#app-shell` comme conteneur relatif.
- `#sidebar-backdrop`, clic pour fermer la sidebar.
- `#sidebar-panel`, sidebar off-canvas de `280px`.
- bouton desktop de sidebar dans un `header` absolu, cache sur mobile.
- `main` prend toute la hauteur et contient une zone scrollable interne.
- si `.Params.full_width` est vrai, le template recoit toute la largeur et toute la hauteur.
- sinon, contenu standard dans un conteneur `max-w-5xl`.
- la navigation mobile est injectee en bas via `layouts/partials/mobile-nav.html`.

La sidebar (`layouts/partials/sidebar.html`) est un composant visuel :

- logo `Presque.`
- menu issu de `menus.main`
- couleurs cycliques Catppuccin sur les entrees
- liens footer vers `/manuel/`, `/tags/`
- bouton `Aléatoire`, qui appelle `randomArticle()` et consomme `/articles-aleatoires.json`

La nav mobile :

- barre fixe en bas ;
- bouton accueil ;
- icones SVG par entree de menu ;
- fallback etoile si une entree n'a pas d'icone declaree.

---

## 6. Accueil Dashboard

`layouts/index.html` construit la page d'accueil comme un dashboard plein ecran.

Composition :

- `widgets/system-header.html`
- `widgets/dom-card.html`
- `widgets/identity-card.html`
- `widgets/latest-posts.html`
- `widgets/almanach-card.html`

`system-header.html` calcule des metriques de corpus :

- heures depuis une date d'origine ;
- nombre de mots uniques ;
- parentheses ;
- densite moyenne de mots par phrase ;
- asterisques ;
- liens Markdown ;
- sidenotes ;
- entrees d'almanach.

Il parcourt `hugo.Sites` et utilise `hugo.Data.almanach`. Cette forme est importante avec Hugo recent.

`dom-card.html` est un widget interactif avec :

- bouton central ;
- compteur ;
- journal systeme ;
- etats tombstone/admin/virus ;
- donnees narratives cote `static/data/dom-story.json` et logique dans `assets/js/dom-engine.js`.

`identity-card.html` affiche :

- avatar `static/media/avatar-explorer.jpg` ;
- fiche personnage ;
- experience calculee depuis `params.author.birthdate` ;
- liens YouTube, Instagram, Patafoin, Manuel ;
- chargement de `assets/js/daily-exp.js`.

`latest-posts.html` affiche les 8 derniers contenus de :

- `ondes-pixels`
- `recherches`
- `solutions-imaginaires`

Il les represente avec les images d'inventaire de `static/media/inventory/`.

`almanach-card.html` affiche :

- date pataphysique via `PataphysicalDate.js` ;
- fete du jour ;
- entree quotidienne chargee depuis `/almanach/index.json`.

---

## 7. Articles Et Pages Simples

Le template general d'article est `layouts/_default/single.html`.

Il fournit :

- fil d'Ariane ;
- titre ;
- tags ;
- bouton de plan si `.TableOfContents` existe ;
- panneau de table des matieres en overlay ;
- contenu en `article.content.max-w-[60ch].prose.prose-catppuccin`;
- footer article, sauf si `hide_footer` est vrai ;
- chargement de `assets/js/sidenote-adjuster.js`.

Le footer article (`layouts/partials/article-footer.html`) contient :

- date de publication ;
- nombre de caracteres ;
- hash Git si `enableGitInfo` donne une info ;
- bouton de partage par clipboard ;
- CTA vers Patafoin avec `?sujet={{ .Title | urlquery }}`;
- articles lies via `Site.RegularPages.Related`, fallback meme section ;
- navigation precedent/suivant dans la section.

Le shortcode `sidenote` :

- cree une note laterale numerotee ;
- alterne gauche/droite selon le rang ;
- est cliquable sur mobile ;
- est place en marge sur desktop ;
- depend de `sidenote-adjuster.js` pour eviter les collisions verticales.

Quand on ecrit des textes longs, les notes de bas de page Markdown classiques restent preferables pour les references documentaires longues. Le shortcode `sidenote` sert plutot aux marginalia lisibles dans la page.

---

## 8. Sections Publiques

### `/solutions-imaginaires/`

Fichiers :

- contenu : `content/solutions-imaginaires/`
- layout : `layouts/solutions-imaginaires/list.html`
- styles : bloc `SOLUTIONS IMAGINAIRES` dans `assets/css/main.css`
- assets : `static/media/solution-imaginaire/`

Role :

- section claire, exception volontaire au fond Catppuccin sombre ;
- atmosphere de jardin automnal ;
- titre image `solutions_imaginaires_titre.png` ;
- cartes-feuilles tirees de 7 images de feuilles ;
- colonne centrale organique ;
- pollen flottant ;
- 42 fourmis statiques dispersees ;
- chaque sous-page devient une feuille cliquable.

Contenu actuel important :

- `content/solutions-imaginaires/blog_corée/` contient le carnet de Coree, prologue et jours 1 a 14.
- Ce dossier etait non suivi Git au moment de l'audit.
- Comme `removePathAccents` est actif, l'URL publiee devient `/solutions-imaginaires/blog_coree/...`.
- Les pages de ce carnet n'ont pas toutes de `date`. Si l'ordre visuel devient important, ajouter `weight` ou `date` plutot que compter sur l'ordre de fichiers.

### `/ondes-pixels/`

Fichiers :

- contenu : `content/ondes-pixels/`
- layout : `layouts/ondes-pixels/list.html`
- carte : `layouts/partials/cards/wave-card.html`
- styles : bloc `ONDES & PIXELS` dans `assets/css/main.css`

Role :

- espace pour objets sonores, videos, textures numeriques ;
- grille asymetrique de wave cards ;
- cards differenciees `ondes` et `pixels` selon les tags ;
- embeds sectionnels YouTube et Spotify depuis le front matter de `content/ondes-pixels/_index.md`.

Series actuelles :

- `autour-du-pot`
- `mamies`
- `bestiaire_miyazaki_youtube`

Les contenus audio peuvent integrer directement des iframes, comme Acast dans `autour-du-pot`.

### `/recherches/`

Fichiers :

- contenu : `content/recherches/`
- liste : `layouts/recherches/list.html`
- single : `layouts/recherches/single.html`

Role :

- registre de travaux academiques ;
- liste pleine largeur avec style tableau technique ;
- single en deux colonnes : fiche signaletique, image, PDF, metadonnees, contenu.

Contenu actuel :

- `memoire-miyazaki`, avec `featured.png` et PDF compresse.

Le front matter utile inclut :

- `full_width: true`
- `date`
- `description`
- `tags`
- `authors`
- `icon`
- `color`

### `/rhizome-curieux/`

Fichiers :

- contenu : `content/rhizome-curieux/`
- layout HTML : `layouts/rhizome-curieux/list.html`
- JSON : `layouts/rhizome-curieux/list.rhizome.json`
- extracteur : `layouts/partials/functions/get-rhizome-items.html`
- moteur : `assets/js/rhizome-engine.js`

Role :

- graphe D3 de curiosites ;
- noeuds internes issus des pages Markdown ;
- noeuds externes issus de `items` dans `content/rhizome-curieux/_index.md`;
- sortie JSON exposee a `index.json`.

Front matter critique de la section :

```yaml
full_width: true
layout: "list"
outputs:
  - HTML
  - RHIZOME
```

Le moteur D3 :

- charge `index.json` relativement a la section ;
- separe `internal` et `external` ;
- organise les internes en noyau ;
- place les externes en orbite ;
- permet de filtrer nucleus/orbit ;
- ouvre les externes dans un nouvel onglet.

### `/patafoin/`

Fichiers :

- contenu : `content/patafoin/_index.md`
- layout : `layouts/patafoin/list.html`
- moteur : `assets/js/patafoin.js`

Role :

- forum minimal, terminal, alimente par Supabase ;
- sujets et reponses recursives ;
- l'article footer peut pre-remplir un nouveau sujet via `/patafoin/?sujet=TITRE`.

Schema attendu cote Supabase, d'apres le JS :

- table `topics` : au minimum `id`, `title`, `created_at`.
- table `posts` : `id`, `topic_id`, `parent_id`, `author_name`, `content`, `created_at`.
- le premier post d'un sujet a `parent_id: null`.
- les reponses pointent vers un `parent_id`.

Variables d'environnement vraiment lues par le template :

```sh
HUGO_SUPABASE_URL
HUGO_SUPABASE_KEY
```

Le commentaire dans `hugo.yaml` peut mentionner `HUGO_PARAMS_...`, mais le template actuel lit bien `HUGO_SUPABASE_URL` et `HUGO_SUPABASE_KEY` avec fallback sur `params.supabase_url` et `params.supabase_key`.

### `/manuel/`

Fichier :

- `content/manuel/_index.md`

Role :

- page simple avec `layout: "single"`.
- lien accessible depuis la sidebar et l'identity card.

### `/tags/` Et `/authors/`

- taxonomie `tags`, appelee visuellement `thesaurus`.
- taxonomie `authors`.
- `content/authors/_index.md` utilise `build` et `cascade` pour controler la sortie.

---

## 9. Endpoints JSON Et Donnees

### Randomizer

Fichier :

- `layouts/index.randomizer.json`

Sortie :

- `/articles-aleatoires.json`

Contenu :

- pages regulieres des sections `recherches`, `solutions-imaginaires`, `ondes-pixels`;
- chaque entree expose `title`, `permalink`, `section`.

Consommateur :

- `randomArticle()` dans `baseof.html`, appele par la sidebar.

### Almanach

Fichiers :

- donnees : `data/almanach.yaml`
- section fantome : `content/almanach/_index.md`
- template JSON : `layouts/almanach/list.almanach.json`
- widget JS : `assets/js/almanach.js`

Sortie :

- `/almanach/index.json`

Template :

- expose `meta.generated_at`;
- expose `database` depuis `hugo.Data.almanach`.

Ne pas remettre `ALMANACH` dans `outputs.section`, sinon Hugo regenerera des sorties inattendues pour toutes les sections.

### Rhizome

Fichiers :

- `layouts/rhizome-curieux/list.rhizome.json`
- `layouts/partials/functions/get-rhizome-items.html`

Sortie :

- `/rhizome-curieux/index.json`

Contenu :

- `nodes`
- `meta.count`
- `meta.generated`

### Pagefind

Pagefind est lance uniquement dans `netlify.toml` :

```sh
pnpm dlx pagefind --source 'public' --verbose
```

Il n'y a pas de script npm local dedie a Pagefind dans `package.json`.

---

## 10. Frontend Et CSS

Pipeline CSS :

- `layouts/partials/css.html` charge `assets/css/main.css`.
- Hugo utilise `css.TailwindCSS`.
- En dev : compilation Tailwind rapide.
- En prod : Tailwind puis `fingerprint`.
- Ne pas ajouter `| minify` apres `css.TailwindCSS` tant que Tailwind v4 et le CSS nesting natif provoquent des pertes de style.

`assets/css/main.css` contient :

- import Google Fonts unique avec `display=swap`;
- `@import "tailwindcss"`;
- `@plugin "@tailwindcss/typography"`;
- `@source` vers les layouts et le contenu ;
- variables Catppuccin Mocha ;
- theme Tailwind via `@theme`;
- `.prose-catppuccin`;
- `.bento-card`;
- styles de breadcrumb ;
- TOC overlay ;
- styles de `solutions-imaginaires` ;
- utilitaires globaux : `bg-grid-pattern`, `scrollbar-hide`, `image-pixelated`, etc. ;
- styles `ondes-pixels` et `wave-card`.

Regles visuelles importantes :

- Les accents des liens, boutons, tags et controles doivent etre visibles par defaut, pas seulement au hover.
- Les effets interactifs privilegient `transform` et `opacity`.
- Eviter `transition: all` sur des gros blocs.
- Eviter les grands `filter` et `backdrop-filter`; le site a deja remplace plusieurs flous par des fonds solides.
- Les ombres du systeme sont souvent des hard shadows, pas des ombres floues decoratives.
- Les cartes bento sont le langage principal du dashboard, mais les sections de lecture et les sections pleines largeur ont leur propre grammaire.

Fonts principales :

- sans : Ubuntu
- serif : Crimson Text
- mono : JetBrains Mono
- hand : Caveat
- display : Bebas Neue
- script : Bad Script

---

## 11. JavaScript Local

Loader standard :

- `layouts/partials/functions/js-loader.html`
- appel : `{{ partial "functions/js-loader.html" (slice "script1" "script2") }}`
- source attendue : `assets/js/script1.js`
- build : `js.Build`, minification en production, fingerprint.

Scripts :

- `PataphysicalDate.js` : librairie calendrier pataphysique.
- `almanach.js` : remplit le widget almanach et charge `/almanach/index.json`.
- `daily-exp.js` : anime la barre d'experience dans l'identity card.
- `dom-engine.js` : logique du widget DOM.
- `mobile-tooltip.js` : sur mobile, premier tap affiche le tooltip, second tap laisse naviguer.
- `patafoin.js` : client Supabase et rendu recursif forum.
- `rhizome-engine.js` : graphe D3 orbital.
- `sidenote-adjuster.js` : collision manager pour notes laterales.

Chargements externes :

- Rhizome charge D3 depuis `https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js`, avec SRI.
- Patafoin charge Supabase depuis `https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.105.1/dist/umd/supabase.min.js`, avec SRI.
- Le widget almanach utilise une texture externe `transparenttextures.com` dans son CSS inline.

Si une section doit marcher hors ligne ou avec une politique CSP plus stricte, ces dependances externes sont les premieres a regarder. Si on change la version d'un script CDN, recalculer l'attribut `integrity`.

---

## 12. Modele De Contenu

Convention generale :

- Preferer les leaf bundles : `content/section/slug/index.md`.
- Les ressources propres a une page restent dans son dossier.
- Les images servies globalement restent dans `static/media/`.

Front matter courant :

```yaml
---
title: "Titre"
date: 2026-04-28
description: "Phrase courte pour les cartes et le SEO"
tags:
  - tag
authors:
  - mathieu-allag
icon: "..."
color: "mauve"
full_width: true
---
```

Tous les champs ne sont pas necessaires partout :

- `full_width` est crucial pour les sections ou singles qui gerent leur propre largeur.
- `description` nourrit SEO, cards et parfois rhizome.
- `tags` nourrissent les related articles et les chips.
- `color` est utilise par rhizome, recherches et certaines cartes.
- `date` gouverne l'ordre dans beaucoup de listes. Sans date, Hugo tombe sur une date zero.

Pour les textes issus de notes :

- garder les formulations et images originales quand elles portent une sensation precise ;
- conserver les details concrets, meme s'ils semblent lateraux ;
- mettre les explications de references en notes de bas de page si elles interrompent la scene ;
- ne pas transformer une scene en resume psychologique ;
- quand une bizarrerie douce est presente, l'approfondir par ses consequences visibles.

---

## 13. Memo Commandes

### Etat Et Exploration

```sh
git status --short
git diff --stat
git diff -- path/to/file
rg --files
rg -n "motif" content layouts assets config
hugo version
pnpm --version
hugo list all
```

### Retrouver Les Raccourcis

```sh
git config --show-origin --get-regexp '^alias\.'
make -n dev
make -n build
pnpm run
rg -n "git save|pnpm dev|make dev|hugo" ~/.zsh_history
```

Observation actuelle :

- `git save` vient de `/Users/mathieu/.gitconfig`.
- ancien `alias hdev="pnpm dev"` trouve dans `~/.zshrc.pre-oh-my-zsh`.
- pas d'alias `hdev` actif trouve dans `~/.zshrc` lors de cet audit.

### Dev Local

```sh
make dev
pnpm dev
hugo server --disableFastRender
```

`make dev` et `pnpm dev` font la meme chose :

```sh
bash -c 'if [ -f .env.local ]; then set -a; source .env.local; set +a; fi; hugo server --disableFastRender'
```

Ils chargent donc `.env.local`, utile pour Patafoin/Supabase.

### Build

```sh
make build
pnpm run build
hugo --gc --minify --cleanDestinationDir
hugo --logLevel info --printPathWarnings
```

Differences :

- `make build` lance `hugo --gc --minify`.
- `pnpm run build` lance seulement `hugo --minify`.
- pour verifier une sortie propre, preferer `hugo --gc --minify --cleanDestinationDir`.
- pour chasser les avertissements de chemins/deprecations, utiliser `hugo --logLevel info --printPathWarnings`.

### Nettoyage

```sh
make clean
```

Cette cible supprime `public` et `resources`, puis lance `hugo mod clean`. A utiliser seulement quand on veut vraiment forcer Hugo/Tailwind a repartir de frais.

### Git

Alias existant :

```sh
git save "message"
```

Definition exacte :

```sh
git add -A && git commit -m "$1" && git push origin HEAD
```

Attention :

- `git save` stage tout, y compris les fichiers non suivis.
- avant `git save`, toujours lancer `git status --short`.
- au moment de cet audit, `content/solutions-imaginaires/blog_corée/` est non suivi et serait embarque.

Equivalent plus prudent :

```sh
git add fichier1 fichier2
git status --short
git commit -m "message"
git push origin HEAD
```

---

## 14. Build Et Deploiement Netlify

`netlify.toml` fait :

1. affiche versions Node, pnpm, Hugo ;
2. `pnpm install --verbose` ;
3. `hugo --gc --minify --logLevel debug --printI18nWarnings --printPathWarnings` ;
4. `pnpm dlx pagefind --source 'public' --verbose`.

Production :

- `HUGO_ENV = "production"`
- `HUGO_BASEURL = "https://www.presque-quelque-chose.com/"`
- `URL = "https://www.presque-quelque-chose.com/"`

Deploy previews :

- utilisent `-b $DEPLOY_PRIME_URL`;
- deploy preview ajoute `--buildFuture`.

Headers :

- headers de securite globaux dans `netlify.toml` : `X-Frame-Options`, `nosniff`, HSTS, `Referrer-Policy`, `Permissions-Policy` et CSP ;
- CSS/JS/fonts : cache long immutable.
- `/media/*` : cache 30 jours.

CSP :

- la CSP est appliquee par `netlify.toml`, pas par un `_headers` genere ;
- scripts autorises actuellement : site local, inline, `cdn.jsdelivr.net`, `www.googletagmanager.com`, `api.podcache.net` ;
- styles/fonts : `fonts.googleapis.com`, `fonts.gstatic.com`, inline ;
- frames : YouTube, YouTube nocookie, Spotify, Acast, Podcache/RedCircle ;
- images/connect/media restent volontairement larges (`https:`) pour eviter de casser les contenus et embeds existants ;
- si un nouvel embed, script, iframe, API ou asset externe ne fonctionne pas en prod, verifier la CSP dans `netlify.toml` avant de chercher une panne JS. Ajouter le domaine explicitement si le nouvel usage est voulu.

Redirects :

- `/categories/*` vers `/tags/:splat`
- `/categories` vers `/tags/`

Point a surveiller :

- Netlify et le poste local sont alignes sur Hugo `0.160.1`. Si l'un des deux bouge, refaire un build propre et verifier les warnings Hugo.

---

## 15. Mines Connues

Hugo recent :

- ne pas remettre `_build`, utiliser `build`.
- ne pas remettre `cascade._target`, utiliser `cascade.target`.
- ne pas remettre `includeFiles`, utiliser `files`.
- ne pas remettre `languageCode`, utiliser `locale`.
- preferer `hugo.Data` quand on vise les donnees globales.
- pour parcourir tout le corpus dans des templates globaux, utiliser `hugo.Sites` plutot que `site.AllPages`.

Almanach :

- ne pas declarer `ALMANACH` dans `outputs.section`.
- verifier apres build propre que seul `/almanach/index.json` existe pour l'API.

Tailwind :

- ne pas ajouter `| minify` dans `layouts/partials/css.html` apres `css.TailwindCSS` sans verifier les couleurs et le CSS nesting.
- `hugo_stats.json` doit rester hors des mounts.

Vendor :

- `_vendor/` contient des correctifs locaux. Un `hugo mod vendor` ou une mise a jour Hugo Blox peut les ecraser.
- apres mise a jour du module, relancer les recherches de deprecations et comparer les fichiers vendories modifies.

Patafoin :

- si le forum affiche une erreur de connexion, verifier `.env.local`, les variables Netlify et les politiques Supabase.
- le template lit `HUGO_SUPABASE_URL` et `HUGO_SUPABASE_KEY`.

Solutions imaginaires :

- la section force un fond clair avec `body:has(.solutions-imaginaires-page)`.
- elle deborde volontairement du conteneur standard avec marges negatives.
- les pages sans date peuvent etre mal ordonnees si Hugo change l'ordre par defaut ou si de nouveaux contenus sont ajoutes.

Articles :

- le TOC contient parfois des placeholders de shortcodes ; `single.html` nettoie `HAHAHUGOSHORTCODE...HBHB`.
- les sidenotes dependent du positionnement de l'`article`. Si la structure du single change, verifier les marges desktop.

---

## 16. Protocole De Travail Recommande

Avant d'editer :

```sh
git status --short
rg -n "terme pertinent" layouts assets content config
```

Pour une modification de contenu :

- lire le texte source entierement si la demande est stylistique ;
- ne pas lisser les details concrets ;
- verifier les front matters ;
- si l'ordre importe, ajouter `date` ou `weight`.

Pour une modification de layout/CSS :

- lire le layout et le bloc CSS correspondant ;
- verifier desktop et mobile ;
- eviter les effets couteux ;
- conserver les accents visibles par defaut ;
- lancer au moins `hugo --logLevel info --printPathWarnings`.

Pour une modification Hugo/config :

```sh
hugo --gc --minify --cleanDestinationDir
hugo --logLevel info --printPathWarnings
```

Pour une modification Patafoin :

- verifier les variables d'environnement ;
- verifier la structure `topics/posts` ;
- tester le chemin article footer vers `/patafoin/?sujet=...`.

Pour une modification d'API statique :

- verifier le fichier genere sous `public/` apres build ;
- verifier que la sortie HTML indesirable n'apparait pas ;
- verifier les consommateurs JS.

---

## 17. Dernieres Verifications Rapportees

D'apres la reprise technique precedente collee dans la conversation :

```sh
hugo --gc --minify --cleanDestinationDir
pnpm run build
hugo --logLevel info --printPathWarnings
```

Resultat rapporte :

- build Hugo OK ;
- build pnpm OK ;
- pas d'avertissement de deprecation ;
- `public/almanach/index.html` supprime apres nettoyage ;
- `public/almanach/index.json` conserve, comme attendu.

Ces resultats datent de la reprise du 2026-04-28. Si le site bouge, refaire les commandes plutot que se fier a ce souvenir.

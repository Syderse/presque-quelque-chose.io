# Phase 1 — Socle & coquille (P01 → P06)

Lis d'abord `00_PLAN.md` (esprit, décisions verrouillées, règles d'or, tokens). Chaque prompt ci-dessous est à coller tel quel dans Claude Opus 4.8, dans l'ordre.

---

## P01 — Branche + baseline mesurée + garde-fous

**But.** Créer la branche de refonte et figer une baseline chiffrée pour comparer à la fin.
**Fichiers.** Aucun fichier source modifié ; on note des mesures.

**Prompt à coller :**

> Nous démarrons une refonte UI radicale du site (voir `docs/refonte-typeheavy/00_PLAN.md`). Avant tout :
> 1. Lance `git status --short` et confirme un worktree propre. Crée et bascule sur la branche `refonte-typeheavy`.
> 2. Mesure et **affiche** la baseline, puis recopie-la dans un nouveau fichier `docs/refonte-typeheavy/BASELINE.md` (date du jour en titre) :
>    - `du -sh .git static _vendor public 2>/dev/null`
>    - build propre : `pnpm exec hugo --gc --minify --cleanDestinationDir` puis `ls -la public/css/` (poids CSS) et `find public -name '*.js' -exec du -ch {} + | tail -1` (poids JS total)
>    - présence des endpoints : `ls public/almanach/index.json public/articles-aleatoires.json public/rhizome-curieux/index.json` et vérifie qu'il n'y a PAS de `public/almanach/index.html`
>    - nombre de pages générées (fin du log Hugo)
> 3. Ne modifie aucun fichier source. Ne touche pas à `content/`. Commit : `refonte: branche + baseline`.
> Rappel des règles d'or : contenu sacré, fontes système seulement, haut contraste sans gris, on garde les endpoints/URLs/CSP, on mesure, on vérifie le build, Hugo épinglé via `pnpm exec hugo`.

**Vérif.** Branche `refonte-typeheavy` active, `BASELINE.md` créé, build vert.

---

## P02 — `site.css` : tokens + reset + base typographique (LE CŒUR)

**But.** Écrire le fichier CSS unique, à la main, qui porte toute l'identité type-heavy. C'est le prompt le plus important.
**Fichiers.** Créer `assets/css/site.css`. Ne touche pas encore à `main.css` ni au pipeline.

**Prompt à coller :**

> Crée `assets/css/site.css` : un **unique** fichier CSS écrit à la main, lisible, commenté, sans aucune dépendance (pas de Tailwind, pas de `@import` distant, **aucune fonte distante**). Objectif : socle type-heavy clair, haut contraste, fontes système, même rendu partout. Structure le fichier en sections commentées : `TOKENS`, `RESET`, `BASE`, `LAYOUT`, `TYPOGRAPHIE`, `COMPOSANTS` (vide pour l'instant), `UTILITAIRES`.
>
> 1. **TOKENS** — reprends exactement les custom properties de `docs/refonte-typeheavy/00_PLAN.md` §4 (palette claire, `--serif`, `--mono`, `--measure`, `--base`, `--lh`).
> 2. **RESET** — reset moderne minimal : `*,*::before,*::after{box-sizing:border-box} margin:0` raisonnés, `img,svg,video{max-width:100%;height:auto;display:block}`, `html{-webkit-text-size-adjust:100%}`, focus visible net (`:focus-visible{outline:2px solid var(--accent);outline-offset:2px}`).
> 3. **BASE** — `html` scroll fluide ; `body{background:var(--bg);color:var(--fg);font-family:var(--serif);font-size:var(--base);line-height:var(--lh)}` ; en **flux normal**, document qui défile (PAS de `height:100vh` ni `overflow:hidden`). Sélection (`::selection`) contrastée.
> 4. **TYPOGRAPHIE** — titres `h1..h6` en serif, gras, interlignage serré, échelle modulaire (h1 ≈ clamp(2rem,…,2.8rem) → h6 ≈ 1rem). `p,ul,ol,blockquote` avec rythme vertical cohérent. Liens : **soulignés**, `a{color:var(--link)}`, `a:visited{color:var(--link-visited)}`, hover renforcé (épaissir le soulignement, pas de changement vers du pâle). `blockquote` avec filet à gauche couleur `--rule`. `code,pre` en `--mono` sur `--code-bg`. `hr` = filet `--rule`. `mark` = `--mark`. Tables lisibles, filets `--rule`.
> 5. **LAYOUT** — une classe `.measure{max-width:var(--measure);margin-inline:auto;padding-inline:1rem}` pour la colonne de lecture, et `.wide{max-width:72rem;margin-inline:auto;padding-inline:1rem}` pour les pages larges. Rien de plus.
> 6. **Règle anti-gris** : nulle part une couleur de texte grise/délavée. Un texte secondaire se distingue par la taille, la graisse, les petites capitales (`font-variant:small-caps` ou `text-transform:uppercase;letter-spacing` en mono), ou un filet — jamais par un gris.
>
> Garde le fichier court et net. Ne le branche pas encore (prochain prompt). Ne touche pas à `content/`. Commit : `refonte: site.css (socle typographique)`.

**Vérif.** `assets/css/site.css` existe, cohérent, sans `@import` ni domaine distant (`grep -n "@import\|googleapis\|http" assets/css/site.css` ne renvoie rien de distant).

---

## P03 — Brancher `site.css` (à côté de Tailwind, le temps de migrer)

**But.** Servir `site.css` via Hugo Pipes (minify + fingerprint), en parallèle de l'ancien CSS, pour migrer gabarit par gabarit sans casser le site.
**Fichiers.** `layouts/partials/css.html` (ou `baseof.html`).

**Prompt à coller :**

> Modifie `layouts/partials/css.html` pour émettre AUSSI `assets/css/site.css`, en plus du CSS actuel, pendant la migration. Pipeline pour `site.css` : `resources.Get "css/site.css" | minify | fingerprint`, avec `integrity` en prod. Place le `<link>` de `site.css` **après** celui de Tailwind pour qu'il prime. Ne retire rien d'autre pour l'instant (Tailwind reste, on le démontera au P22, une fois tous les gabarits migrés). Vérifie le build avec `pnpm exec hugo --gc --minify`. Ne touche pas à `content/`. Commit : `refonte: branche site.css en parallèle`.

**Vérif.** Build vert, `site.css` chargé (visible dans `public/`), site inchangé visuellement (normal : aucun gabarit ne l'utilise encore).

---

## P04 — `baseof.html` : coquille sémantique en flux normal

**But.** Remplacer la coquille « dashboard plein écran + sidebar overlay » par un document classique qui défile : `header` / `main` / `footer`.
**Fichiers.** `layouts/_default/baseof.html`.

**Prompt à coller :**

> Réécris `layouts/_default/baseof.html` en coquille minimale et sémantique, en flux normal (le site doit défiler comme un document, fini le verrouillage plein écran).
> - `<html lang>` ; `<head>` garde `{{ partial "seo.html" . }}` et `{{ partial "css.html" . }}`. **Supprime** les `preconnect` vers Google Fonts.
> - `<body>` : retire `h-screen w-screen overflow-hidden` et toutes les classes Tailwind ; le body est en flux normal. Structure : `{{ partial "header.html" . }}` (créé au P05), puis `<main class="measure">` (ou `wide` si `.Params.full_width`) contenant `{{ block "main" . }}{{ end }}`, puis `{{ partial "footer.html" . }}` (créé au P06).
> - **Supprime** la sidebar overlay, le backdrop, le bouton toggle, et l'inclusion de `mobile-nav.html`. Conserve le petit script `randomArticle()` (utilisé par le lien aléatoire) — garde-le inline, c'est minuscule. Conserve `{{ block "scripts" . }}{{ end }}`.
> - Retire l'inclusion globale de `mobile-tooltip` (on n'a plus de tooltips). Garde le fichier sobre.
> Comme `header.html`/`footer.html` n'existent pas encore, crée-les en stubs minimaux (un `<header class="wide">` avec un lien vers `/`, un `<footer class="wide">` avec le copyright) pour que le build passe ; ils seront étoffés aux P05/P06. Vérifie le build. Ne touche pas à `content/`. Commit : `refonte: coquille baseof en flux normal`.

**Vérif.** Le site défile normalement, plus de sidebar overlay, build vert. (Le style sera encore imparfait tant que P05/P06/P08 ne sont pas passés — normal.)

---

## P05 — En-tête + navigation texte

**But.** Une navigation typographique sobre qui remplace la sidebar overlay et la mobile-nav.
**Fichiers.** Créer `layouts/partials/header.html`. Le menu vient déjà de `config/_default/hugo.yaml` (`menus.main`).

**Prompt à coller :**

> Crée `layouts/partials/header.html` : un en-tête typographique minimal, en haut du document, dans `<header class="wide">`.
> - Le titre du site `presque-quelque-chose` en lien vers `/` (lien de retour à l'accueil).
> - Une `<nav>` avec les entrées de `.Site.Menus.main` (solutions imaginaires, recherches, ondes & pixels, antenne radio, rhizome curieux, patafoin), plus des liens vers `/tags/` (thésaurus), `/manuel/`, `/recherche/` (page recherche Pagefind, créée au P24) et un lien « au hasard » qui appelle `randomArticle()`.
> - Liens texte simples, soulignés, séparés proprement (espaces/filets), repli en colonne sur petit écran via CSS simple. Marque la section courante avec `{{ if $.IsMenuCurrent "main" . }}` (gras ou petite puce, **pas** une couleur pâle).
> - Aucune classe Tailwind, aucune icône SVG décorative, aucune fonte distante. Ajoute les styles nécessaires dans la section `COMPOSANTS` de `assets/css/site.css` (ex. `.site-header`, `.site-nav`), en respectant la règle anti-gris.
> Vérifie le build. Ne touche pas à `content/`. Commit : `refonte: header + navigation texte`.

**Vérif.** Nav lisible, tous les liens de section présents, section active marquée sans gris, responsive correct.

---

## P06 — Pied de page minimal

**But.** Un pied sobre : copyright + licence, éventuellement une ligne d'identité.
**Fichiers.** Créer `layouts/partials/footer.html`. (S'inspirer du bloc `footer.copyright` de `hugo.yaml`.)

**Prompt à coller :**

> Crée `layouts/partials/footer.html` dans `<footer class="wide">` : minimal.
> - Ligne de copyright + licence à partir de `site.Params.footer.copyright` (notice avec l'année, licence si activée). Garde la mention de licence Creative Commons existante.
> - Liens utiles : accueil, manuel, thésaurus. Tout en texte.
> - Styles dans `COMPOSANTS` de `site.css` (`.site-footer`), filet de séparation en `--rule`, pas de gris.
> Vérifie le build. Ne touche pas à `content/`. Commit : `refonte: footer minimal`.

**Vérif.** Pied lisible, licence présente, build vert.

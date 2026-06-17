# Phase 5 — Démontage, sécurité, vérif, doc (P22 → P26)

On ne lance cette phase qu'une fois **tous les gabarits migrés** (P04→P21). C'est ici qu'on retire Tailwind/Blox et qu'on encaisse les gains. Lis `00_PLAN.md` d'abord.

---

## P22 — Retrait de Tailwind + Hugo Blox + ancien `main.css`

**But.** Atteindre l'état cible : un seul CSS écrit à la main, plus de build Tailwind, plus de Hugo Blox.
**Fichiers.** `assets/css/main.css` (suppression), `layouts/partials/css.html`, `config/_default/hugo.yaml` (module imports/mounts), `layouts/partials/debug/safelist.html`, `_vendor/`, `package.json`/`pnpm-*`.

**Prompt à coller :**

> Lis `CLAUDE.md` d'abord. Lis `00_PLAN.md` d'abord.
> Pré-requis : tous les gabarits doivent déjà utiliser `site.css` (P04→P21). Vérifie d'abord qu'il ne reste **aucune** classe Tailwind/Catppuccin utilisée : `rg -n "ctp-|md:|class=\"[^\"]*\\b(flex|grid|text-|bg-|p-[0-9])" layouts | head` — s'il reste des usages, **arrête-toi et liste-les**, ne casse rien.
> Ensuite, démonte proprement :
> - `layouts/partials/css.html` : ne sert plus QUE `site.css` (`resources.Get "css/site.css" | minify | fingerprint`). Retire toute la branche `css.TailwindCSS`.
> - `config/_default/hugo.yaml` : retire les `module.imports` `blox-tailwind` (et `blox-plugin-netlify` si plus utilisé), et les `module.mounts` liés à Hugo Blox (community/all-access/blox css). Retire `build.writeStats` (spécifique Tailwind JIT) si plus rien ne l'utilise.
> - Supprime `assets/css/main.css` (l'ancien) et `layouts/partials/debug/safelist.html`.
> - `package.json` : retire les dépendances devenues inutiles (Tailwind v4, typography plugin, PostCSS éventuel). Mets à jour le lockfile (`pnpm install`).
> - `_vendor/` : audit prudent (`pnpm exec hugo mod graph` / build `--ignoreVendorPaths "**"`) — ne supprime `_vendor/` que si le build passe sans lui. Sinon documente ce qui reste nécessaire.
> Build complet `pnpm exec hugo --gc --minify --cleanDestinationDir --printPathWarnings`. **Tout doit passer.** Si quelque chose casse, reviens en arrière plutôt que de bricoler. Ne touche pas à `content/`. Commit : `refonte: retrait Tailwind + Hugo Blox`.

**Vérif.** Build vert, un seul CSS servi, plus de référence Tailwind/Blox, aucune classe utilitaire orpheline.

---

## P23 — Nettoyage JS, fontes, images

**But.** Supprimer tout le JS/asset mort et toute trace de fonte distante.
**Fichiers.** `assets/js/*`, `layouts/partials/widgets/*`, `layouts/partials/mobile-nav.html`, `layouts/partials/sidebar.html`, `assets/css/themes/custom.css`, images de `static/media/`.

**Prompt à coller :**

> Lis `CLAUDE.md` d'abord. et `00_PLAN.md`.
> Nettoie tout le code désormais inutilisé, en vérifiant à chaque fois qu'il n'est plus référencé (`rg` avant de supprimer).
> - **JS** : supprime les moteurs remplacés — `dom-engine.js` (→ `dom.js`), `antenne-radio.js`, `daily-exp.js`, `mobile-tooltip.js`, `sidenote-adjuster.js`, et `almanach.js` si la version texte du P16 l'a rendu inutile. Garde `dom.js`, `PataphysicalDate.js`, `patafoin.js`, et `rhizome-engine.js` (chargé à la demande). Vérifie `layouts/partials/functions/js-loader.html`.
> - **Widgets/partials morts** : supprime `widgets/dom-card.html`, `widgets/identity-card.html`, `widgets/almanach-card.html`, `widgets/manifesto-card.html`, `widgets/system-header.html`, `widgets/latest-posts.html`, `partials/sidebar.html`, `partials/mobile-nav.html`, et les cartes décorées inutilisées (`cards/wave-card.html`, `cards/archive-card.html`, `cards/rhizome-card.html`) — **seulement** si plus aucun gabarit ne les inclut.
> - **Fontes distantes** : confirme qu'il ne reste **aucune** trace — `rg -n "googleapis|gstatic|fonts.google|@import url" assets layouts` doit être vide. Supprime `assets/css/themes/custom.css` s'il est vide/inutile.
> - **Images** : supprime les images décoratives inutilisées ; pour `static/media/logo.png` (~1,3 Mo) et l'avatar, soit optimise (recompresse sans changer le rendu utile), soit retire si plus référencé. Mesure `du -sh static`.
> Build complet, puis `rg` de contrôle. Ne touche pas à `content/` ni à `data/` ni à `static/data/`. Commit : `refonte: nettoyage JS/fontes/images`.

**Vérif.** `rg "googleapis|gstatic"` vide ; aucun JS mort chargé ; `static/` allégé ; build vert.

---

## P24 — Netlify / CSP / Pagefind / (GA optionnel)

**But.** Mettre la CSP et l'infra en cohérence avec le nouveau site (plus de domaines de fontes, dépendances self-hosted), et installer la page recherche.
**Fichiers.** `netlify.toml`, `layouts/partials/seo.html` (si refs fontes), une page `/recherche` (Pagefind).

**Prompt à coller :**

> Lis `CLAUDE.md` d'abord. et `00_PLAN.md`.
> Mets l'infra en cohérence avec la refonte :
> 1. **CSP** dans `netlify.toml` : retire `https://fonts.googleapis.com` (style-src/style-src-elem) et `https://fonts.gstatic.com` (font-src) — on n'utilise plus de fontes distantes ; `font-src 'self' data:` suffit, `style-src 'self' 'unsafe-inline'`. Retire `https://cdn.jsdelivr.net` si D3/Supabase sont désormais self-hosted (P17/P20) ; sinon garde-le. **Conserve** `frame-src` pour les embeds (YouTube, Spotify, Acast, podcache, redcircle) et `connect-src` pour Supabase. Vérifie qu'aucune ressource réelle n'est bloquée.
> 2. **Preconnect** : confirme que les `preconnect` Google Fonts ont bien disparu (`baseof.html`, `seo.html`).
> 3. **Pagefind / recherche** : crée une page `/recherche` qui charge l'UI Pagefind (assets locaux générés dans `/pagefind/` au build Netlify) **uniquement sur cette page**. Garde l'indexation Pagefind dans la commande de build. Lien « recherche » déjà dans le header (P05).
> 4. **Google Analytics (je valide en vrai je suis chaud)** : si tu veux un site vraiment sans traceur, retire `services.googleAnalytics` de `hugo.yaml` et `https://www.googletagmanager.com` de la CSP. **Demande-moi avant** — c'est un choix éditorial, pas un défaut.
> Vérifie le build et, si possible, un déploiement preview. Commit : `refonte: CSP + recherche Pagefind`.

**Vérif.** CSP sans domaines de fontes, embeds et forum fonctionnels, page `/recherche` opérationnelle.

---

## P25 — Build, mesures, comparaison baseline, contraste & multi-navigateur

**But.** Encaisser et chiffrer les gains ; contrôler l'accessibilité et le rendu.
**Fichiers.** `docs/refonte-typeheavy/BASELINE.md` (ajout des mesures « après »).

**Prompt à coller :**

> Lis `CLAUDE.md` d'abord. et `00_PLAN.md`.
> Build final et bilan chiffré :
> 1. `pnpm exec hugo --gc --minify --cleanDestinationDir --printPathWarnings` — zéro erreur.
> 2. Re-mesure exactement comme la baseline (voir `00_PLAN.md` §6) et ajoute une section « APRÈS » à `docs/refonte-typeheavy/BASELINE.md` : `du -sh static _vendor public`, poids CSS généré, poids JS total, présence des endpoints (`almanach/index.json`, `articles-aleatoires.json`, `rhizome-curieux/index.json`), absence de `almanach/index.html`, nombre de pages.
> 3. **Contrôle contraste** : vérifie que le texte courant atteint un ratio AAA sur `--bg` et qu'il n'existe **aucun** texte gris délavé (`rg -n "color:\\s*#?(8|9|a|b|c)" assets/css/site.css` pour repérer des couleurs claires suspectes ; justifie chaque cas).
> 4. **Multi-navigateur / responsive** : vérifie le rendu (idéalement via l'outil de preview) sur une page d'accueil, un article avec sidenotes, une liste, le rhizome, l'antenne radio, le forum — en large ET en étroit. Note tout écart.
> 5. **Réseau** : confirme zéro requête vers `fonts.googleapis.com`/`gstatic.com` (onglet réseau ou `rg`).
> Affiche un tableau avant/après (CSS, JS, static, requêtes de fontes). Commit : `refonte: bilan mesures + contrôles`.

**Vérif.** CSS et JS nettement plus légers qu'en baseline, zéro fonte distante, endpoints présents, rendu correct partout.

---

## P26 — Mise à jour de la doc projet

**But.** Refléter la nouvelle stack dans la doc de reprise.
**Fichiers.** `docs/AGENTS.md`, `docs/HISTORIQUE.md`, `docs/CHANTIERS.md`.

**Prompt à coller :**

> Lis `CLAUDE.md` d'abord. et `00_PLAN.md`.
> Mets à jour la doc projet pour refléter la refonte :
> - `docs/AGENTS.md` : nouvelle stack (Hugo + **un seul CSS écrit à la main** `assets/css/site.css`, **sans Tailwind ni Hugo Blox**, **fontes système**, JS minimal). Mets à jour la « Carte Rapide » (header/footer partials, site.css, dom.js…), retire les mentions Tailwind/JIT/`hugo_stats.json`/safelist, et la liste des moteurs JS supprimés. Garde les sections endpoints JSON, sidenotes, sections.
> - `docs/HISTORIQUE.md` : une entrée datée « Refonte type-heavy » — décision (manifeste bestmotherfucking : clair, serif système, haut contraste, sans fontes distantes, CSS main, sans Tailwind/Blox), conséquences (gadgets reconvertis : DOM préservé, almanach/rhizome/antenne en texte, forum isolé), endpoints/URLs préservés. Très concis.
> - `docs/CHANTIERS.md` : clôture les tâches rendues caduques (migration paquet almanach, libellés identity-card, audit embeds, self-host D3/Supabase) et ajoute les éventuels restes (ex. choix GA).
> - Mets à jour le `README.md` si tu veux qu'il décrive le vrai site plutôt que le thème d'origine (optionnel).
> Commit : `doc: refonte type-heavy`.

**Vérif.** La doc décrit la stack réelle ; un repreneur comprend le nouveau socle sans lire tout le code.

---

## Après la série

Quand tout est vert et mesuré : ouvrir une PR `refonte-typeheavy` → `main`, relire le diff (en confirmant qu'aucun fichier de `content/` n'a été altéré, sauf la migration d'embeds explicitement validée au P19), puis fusionner. Le cabinet de curiosités est intact ; il pèse une plume et se lit comme un livre.

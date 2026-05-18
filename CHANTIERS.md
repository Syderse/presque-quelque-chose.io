# CHANTIERS.md - presque-quelque-chose.io

## Lecture Et Articles



## Accueil Et Widgets

- [ ] Dans `identity-card`, afficher au hover des petites icones de liens un libelle tres court indiquant la destination : YouTube, Instagram, forum, guide, site. Prevoir aussi un comportement accessible au clavier et coherent avec `mobile-tooltip.js`.
- [ ] j'aimerais changer le fonctionnement d'almanach. plutôt que d'écrire au préalable une mini-entrée de journal pour chaque jour de l'année de manière prévue et fixe, j'aimerais que le widget de l'accueil pioche dans une réserve d'entrées de journal. il faudrait définir un aléatoire qui évite la répétition pour que toutes sortent avant que la première ne ressorte, mais dans un ordre aléatoire.. par ailleurs, ce faisant, je me permettrai sans doute d'écrire des entrées à longueur encore plus variable, donc il faudrait trouver une solution pour que les lecteurs puissent agrandir le cadre et qu'il occupe presque un plein écran, une large fenêtre centrée, si les premières lignes les intéressent et qu'ils veulent lire ce qui suit les ...

## Pages Et Parcours

- [ ] Clarifier le statut du droit d'auteur des contenus publies. Decider ce qui vaut pour les textes, romans-feuilletons, scripts audio, images, PDF et contenus academiques ; puis mettre a jour footer, page dediee ou metadata si besoin.
- [ ] Verifier les pages de sections apres les suppressions d'assets : accueil, `/solutions-imaginaires/`, `/ondes-pixels/`, `/recherches/`, `/rhizome-curieux/`, `/patafoin/`.

## Performance Et Assets

- [ ] Optimiser `static/media/logo.png` sans changer son rendu utile, ou confirmer qu'il doit rester tel quel.
- [ ] Confirmer que les anciens assets decoratifs remplaces restent non references avant toute suppression finale : inventaire, feuilles, titre image, et tout asset de decor similaire.
- [ ] Auditer les embeds audio/video d'`ondes-pixels` : lazy loading, taille des iframes, domaines CSP, et experience mobile.
- [ ] Etudier une variante self-hosted ou mieux isolee pour les dependances externes critiques : D3, Supabase UMD, texture almanach.
- [ ] Continuer a limiter `transition-all`, `backdrop-blur`, `filter`, `drop-shadow`, `will-change` et animations permanentes dans les templates restants.

## Build Et Maintenance

- [ ] Auditer `_vendor/` sans suppression brutale avec `pnpm exec hugo mod graph --ignoreVendorPaths "**"` et un build `--ignoreVendorPaths "**"`. Identifier les correctifs locaux avant toute decision.
- [ ] Documenter plus explicitement la difference entre `pnpm exec hugo` et un Hugo global Homebrew si une doc utilisateur est ajoutee hors `AGENTS.md`.
- [ ] Garder une mesure de baseline apres gros chantier : `du -sh .git static _vendor public`, taille CSS generee, presence des endpoints JSON, absence de `public/almanach/index.html`.

# CHANTIERS.md - presque-quelque-chose.io

Backlog de maintenance. Ne pas tout faire en meme temps : prendre un chantier, mesurer, verifier, puis seulement passer au suivant.

---

## Lecture Et Articles

- [ ] Rendre le bouton `Plan` accessible pendant toute la lecture d'un article. Chercher une solution integree au shell de lecture, compatible desktop/mobile, et verifier explicitement qu'elle ne se superpose pas aux sidenotes.
- [ ] Ajouter la reciprocite des sidenotes : quand on clique sur le cadre d'une sidenote, mettre aussi en valeur le numero d'appel correspondant. Le chemin inverse existe deja ; garder le meme esprit visuel et prevoir les cas mobile/clavier.
- [ ] Verifier les longs articles avec beaucoup de sidenotes apres toute modification du layout `single.html`, surtout les pages du carnet de Coree.

## Accueil Et Widgets

- [ ] Dans `identity-card`, afficher au hover des petites icones de liens un libelle tres court indiquant la destination : YouTube, Instagram, forum, guide, site. Prevoir aussi un comportement accessible au clavier et coherent avec `mobile-tooltip.js`.
- [ ] Reparer et clarifier les stats du `system-header`. Priorite : afficher la derniere date/heure/minute de publication du site, puis la duree depuis la publication precedente pour donner une idee de l'activite recente.
- [ ] Auditer le cout build du calcul de vocabulaire dans `system-header.html` quand le corpus grossira. Le calcul est cote build, pas runtime, mais il peut devenir cher.

## Pages Et Parcours

- [ ] Concevoir une vraie page `404` locale, legere et dans le ton du site. Eviter la page par defaut ; proposer un retour accueil, quelques chemins utiles, et eventuellement un lien aleatoire sans charger d'asset lourd.
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

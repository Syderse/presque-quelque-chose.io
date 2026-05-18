# CHANTIERS.md - presque-quelque-chose.io

Backlog de maintenance. Ne pas tout faire en meme temps : prendre un chantier, mesurer, verifier, puis seulement passer au suivant.

---

## Lecture Et Articles

- [x] Rendre le bouton `Plan` accessible pendant toute la lecture d'un article. Chercher une solution integree au shell de lecture, compatible desktop/mobile, et verifier explicitement qu'elle ne se superpose pas aux sidenotes.
- [x] Ajouter la reciprocite des sidenotes : quand on clique sur le cadre d'une sidenote, mettre aussi en valeur le numero d'appel correspondant. Le chemin inverse existe deja ; garder le meme esprit visuel et prevoir les cas mobile/clavier.
- [x] La réciprocité fonctionne mais... j'aimerais que cliquer sur le cadre de la sidenote fonctionne comme quand je clique sur le numéro d'appel, c'est-à-dire : quand je clique une fois, ça le met en valeur et le colore (c'est déjà bon), et quand je reclique : ça le remet dans son état initial (ce n'est pas encore le cas pour les clics dans le cadre ; alors que ça l'est pour les clics sur le numéro d'appel). Comme tes moyens de vérification ont pris beaucoup de temps la dernière fois, tu peux me laisser vérifier moi même si ça fonctionne ^^je te ferai un retour précis. 

## Accueil Et Widgets

- [ ] Dans `identity-card`, afficher au hover des petites icones de liens un libelle tres court indiquant la destination : YouTube, Instagram, forum, guide, site. Prevoir aussi un comportement accessible au clavier et coherent avec `mobile-tooltip.js`.
- [x] Reparer et clarifier les stats du `system-header`. Priorite : afficher la derniere date/heure/minute de publication du site, puis la duree depuis la publication precedente pour donner une idee de l'activite recente.
- [x] Auditer le cout build du calcul de vocabulaire dans `system-header.html` quand le corpus grossira. Le calcul est cote build, pas runtime, mais il peut devenir cher.
- [x] on a bien géré le changement lightweight de layouts/partials/widgets/latest-posts.html mais il reste un souci. comme tu peux le voir sur la photo, ce n'est pas toujours très propre en fonction du zoom et de la taille de l'écran. les lignes se chevauchent, des mots semblent apparaître en filigrane, tout n'est pas bien centré dans les cadre parfois c'est trop proche du bord. j'aimerais que tu améliores drastiquement la propreté/netteté de ce petit cadre de l'accueil stp, en toutes circonstances de zoom stp
- [ ] j'aimerais changer le fonctionnement d'almanach. plutôt que d'écrire au préalable une mini-entrée de journal pour chaque jour de l'année de manière prévue et fixe, j'aimerais que le widget de l'accueil pioche dans une réserve d'entrées de journal. il faudrait définir un aléatoire qui évite la répétition pour que toutes sortent avant que la première ne ressorte, mais dans un ordre aléatoire.. par ailleurs, ce faisant, je me permettrai sans doute d'écrire des entrées à longueur encore plus variable, donc il faudrait trouver une solution pour que les lecteurs puissent agrandir le cadre et qu'il occupe presque un plein écran, une large fenêtre centrée, si les premières lignes les intéressent et qu'ils veulent lire ce qui suit les ...

## Pages Et Parcours

- [x] Concevoir une vraie page `404` locale, legere et dans le ton du site. Eviter la page par defaut ; proposer un retour accueil, quelques chemins utiles, et eventuellement un lien aleatoire sans charger d'asset lourd.
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

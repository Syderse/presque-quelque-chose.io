# CHANTIERS.md - presque-quelque-chose.io

## Antenne radio

### Liste de ressources à récolter

- Radiomorphoses
- Radio Fañch, le blog de Fañch Langoët
- Le Transistor, d’Hervé Marchais
- Les Radios Libres et La Radio du Futur — associés à Sébastien Poulain
- La Lettre Pro de la Radio & du Podcast et RadioActu
- Transom
- RadioDoc Review — revue spécialisée dans le documentaire audio, les podcasts narratifs et les formes factuelles travaillées
- Sounding Out! — grand blog de sound studies, pas seulement radio, mais avec de nombreuses entrées sur radio, podcasting, radio art, voix, écoute, médias sonores
- MeCCSA Radio and Audio Studies Network
- James Cridland / Radioland / Podnews
- WorldRadioHistory
- AIR, Third Coast, Nieman Storyboard / Audio Danger
- SchooP
- Syntone

## Autres

- [ ] Dans `identity-card`, afficher au hover des petites icones de liens un libelle tres court indiquant la destination : YouTube, Instagram, forum, guide, site. Prevoir aussi un comportement accessible au clavier et coherent avec `mobile-tooltip.js`.
- [ ] migration de paquet
  - [ ] Améliore la logique de migration du paquet almanach quand la réserve change. ne plus réinitialiser entièrement la queue locale dès que le fingerprint change. Si des entrées sont ajoutées, conserver autant que possible la progression locale du lecteur. 
Comportement souhaité :
1. Charger l’état local existant : queue, lastShownId, fingerprint, version.
2. Charger la nouvelle liste d’entrées depuis /almanach/index.json.
3. Comparer les ids connus localement avec les ids actuels.
4. Supprimer de queue les ids qui n’existent plus.
5. Identifier les nouveaux ids absents de l’ancien état.
6. Ajouter ces nouveaux ids à la queue existante, idéalement en les insérant à des positions aléatoires plutôt qu’en bloc au début ou à la fin.
7. Ne recréer un paquet complet que si l’état local est vraiment invalide/corrompu, ou si la queue devient vide.
8. Conserver la sécurité anti-répétition immédiate avec lastShownId.
9. Prévoir des tests de simulation :
   - ajout de nouvelles entrées en cours de cycle ;
   - suppression d’entrées en cours de cycle ;
   - ajout + suppression simultanés ;
   - état local corrompu ;
   - localStorage indisponible.
10. Documenter clairement la différence entre :
   - changement compatible de réserve, migré doucement ;
   - changement cassant, qui force une recréation complète.

- [ ] Clarifier le statut du droit d'auteur des contenus publies. Decider ce qui vaut pour les textes, romans-feuilletons, scripts audio, images, PDF et contenus academiques ; puis mettre a jour footer, page dediee ou metadata si besoin.

- [ ] Optimiser `static/media/logo.png` sans changer son rendu utile, ou confirmer qu'il doit rester tel quel.
- [ ] Auditer les embeds audio/video d'`ondes-pixels` : lazy loading, taille des iframes, domaines CSP, et experience mobile.
- [ ] Etudier une variante self-hosted ou mieux isolee pour les dependances externes critiques : D3, Supabase UMD, texture almanach.

- [ ] Auditer `_vendor/` sans suppression brutale avec `pnpm exec hugo mod graph --ignoreVendorPaths "**"` et un build `--ignoreVendorPaths "**"`. Identifier les correctifs locaux avant toute decision.
- [ ] Documenter plus explicitement la difference entre `pnpm exec hugo` et un Hugo global Homebrew si une doc utilisateur est ajoutee hors `AGENTS.md`.
- [ ] Garder une mesure de baseline apres gros chantier : `du -sh .git static _vendor public`, taille CSS generee, presence des endpoints JSON, absence de `public/almanach/index.html`.

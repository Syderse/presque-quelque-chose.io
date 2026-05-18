# HISTORIQUE.md - presque-quelque-chose.io

Journal minimal des changements structurels du site. Noter seulement ce qui aide a comprendre l'archeologie : date, decision, consequence. Rester tres tres tres concis.

---

## 2026-04-28 - Reprise Hugo recente

- Hugo local et Netlify alignes sur `hugo-extended` `0.160.1` via `pnpm exec hugo`.
- `HUGO_VERSION` et `HUGO_EXTENDED` retires de `netlify.toml` pour eviter l'installation Hugo interne Netlify/mise.
- Deprecations Hugo corrigees : `build`, `cascade.target`, `files`, `locale`, `hugo.Data`, parcours via `hugo.Sites`.
- Almanach isole : `ALMANACH` n'est plus une sortie globale de section ; endpoint attendu `public/almanach/index.json`, pas `index.html`.
- `_vendor/` garde des correctifs locaux Hugo Blox ; toute regen peut les ecraser.

## 2026-04-28 - Etat editorial et contenu

- Le site est documente comme systeme d'exploration, pas simple blog : textes longs, recherches, audio/video, rhizome, forum, almanach, dashboard.
- Le carnet `content/solutions-imaginaires/blog_corée/` etait signale comme point Git fragile ; etat a reverifier a chaque reprise.
- Convention forte : garder les details concrets des notes sources, ne pas lisser les textes longs.

## 2026-05-15 - Chantier lightweight

- Direction generale : conserver l'identite visuelle, reduire images decoratives, animations permanentes et effets couteux.
- `/solutions-imaginaires/` passe d'un decor image/pollen/fourmis a une composition CSS lightweight.
- `latest-posts` abandonne les assets d'inventaire et devient une liste dense avec pastilles CSS.
- Suppressions d'assets decoratifs visibles dans le worktree, notamment `static/media/inventory/`.
- `static/` devient beaucoup plus leger ; dernier gros fichier suivi note : `static/media/logo.png`.
- Bouton `Plan` rendu persistant : desktop aligne colonne de lecture, mobile integre a la nav basse.
- Sidenotes reciproques : clic/focus sur le cadre active aussi le numero d'appel, avec clavier et mobile.

## 2026-05-15 - AGENTS allege

- `AGENTS.md` passe d'une reprise longue a une fiche d'action courte pour Codex.
- L'archeologie sort de `AGENTS.md` et vit ici, dans `HISTORIQUE.md`.
- La liste de taches lightweight sort dans `CHANTIERS.md`; `AGENTS.md` garde seulement le lien.

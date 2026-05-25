# AGENTS.md - presque-quelque-chose.io

**Version :** 9.0, fiche lightweight
**Dernier audit :** 2026-05-15
**Stack observee :** Hugo Extended `0.160.1`, pnpm `10.14.0`, Tailwind CSS v4, Hugo Blox vendorie, D3, Supabase, Hugo Pipes/ESBuild.

Ce fichier est surtout une fiche de reprise pour Codex. Lire ceci, puis verifier l'etat reel avec `git status --short` et les fichiers sources. Ne jamais supposer que le worktree est propre.

Pour l'archeologie du site, utiliser [HISTORIQUE.md](HISTORIQUE.md) : y consigner au fil du temps des bilans tres tres tres concis, minimum, des changements structurels. `AGENTS.md` doit rester actionnable.

---

## Intention

`presque-quelque-chose.io` est un site personnel dense : textes longs, carnets, recherches, objets audio/video, rhizome de liens, forum maison, almanach et dashboard vivant. Ce n'est pas seulement un blog lineaire.

---

## Discipline Lightweight

Le site doit rester singulier et tactile, mais avec moins de cout permanent.

Par defaut :

- privilegier CSS stable, couleurs existantes, hard shadows, bordures nettes, variations typographiques ;
- ne charger une image que si elle porte un contenu reel ou une identite impossible a rendre proprement en CSS ;
- eviter les animations infinies decoratives, `transition-all`, `will-change` permanent, grands `filter`, `drop-shadow`, `backdrop-filter` et `backdrop-blur` ;
- limiter les transitions a `opacity`, `transform`, couleurs et bordures ;
- charger D3, Supabase et les moteurs JS seulement sur les pages utiles ;
- conserver URLs, front matters, endpoints JSON et workflows editoriaux ;
- mesurer avant/apres quand on touche a `static/`, `_vendor/`, `assets/css/main.css`, aux embeds ou au pipeline Hugo.

Critere de sortie : la page reste belle et identifiable, mais elle charge moins, anime moins, et se lit mieux sur mobile.

---

## Garde-Fous Git

- Toujours commencer par `git status --short`.
- Le worktree peut contenir des changements lightweight en cours ; ne rien revert automatiquement.
- L'alias `git save "message"` fait `git add -A && git commit -m "$1" && git push origin HEAD`. Il embarque donc suppressions, fichiers non suivis et changements voisins.
- Pour committer, preferer `git add fichier1 fichier2`, verifier le status, puis commit/push.

---

## Carte Rapide

- Config : `config/_default/hugo.yaml`
- Shell global : `layouts/_default/baseof.html`
- Articles : `layouts/_default/single.html`
- Accueil : `layouts/index.html` et `layouts/partials/widgets/`
- CSS : `layouts/partials/css.html`, `assets/css/main.css`
- JS loader : `layouts/partials/functions/js-loader.html`
- SEO : `layouts/partials/seo.html`
- Nav : `layouts/partials/sidebar.html`, `layouts/partials/mobile-nav.html`
- Footer article : `layouts/partials/article-footer.html`
- Sidenotes : `layouts/shortcodes/sidenote.html`, `assets/js/sidenote-adjuster.js`
- Almanach : `data/almanach.yaml`, `content/almanach/_index.md`, `layouts/almanach/list.almanach.json`, `assets/js/almanach.js`
- Rhizome : `layouts/rhizome-curieux/list.html`, `layouts/rhizome-curieux/list.rhizome.json`, `assets/js/rhizome-engine.js`
- Patafoin : `layouts/patafoin/list.html`, `assets/js/patafoin.js`
- Vendor Hugo Blox : `_vendor/` contient des correctifs locaux, prudence avant regen.

---

## Configuration A Ne Pas Casser

Hugo recent :

- utiliser `build`, pas `_build` ;
- utiliser `cascade.target`, pas `cascade._target` ;
- utiliser `files`, pas `includeFiles` ;
- utiliser `locale`, pas `languageCode` ;
- utiliser `hugo.Data` pour les donnees globales ;
- parcourir le corpus global avec `hugo.Sites`, pas `site.AllPages`.

Sorties JSON :

- `/articles-aleatoires.json` vient de `layouts/index.randomizer.json` ;
- `/rhizome-curieux/index.json` vient de `RHIZOME` ;
- `/almanach/index.json` vient de `ALMANACH` declare seulement dans `content/almanach/_index.md` ;
- ne pas remettre `ALMANACH` dans `outputs.section` ;
- apres build propre, `public/almanach/index.json` doit exister et `public/almanach/index.html` ne doit pas exister.

Tailwind/Hugo Pipes :

- `layouts/partials/css.html` utilise `css.TailwindCSS` ;
- ne pas ajouter `| minify` apres `css.TailwindCSS` sans verifier le CSS nesting et les couleurs ;
- `build.writeStats: true` est utile a Tailwind ;
- ne pas remonter `hugo_stats.json` dans les mounts.

Netlify :

- Netlify utilise le `hugo-extended` epingle par le projet via `pnpm exec hugo` ;
- `HUGO_VERSION` et `HUGO_EXTENDED` restent absents de `netlify.toml` ;
- la CSP vit dans `netlify.toml`. Si un embed/API casse en prod, verifier la CSP.

---

## Sections

`/antenne_radio/`

- Projet : antenne locale de veille en études radiophoniques.
- Périmètre v0.1 strict : RSS/Atom + HAL + Pydantic + scoring lexical + export Markdown Obsidian.
- Ne pas ajouter en v0.1 : Crossref, OpenAlex, CiNii, NDL, J-STAGE, Zotero automatique, Hugo, scraping, cron, auto-commit, LLM summaries.
- Toujours lancer `git status --short` au début et à la fin.
- Toujours lancer les tests pertinents après modification.
- Préférer des changements petits, testés, réversibles.
- Ne jamais masquer un test échoué.
- À la fin des blocs, mettre à jour antenne_radio/codex_memoire_materielle.md pour transmettre la mémoire des sessions.

### Philosophie & Doctrine de données — Antenne radio

L’antenne radio est un outil léger de veille académique, non une archive exhaustive.

**Principes cardinaux pour les agents :**
- **Impermanence & Rétention** : Conserver une fenêtre de veille récente de **18 mois** max. Ne pas accumuler indéfiniment les notices locales. Les caches bruts, bases intermédiaires, logs et exports privés sont jetables et ignorés par Git.
- **Archivage savant externe** : Zotero et Obsidian privé sont les uniques espaces d'archivage pérennes. La curation finale est manuelle et consciente.
- **Sobriété & Whitelist publique** : Garder les exports publics Hugo sobres, minimaux et strictement limités à la whitelist auditée. Ne jamais exporter de champ supplémentaire sans un audit explicite, justifié légalement et testé.
- **Intégrité de la curation humaine** : Le pipeline peut recalculer dynamiquement les scores machines et suggestions de toute la base si la configuration change, mais il ne doit **jamais** écraser silencieusement les décisions humaines de curation (`to_read`, `ignored`, `exported`, etc.).
- **Simplicité & Transmission** : Préférer des mécanismes ultra-simples, lisibles et transmissibles (ex. overrides via YAML externe) à toute forme d'architecture logicielle complexe ou d'automatisation cachée. Le projet a vocation à être partagé avec un laboratoire de recherche.

`/solutions-imaginaires/`

- Fond clair, jardin automnal, cartes-feuilles CSS.
- Etat lightweight : pas d'images de feuilles, pollen, fourmis ou titre image requis.
- Ne pas reintroduire d'assets decoratifs sans mesure et justification.
- `content/solutions-imaginaires/blog_corée/` est suivi par Git ; URL publique accentuee en `/blog_coree/`.
- Les pages du carnet n'ont pas toutes de `date`; si l'ordre importe, ajouter `weight` ou `date`.

`/ondes-pixels/`

- Objets audio/video, wave cards, embeds YouTube/Spotify/Acast.
- Auditer lazy loading, CSP et mobile avant d'ajouter des embeds.

`/recherches/`

- Travaux academiques ; liste tableau technique ; single en deux colonnes.
- `full_width`, `date`, `description`, `tags`, `authors`, `icon`, `color` peuvent compter selon les vues.

`/rhizome-curieux/`

- Graphe D3 charge depuis `index.json`.
- Front matter critique : `full_width: true`, `layout: "list"`, outputs `HTML` + `RHIZOME`.

`/patafoin/`

- Forum Supabase minimal.
- Variables lues : `HUGO_SUPABASE_URL`, `HUGO_SUPABASE_KEY`, avec fallback params.
- Tables attendues : `topics(id,title,created_at)` et `posts(id,topic_id,parent_id,author_name,content,created_at)`.

---

## Articles Et Sidenotes

- Le single article contient breadcrumb, titre, tags, bouton `Plan`, TOC overlay, contenu `article.content.max-w-[60ch].prose.prose-catppuccin`, footer, puis `sidenote-adjuster.js`.
- Le TOC nettoie parfois des placeholders `HAHAHUGOSHORTCODE...HBHB`.
- Les sidenotes dependent du positionnement de l'`article`; verifier les marges desktop apres changement de layout.
- Shortcode classique : `{{< sidenote >}}Texte.{{< /sidenote >}}`
- Variante commentaire : `{{< sidenote variant="comment" >}}Texte.{{< /sidenote >}}`
- Libelle global possible via `sidenote_comment_label`; ponctuellement `label`, `caption` ou `author`.

---

## Commandes

Etat et exploration :

```sh
git status --short
git diff --stat
git diff -- path/to/file
rg --files
rg -n "motif" content layouts assets config
pnpm exec hugo version
pnpm --version
```

Dev local :

```sh
make dev
pnpm dev
pnpm exec hugo server --disableFastRender
```

`make dev` et `pnpm dev` chargent `.env.local` puis utilisent le Hugo epingle du projet. Eviter `hugo server` brut.

Build/verifications :

```sh
make build
pnpm run build
pnpm exec hugo --gc --minify --cleanDestinationDir
pnpm exec hugo --logLevel info --printPathWarnings
```

Apres gros chantier, garder une baseline simple : `du -sh .git static _vendor public`, taille CSS generee, endpoints JSON, absence de `public/almanach/index.html`.

---

## Dernier Etat Utile

Chantier lightweight de mai 2026 :

- branche rapportee : `codex/lightweight-reform` ;
- `/solutions-imaginaires/` rendu en CSS lightweight ;
- `latest-posts` ne charge plus `/media/inventory/` ;
- plusieurs suppressions d'assets decoratifs sont visibles dans le worktree ;
- dernier build rapporte OK : `pnpm exec hugo --gc --minify --cleanDestinationDir --logLevel info --printPathWarnings` ;
- warning connu : deprecation Node/Tailwind `module.register()`.

Mesures locales notees le 2026-05-15 :

- `.git` : `177M`
- `static` : `1.4M`
- `_vendor` : `16M`
- `public` : `14M`
- CSS genere visible dans `public/css/` : environ `283632` octets
- seul fichier suivi de plus de 500K dans `static/media/` : `static/media/logo.png`

---

## Chantiers

La liste de taches vit dans [CHANTIERS.md](CHANTIERS.md). Prendre un chantier, mesurer, verifier, puis seulement passer au suivant.

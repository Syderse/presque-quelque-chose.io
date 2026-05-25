# Mémoire matérielle - Antenne Radio

> [!NOTE]
> Ce document est la mémoire technique consolidée du sous-projet `antenne_radio`. Il contient l'état actuel de l'architecture, les contrats de données critiques, la politique de sécurité anti-fuite et la synthèse historique des versions.

## 1. Reprise rapide & État du pipeline (Plan final gelé — 2026-05-25)

- **Démarrage rapide** : `git status --short`, puis lire `antenne_radio/README.md`. Commande hebdo : `make weekly` depuis `antenne_radio/`.
- **Architecture & Isolation** : Le sous-projet vit exclusivement dans `antenne_radio/` avec son `.venv` et ses dépendances. Pas de cron global, pas d'auto-commit, pas de LLM dans le pipeline.
- **Pipeline opérationnel** (6 steps) :
  - **Ingestion** : RSS/Atom (9 sources actives, `la_lettre_pro` désactivée) + HAL (limite 20) + Crossref (6 revues, `rows: 20`) + OpenAlex (19 profils, `per_page: 20`). Secrets via `.env.local` obligatoires.
  - **Normalisation & Déduplication** : Fusion dans `data/normalized/db.json` par ID stable (DOI > URL > Titre+Date).
  - **Rétention 18 mois** (`scripts/core/prune.py`) : élagage automatique des notices non-exported de plus de 18 mois.
  - **Scoring lexical** : Mots-clés positifs/négatifs + plancher académique (crossref/openalex/hal ≥ candidate). Seuils : `to_read ≥ 6`, `candidate ≥ 2`, `ignored < 2`.
  - **Exports privés** : Obsidian hebdomadaire, Zotero CSL JSON.
  - **Export public** : `static/antenne-radio/index.json` — whitelist stricte (10 clés éditorial / 13 clés bibliographique).
- **Intégration Hugo** : Page `/antenne-radio/` — cartes néo-brutalistes Catppuccin Mocha, filtres (type/source/langue/année/tri), deep-linking, bloc « À propos / contact / retrait », fallback noscript.
- **Routine** : `make weekly` → récolte + pruning + export + récapitulatif + scan anti-fuite + commandes git à copier-coller.

---

## 2. Contrats de données & Sécurité (Anti-fuite)

> [!IMPORTANT]
> **Confidentialité absolue (Anti-fuite)** : Interdiction stricte de publier abstracts (y compris `abstract_inverted_index`), raw dumps, logs de pipeline, scores internes, explications lexicales, mots-clés internes, auteurs, tags ou chemins locaux. Seules les métadonnées de la whitelist publique sont exportables.

### Whitelist publique autorisée (`index.json`)
La whitelist varie selon la famille de source (`BIBLIOGRAPHIC_SOURCE_FAMILIES = {crossref, openalex, hal}`) :

**Sources éditoriales (RSS/blogs)** — 10 clés :
`id`, `title`, `url`, `doi`, `published_at`, `source_name`, `source_type`, `language`, `source_family`, `attribution_id`.

**Sources bibliographiques (Crossref, OpenAlex, HAL)** — 13 clés (+ `authors`, `container_title`, `item_type`) :
idem + `authors` (liste noms, regex anti-email), `container_title` (titre revue), `item_type` (type biblio).

### Protocoles de courtoisie et secrets API
- **Identification (Polite API)** : Les connecteurs Crossref et OpenAlex requièrent des emails valides via les variables d'environnement locales `CROSSREF_MAILTO` et `OPENALEX_MAILTO` (chargées via `.env.local` non commité). Sans ces variables, aucun appel réseau n'est effectué (levée d'une erreur propre `missing_mailto`).
- **Redaction des secrets** : Les requêtes et payloads d'erreurs loggés doivent systématiquement masquer les clés privées et adresses email (`mailto=<redacted>`).

---

## 3. Synthèse de l'évolution historique

### v0.1 & v1 - Fondation et Base de Veille (18-19 mai 2026)
- **Objectif** : Initialisation du squelette Pydantic, connecteurs RSS/Atom et HAL, scoring lexical, export Obsidian, et premier audit juridique (`LEGAL_AUDIT.md`).
- **Changements clés** :
  - Création du pipeline d'exportation avec whitelist stricte et première section Hugo.
  - Implémentation du scoring lexical avec pénalisation des faux positifs techniques (`technical_radio_noise: -2`) et export Zotero CSL JSON.

### v2 - Interface Néo-brutaliste et UX (20 mai 2026)
- **Objectif** : Amélioration de l'ergonomie, de l'accessibilité et de la navigation Hugo.
- **Changements clés** :
  - **Navigation Hugo** : Ajout d'une entrée menu `antenne radio` avec icône SVG personnalisée, responsive mobile.
  - **Abonnements RSS** : Activation de 10 sources RSS conformes à l'audit juridique (Radiomorphoses, Radio Fañch, etc.).
  - **Template Néo-Brutaliste** : Passage d'un tableau à une grille de cartes (couleurs Catppuccin Mocha), transitions optimisées à 60fps (limitation à `transform` et `box-shadow`).
  - **Vanilla JS & Deep-linking** : Moteur de filtrage client dynamique isolée (7.6 Ko), logique de recherche textuelle combinée (ET), pagination progressive et synchronisation bidirectionnelle de l'URL (`history.replaceState` pour `q`, `cat`, `src`, `lang`).
  - **Accessibilité** : Badges interactifs de filtres actifs avec boutons équipés de `aria-label` et restauration du focus au clavier.

### v3 - Connecteurs Académiques & Intégration Robuste (20-21 mai 2026)
- **Objectif** : Intégration de Crossref et OpenAlex avec déduplication robuste et gestion fine des sources de confiance.
- **Changements clés** :
  - **Déduplication DOI inter-sources** : Algorithme puissant dans `merge_items_without_duplicates` qui fusionne les notices (HAL, Crossref, OpenAlex, RSS) sur la base du DOI normalisé, URL normalisée ou titre+date. Conserve l'ID canonique initial et le statut d'évaluation humaine (`to_read`, `candidate`, `ignored`).
  - **Intégration Crossref** : Activation en production pour les revues ciblées avec garde-fou polite (`rows: 20`, `polite_delay_seconds: 1`).
  - **Intégration OpenAlex** : Implémentation du connecteur mockable Works (`openalex.enabled: true`) avec requêtes ciblées et exclusions strictes de bruit (`NOT (radio frequency, beamforming, 5G, MIMO...)`).
  - **Boost de Scoring** : Ajout de `source_name: 1` dans `scoring.yaml` pour valoriser les revues de référence (ex. *Journal of Radio & Audio Media*).
  - **Attributions publiques** : Cartographie propre des sources académiques dans `export_public.py` (attributions `openalex`, `hal`, revues Crossref).

---

## 4. Statut des Sources & Périmètre de Veille (Fin de v3)

| Source / Revue | Canal d'accès | Statut | Rôle / Configuration |
| :--- | :--- | :--- | :--- |
| **RSS (10 sources)** | RSS / Atom | **Actif** | Sources de veille générales (Radio Survivor, Radiomorphoses, La Lettre Pro, etc.) |
| **HAL** | API HAL | **Actif** | Requête ciblée sur les dépôts académiques français (limite 20) |
| **Crossref - JRAM** | API Crossref | **Actif** | *Journal of Radio & Audio Media* (ISSN `1937-6529`), `rows: 20` |
| **Crossref - Radio Journal** | API Crossref | **Actif** | *Radio Journal: Int. Studies in Broadcast & Audio Media* (ISSN `1476-4504`) |
| **Crossref - Sound Studies** | API Crossref | **Actif** | *Sound Studies: An Interdisciplinary Journal* (ISSN `2055-1940`) |
| **Crossref - Resonance** | API Crossref | **Actif** | *Resonance: The Journal of Sound and Culture* (e-ISSN `2688-867X`) |
| **OpenAlex - JSS** | API OpenAlex | **Actif** | *Journal of Sonic Studies* (ISSN `2212-6252`) via profil dédié |
| **OpenAlex - Profils thématiques** | API OpenAlex | *Désactivé* | Profils généraux (`radio_studies`, `sound_studies`, etc.), en attente de réglages |
| **MeCCSA Radio & Audio** | RSS | **Actif** | Réseau suivi via son flux WordPress d'annonces |
| **IAMCR / ECREA** | Humain | *Veille manuelle* | Pas de flux structuré stable ; scraping HTML proscrit |

---

---

## 6. Bilan — Prompt 1 / Plan final (2026-05-25)

**Objectif :** exhaustivité des revues + scoring abouti + désactivation définitive de la_lettre_pro.

### Fichiers modifiés
- `config/sources.yaml` : désactivation définitive `la_lettre_pro` ; +2 revues Crossref (`organised_sound`, `sound_effects_journal`) ; +13 profils OpenAlex venue+mots-clés (7 anglophones + 6 francophones).
- `config/keywords.yaml` : enrichissement FR+EN de `radio_core` (+9 termes), `radio_free` (+6), `sound_studies` (+12), `podcast` (+5).
- `config/scoring.yaml` : ajout du bloc `academic_source_floor` (min_score=0, source_apis: crossref/openalex/hal).
- `scripts/core/scoring.py` : implémentation de `_apply_academic_floor` dans `score_item` — les articles académiques avec score brut ≥ 0 remontent à `candidate` au minimum.
- `scripts/export/export_public.py` : +16 entrées dans `AUDITED_ATTRIBUTIONS` + mappings `ATTRIBUTION_BY_SOURCE_NAME` avec variantes réelles observées post-run (noms sans ponctuation, entités HTML, casse).
- `tests/test_config.py` : +4 nouveaux tests (floor config, nouvelles revues Crossref, profils OpenAlex, la_lettre_pro).
- `tests/test_scoring.py` : +7 tests du plancher académique.
- `tests/test_export_public.py` : +3 tests d'attribution pour les nouvelles sources (19 cas paramétrés).
- `antenne_radio/01_RESSOURCES_SUIVIES.md` : mise à jour Crossref (6 revues), OpenAlex (20 profils), la_lettre_pro → désactivée définitivement.

### Compteurs réels (run du 2026-05-25)
- `make run` : 0 step échoué.
- `data/normalized/db.json` : **660 items** (vs 295 avant) — `to_read=292`, `candidate=266`, `ignored=102`.
- Source APIs : crossref=80, hal=45, openalex=276, rss=259.
- `make export-public` → **505 items publics** (vs 233 avant), 28 sources.
- Répartition publique : HAL 39, RSS Radio Survivor 52, La Lettre Pro (anciens) 30, Sounding Out! 30, Radio Fañch 23, Organised Sound 21, Media C&S 20, Sound Studies 20, Convergence 20, JSS 20, Réseaux 20, VIEW 20, Radio Journal 20, Questions de comm 20, Transposition 17, Sociétés & Repr. 13, Resonance 12, Volume! 11, JRAM T&F 35…
- **Doublons DOI : 0**.
- `make test` : **159/159 passés** (127 initiaux + 32 nouveaux).

### Scan anti-fuite
- 0 clé interdite dans l'index public.
- 0 e-mail, 0 chemin local.
- Whitelist stricte respectée (10 clés exactes par item).

### Plancher de confiance
- Articles Crossref/OpenAlex/HAL avec score ≥ 0 → minimum `candidate` (jamais `ignored`).
- Les poids négatifs techniques (-2) restent dominants si score < 0 : le bruit RF/médical intense reste `ignored`.
- Mention dans `score_explanation` : "plancher académique: statut élevé de ignored à candidate".

### Limites et points à surveiller
- Quelques sources OpenAlex bruyantes (SAGE Open, Social Sciences génériques) captées par les profils filtrés → bruit technique → `ignored`. Acceptable.
- `la_lettre_pro` : 30 anciens items restent en base (statut `to_read`/`candidate`) et sont exportés — c'est le comportement attendu (pas de suppression automatique des items existants).
- Les profils francophones (Réseaux, Questions de comm, etc.) retournent 20 items chacun → bien mais certains peuvent être hors-sujet radio ; le scoring les filtre.

### Prochaine étape
**Prompt 2** — Contrat public enrichi : ajouter `authors`, `container_title`, `item_type` pour les sources bibliographiques uniquement (crossref/openalex/hal), avec anti-fuite e-mail renforcé.

---

---

## 7. Bilan — Prompt 2 / Plan final (2026-05-25)

**Objectif :** enrichir le contrat public avec `authors`, `container_title`, `item_type` pour les sources bibliographiques uniquement, avec anti-fuite e-mail renforcé.

### Fichiers modifiés
- `scripts/core/models.py` : ajout de `container_title: str | None = None` dans `RadioWatchItem` + validateur `strip_text` étendu.
- `scripts/core/normalize.py` : 
  - HAL : `container_title` ← `journalTitle_s`
  - Crossref : `container_title` ← `container-title`
  - OpenAlex : `container_title` ← `source_name` (quand non générique), `authors` ← `_openalex_authors()` (nouvelle fonction sur `authorships`)
  - Fusion : `_merge_duplicate_item` inclut `container_title` (existing or incoming)
- `scripts/export/export_public.py` :
  - Ajout `import re`, `EMAIL_RE`, `BIBLIOGRAPHIC_SOURCE_FAMILIES = {"crossref","openalex","hal"}`
  - `PUBLIC_ITEM_KEYS` → alias de `BIBLIOGRAPHIC_ITEM_KEYS` (13 clés)
  - `EDITORIAL_ITEM_KEYS` (10 clés), `BIBLIOGRAPHIC_ITEM_KEYS` (13 clés)
  - `FORBIDDEN_PUBLIC_KEYS` : suppression de `authors` (maintenant autorisé pour biblio)
  - Nouvelle fonction `_clean_authors()` : regex anti-fuite e-mail
  - `_item_to_public()` : ajout conditionnel de `authors`, `container_title`, `item_type` selon `source_family`
- `tests/test_export_public.py` : +6 nouveaux tests (enrichi biblio, absence editorial, nettoyage e-mail, HAL biblio, whitelist 13 clés, anti-fuite renforcé) ; mises à jour des assertions des tests existants (`EDITORIAL_ITEM_KEYS` vs `BIBLIOGRAPHIC_ITEM_KEYS`)
- `LEGAL_AUDIT.md` : mise à jour « Note de clôture V3 académique » + section « Champs publics supplémentaires » avec justification de l'implémentation.

### Compteurs réels
- `make test` : **164/164 passés** (159 initiaux + 5 nouveaux nets)
- `make export-public` : 505 items publics (inchangé)
- **295 bibliographiques** (crossref/openalex/hal) → 13 clés chacun, dont `authors`, `container_title`, `item_type`
- **210 éditoriaux** (RSS) → 10 clés strictes, sans auteurs ni revue
- Items biblio avec `authors` non vides : **71/295** (les 224 restants ont `authors: []` — base existante sans `authorships` parsés ; peuplé lors du prochain `make run`)
- `container_title` : `null` pour les items existants en base (champ absent avant ce prompt) ; peuplé pour les nouvelles ingestions

### Scan anti-fuite
- **0 clé interdite** dans l'index public
- **0 e-mail** dans le contenu
- **0 chemin local**
- **0 erreur de schéma** (items biblio = 13 clés exactes, éditoriaux = 10 clés exactes)

### Règle bibliographique / éditoriale
- `source_family ∈ {crossref, openalex, hal}` → contrat bibliographique (13 clés)
- Sinon (RSS, blogs) → contrat éditorial (10 clés)
- Encodé dans `BIBLIOGRAPHIC_SOURCE_FAMILIES` et la validation per-item de `_item_to_public()`

### Limites
- `container_title` est `null` pour les 660 items déjà en base (champ nouveau, non rétro-alimenté automatiquement). Il se peuplera naturellement au prochain `make run` pour les items issus de Crossref/OpenAlex/HAL.
- `item_type` = alias de `source_type.value` : légèrement redondant mais explicitement demandé dans le plan (signalement bibliographique distinct du type de source).

### Prochaine étape
**Prompt 3** — Interface Hugo : afficher `authors`, `container_title`, `item_type` sur les cartes + tri + filtre par période + bloc « À propos / contact / retrait ».

---

---

## 9. Bilan — Prompt 4 / Routine hebdo + rétention + gel (2026-05-25)

**Objectif :** commande hebdomadaire unique (`make weekly`), rétention 18 mois, documentation finale, gel du projet.

### Fichiers créés / modifiés

- `scripts/core/prune.py` (nouveau) : `prune_old_items()` (pur, testable) + `prune_db()` (I/O) — élagage 18 mois, `exported` toujours préservé, retour de compteurs.
- `scripts/pipeline.py` : ajout import `prune_db` ; nouveau champ `prune` dans `PipelineFunctions` ; step `prune` entre `normalize` et `scoring` ; flag `--skip-prune` ; `run_pipeline(skip_prune=)`.
- `scripts/weekly_report.py` (nouveau) : récapitulatif lisible (compteurs db + public + sources + doublons DOI) + scan anti-fuite (clés interdites, emails non autorisés, chemins locaux), retour de code 0/1/2.
- `antenne_radio/Makefile` : cible `weekly` ajoutée + `.PHONY` mis à jour.
- `tests/test_prune.py` (nouveau) : 8 tests (recent kept, old pruned, old exported kept, batch mixte, liste vide, fallback discovered_at, prune_db file-level, pas de ré-écriture si rien à élagger).
- `tests/test_pipeline.py` : step `prune` injecté dans les fonctions mock, ordre mis à jour (× 3 assertions de séquence), liste des statuts dans le test de skip (7 → 8 steps).
- `antenne_radio/README.md` : réécriture complète (routine hebdo, whitelist enrichie, rétention 18 mois, état de gel).
- `antenne_radio/LEGAL_AUDIT.md` : note de clôture Prompt 4 ajoutée (pruning, `make weekly`, scan final, 172 tests).
- `antenne_radio/01_RESSOURCES_SUIVIES.md` : compteurs finaux mis à jour, section « Routine hebdomadaire » et « État du projet — Gel plan final » ajoutées.

### Commandes lancées

- `.venv/bin/pytest tests/test_prune.py tests/test_pipeline.py -v` → **12/12 passés**.
- `.venv/bin/pytest -q` → **172/172 passés**.
- `.venv/bin/python scripts/pipeline.py --skip-rss --skip-hal --skip-crossref --skip-openalex --skip-export` → pruning 62 items.
- `.venv/bin/python scripts/export/export_public.py` → 462 items publics.
- `.venv/bin/python scripts/weekly_report.py` → scan OK (EXIT=0).

### Compteurs réels après pruning + export (2026-05-25)

- `db.json` avant pruning (depuis Prompt 1) : **660 items** (to_read=292, candidate=266, ignored=102)
- `db.json` après `make weekly` (pruning 18 mois + rescore) : **599 items** (to_read=260, candidate=254, ignored=85)
- Items élaguées : ~61-62 items (non-exported, publiés/découverts avant novembre 2024)
- Items `exported` préservés (hors rétention) : **0** (aucune curation marquée exported)
- Index public final (`make weekly`) : **463 items publics**, 28 sources
- Doublons DOI : **0**

### Scan anti-fuite exhaustif (2026-05-25)

- **0 clé interdite** dans l'index public (raw, abstract, scores, etc.)
- **0 fuite e-mail** non autorisée (email de contact `mathieu.allag@gmail.com` dans le bloc « À propos » : faux positif documenté, intentionnellement public)
- **0 chemin local** (correction du regex `/home/` qui matchait faussement les URLs SAGEPUB)
- Régression regex documentée et corrigée : `LOCAL_PATH_RE` éxclut désormais les chaînes commençant par `http://` ou `https://`

### Architecture `make weekly`

```
make weekly
  → bash .env.local + scripts/pipeline.py
      → ingest_rss + ingest_hal + ingest_crossref + ingest_openalex
      → normalize (merge existant + nouveau)
      → prune (18 mois, sauf exported)
      → scoring
      → export_obsidian
  → scripts/export/export_public.py
  → scripts/weekly_report.py (récapitulatif + scan, EXIT 0/1/2)
  → [si EXIT=0] affiche commandes git manuelles
```

### Règle de rétention

- Implémentée dans `scripts/core/prune.py`, step `prune` dans `pipeline.py`.
- Fenêtre : **18 mois glissants** depuis `published_at` (ou `discovered_at` si absent).
- Exception : `status == exported` → toujours conservé.
- Testée avec 8 cas unitaires (dont fallback `discovered_at`, batch mixte, pas de ré-écriture si 0 pruned).

### Limites

- Le pruning se déclenche à chaque `make run` (pas seulement dans `make weekly`). Comportement attendu et documenté.
- `make weekly` imprime les commandes git même si le scan échoue ? Non — si `weekly_report.py` retourne EXIT≠0, make s'arrête avant l'affichage des commandes git (comportement make standard : erreur bloquante).
- Les items `la_lettre_pro` anciens (30 items, all pré-novembre 2024) ont été élaguées par le pruning 18 mois → comportement attendu.

### État final du projet

**Plan final gelé.** Le projet est en état opérationnel complet :
- Pipeline de veille avec scoring et plancher académique
- Rétention 18 mois automatique
- Interface Hugo complète (filtres, tri, deep-linking, bloc légal)
- Commande hebdo unique `make weekly` avec scan intégré
- Documentation à jour (README, LEGAL_AUDIT, 01_RESSOURCES_SUIVIES)
- 172 tests, 0 test masqué, 0 secret en dépôt

**Prochaine étape :** aucune. Maintenance par `make weekly` chaque semaine. Pour une V4 japonaise (CiNii, NDL, J-STAGE), ouvrir un nouveau plan.

---

## 5. Perspectives : V4 Japonaise

La future V4 couvrira la littérature académique japonaise (mini-FM, radios communautaires, Tetsuo Kogawa, sound/media studies au Japon).

### Sources cibles
- `CiNii`
- `NDL` (Bibliothèque nationale de la Diète)
- `J-STAGE`

### Prérequis pour l'implémentation
1. **Audit préalable** : Analyse des conditions d'utilisation, obligations d'attribution, rate limiting et encodages spécifiques.
2. **Contrat V4** : Définir la whitelist publique minimale (gestion des titres japonais et de la romanisation).
3. **Approche incrémentale** : Développer un connecteur mocké à la fois, sans appels live incontrôlés, sans cron, et sans auto-commit.

---

## 8. Bilan — Prompt 3 / Interface Hugo aboutie (2026-05-25)

**Objectif :** rendre les nouveaux champs (`authors`, `container_title`, `item_type`) sur les cartes, ajouter tri et filtre par période, et implémenter le bloc légal « À propos / contact / retrait ».

### Fichiers modifiés
- `assets/js/antenne-radio.js` (réécriture complète) :
  - **Nouveaux contrôles** : `yearSelect` (filtre par année, rempli en ordre décroissant) + `sortSelect` (tri date ↓, date ↑, titre A→Z).
  - **`fillYearSelect()`** : remplissage manuel en ordre chronologique inversé (ne passe pas par `fillSelect` qui trie alphabétiquement).
  - **`sortItems(arr)`** : sort par date desc (défaut), date asc, ou titre collator.
  - **`itemMatches()`** : filtre année ajouté (`startsWith(year)`) + champ de recherche étendu à `container_title` et `authors`.
  - **`applyFilters()`** : appelle `sortItems()` après `.filter()`.
  - **`updateURL()`** : paramètres `year` et `sort` (omis si `sort === "date-desc"`).
  - **`syncFiltersFromURL()`** : lecture de `year` et `sort` depuis l'URL.
  - **`renderActiveFilters()`** : badges pour year et sort (sort non affiché si valeur par défaut ; reset sort → "date-desc").
  - **`createCard()`** : affichage conditionnel de `container_title` (class `antenne-radio-container-title`, dans le head, tronqué ellipsis) et `authors` (class `antenne-radio-authors`, max 3 noms + indicateur "+N", sous le titre).
  - **`createEmptyState()`** : reset étendu à yearSelect et sortSelect.
  - **`clearFiltersBtn`** : reset étendu à yearSelect et sortSelect.

- `layouts/antenne-radio/list.html` :
  - **Formulaire restructuré** : 2 rangées via `.antenne-radio-form-filters` (4 cols : catégorie, source, langue, **année**) + `.antenne-radio-form-actions` (3 cols : recherche, **tri**, réinitialiser). CSS `flex-direction: column`.
  - **Noscript enrichi** : `{{ with .container_title }}` + `{{ if .authors }}` avec `first 3` et `sub $authorCount 3` pour l'indicateur "+N".
  - **Section éthique renommée** « À propos & contact » avec 4 §§ complets : finalité, données publiées, droits PI, demande de retrait (adresse `mathieu.allag@gmail.com`), puis sous-titre « Sources référencées » + liste attributions.
  - **CSS** : `.antenne-radio-container-title` (sky, italic, monospace, ellipsis), `.antenne-radio-authors` (subtext1, monospace, 0.72rem, ellipsis), `.antenne-radio-sub-title` (sapphire, Georgia), `.antenne-radio-ethics p a` (mauve). Responsive mis à jour : `@media (max-width: 900px)` → form-filters 2 cols, form-actions 1fr+auto ; `@media (max-width: 640px)` → tout en 1 col. Pas de `transition-all`, pas de `will-change`.

### Résultat build
- `pnpm run build` : **OK** (1002 ms, 83 pages, 0 erreur).
- HTML généré vérifié : 0 clé interdite (score, abstract, raw, keywords_matched).
- Noscript : 50 cartes, `container_title` rendu si non-null, `authors` rendu pour 1 item (Otto Wanke, bibliographique) — correct.
- `antenne-radio-filter-year` et `antenne-radio-filter-sort` présents dans le HTML.
- `mathieu.allag@gmail.com` et mention « À propos » présents.

### Scan anti-fuite (HTML public)
- 0 clé interdite dans `public/antenne-radio/index.html`.
- 0 chemin local, 0 e-mail interne.
- Email de contact (`mathieu.allag@gmail.com`) : **intentionnellement public** (retrait).

### Points UX à surveiller
- `container_title` absent des items éditoriaux (RSS) — comportement attendu, dégradation gracieuse.
- `authors` vides sur la majorité des items (`[]`) car la base existante n'avait pas `authorships` avant le Prompt 2. Se peuplera au prochain `make run`.
- `item_type` non affiché séparément (= `source_type` pour tous les items actuels — redondant, omis par choix).
- Deep-linking : `?year=2024&sort=date-asc` fully synchronisé.

### Prochaine étape
- Lancer `make run` pour ingérer de nouveaux items avec `authors` et `container_title` peuplés.
- Optionnel : tester le deep-linking sur mobile (390×844) en conditions réelles.

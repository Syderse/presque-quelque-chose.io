# Mémoire matérielle - Antenne Radio

> [!NOTE]
> Ce document est la mémoire technique consolidée du sous-projet `antenne_radio`. Il contient l'état actuel de l'architecture, les contrats de données critiques, la politique de sécurité anti-fuite et la synthèse historique des versions.

## 1. Reprise rapide & État du pipeline (v3)

- **Démarrage rapide** : Lancer `git status --short`, lire `docs/AGENTS.md` et `antenne_radio/README.md`.
- **Architecture & Isolation** : Le sous-projet vit exclusivement dans `antenne_radio/` avec son `.venv` et ses dépendances. Pas de cron global, pas d'auto-commit, pas de LLM dans le pipeline.
- **Pipeline opérationnel** :
  - **Ingestion RSS/Atom** : 10 sources actives (voir section 4).
  - **Ingestion Académique** : HAL (requête ciblée resserrée, limite 20) + Crossref (4 revues actives, `rows: 20`) + OpenAlex (venue JSS active). `CROSSREF_MAILTO` et `OPENALEX_MAILTO` locaux obligatoires avant tout appel réseau.
  - **Normalisation & Déduplication** : Fusion dans `data/normalized/db.json` (295 items) par ID stable (DOI normalisé > URL normalisée > Titre/Date). Jamais de suppression automatique des `ignored`.
  - **Scoring lexical** : Mots-clés positifs, négatifs (`-6` pour le bruit médical/clinique) et techniques (`-2` pour le bruit d'ingénierie télécom/MIMO/5G), avec un boost `source_name: 1`. Seuils : `to_read >= 6`, `candidate >= 2`, `ignored < 2`.
  - **Exports** :
    - *Privés* : Obsidian hebdomadaire (`veille-YYYY-MM.md`), Zotero CSL JSON.
    - *Public* : `static/antenne-radio/index.json` (239 items) filtré selon une whitelist stricte anti-fuite.
- **Intégration Hugo** : Page `/antenne-radio/` avec grille responsive de cartes néo-brutalistes (couleurs Catppuccin Mocha), fallback `<noscript>` (50 premières cartes), et hydratation client via Vanilla JS dynamique optimisé de 7.6 Ko (recherche, filtres ET multi-critères, deep-linking sans pollution d'historique, rendu progressif par lots de 50).

---

## 2. Contrats de données & Sécurité (Anti-fuite)

> [!IMPORTANT]
> **Confidentialité absolue (Anti-fuite)** : Interdiction stricte de publier abstracts (y compris `abstract_inverted_index`), raw dumps, logs de pipeline, scores internes, explications lexicales, mots-clés internes, auteurs, tags ou chemins locaux. Seules les métadonnées de la whitelist publique sont exportables.

### Whitelist publique autorisée (`index.json`)
Chaque notice exportée doit contenir **exclusivement** les clés suivantes :
- `id`, `title`, `url`, `doi`, `published_at`, `source_name`, `source_type`, `language`, `source_family`, `attribution_id`.

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

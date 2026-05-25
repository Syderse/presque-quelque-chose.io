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

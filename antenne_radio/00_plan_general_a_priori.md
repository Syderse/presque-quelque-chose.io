# Conception et Implémentation d'une Antenne de Veille en Études Radiophoniques

## 1. Résumé Exécutif

La création d'une infrastructure de veille scientifique spécialisée dans les études radiophoniques (radio studies), l'histoire de la radio libre, la mini-FM japonaise et les médias mineurs requiert une approche dépassant de loin le simple agrégateur de flux RSS. L'objectif est d'édifier un système robuste, maintenable individuellement et interopérable, capable de capter, de normaliser et de redistribuer des données issues d'écosystèmes documentaires hétérogènes (francophones, anglophones et japonais).

Le concept architectural s'articule autour de la métaphore de l'« antenne superhétérodyne ». Dans un récepteur radiophonique classique, ce circuit convertit les fréquences multiples captées par l'antenne en une fréquence intermédiaire unique (FI) afin de les amplifier et de les filtrer efficacement avant de les restituer sous forme de signal audible. De manière analogue, le système conçu ici capte des signaux disparates (flux RSS, JSON-LD, requêtes OpenSearch, requêtes API Solr) et les convertit en un modèle de données pivot standardisé (la fréquence intermédiaire). Ces données sont ensuite soumises à un filtre de pertinence (scoring algorithmique) avant d'être redirigées vers des interfaces de lecture privées (Zotero, Obsidian) et publiques (site statique Hugo).

L'analyse démontre que la pérennité de ce système pour un projet de thèse repose sur l'élimination des dépendances aux bases de données complexes au profit d'une architecture orientée "Doc-as-Code" (fichiers plats JSON et Markdown), soutenue par une automatisation via GitHub Actions et des connecteurs Python légers respectant rigoureusement les contraintes éthiques et légales des API interrogées.

## 2. Architecture Recommandée

L'architecture est structurée en sept couches fonctionnelles distinctes, garantissant que chaque étape du traitement des données est isolée, auditable et extensible sans perturber le reste de la chaîne.

|**Couche Architecturale**|**Fonction Principale**|**Technologies et Standards**|**Description Technique Détaillée**|
|---|---|---|---|
|**1. Sources (Antenne)**|Détection et émission|RSS/Atom, API REST, SRU, OpenSearch|Ingestion de flux natifs de revues, interrogations d'API institutionnelles (Crossref, OpenAlex, CiNii, HAL), et surveillance d'altérations de pages via outils tiers.|
|**2. Ingestion (Tuner)**|Extraction asynchrone|Python (`httpx`, `feedparser`)|Scripts de moissonnage modulaires intégrant la gestion des limites de requêtes (rate limiting) et des en-têtes d'identification polie (Polite Pool).|
|**3. Stockage (Mémoire)**|Persistance à long terme|JSON local, Git|Conservation des données sous forme de fichiers plats (`db.json`). Cette méthode garantit une lisibilité décennale sans dépendance à un moteur de base de données relationnelle.|
|**4. Enrichissement (Filtre)**|Structuration et tri|Python (`pydantic`), Expressions Régulières|Normalisation des métadonnées, dédoublonnage cryptographique (hachage par DOI ou URL), détection de la langue, et calcul du score de pertinence documentaire.|
|**5. Sortie Privée (Monitoring)**|Intégration personnelle|Markdown, CSL-JSON, OPML|Production de notes synthétiques pour Obsidian et d'exports compatibles avec les systèmes d'ingestion de Zotero.|
|**6. Sortie Publique (Diffusion)**|Publication web|Hugo (Data Templates), HTML/CSS|Moteur de rendu statique générant des pages de ressources bibliographiques et un flux RSS sélectif à partir des données Json préalablement filtrées.|
|**7. Automatisation (Horloge)**|Ordonnancement|GitHub Actions, YAML|Exécution séquentielle des scripts d'ingestion et de publication selon une planification prédéfinie (cron), incluant la gestion du cache et des journaux d'erreurs.|

## 3. Comparaison des Stacks Techniques

L'évaluation des choix technologiques doit s'inscrire dans le contexte d'une recherche doctorale : les ressources temporelles pour la maintenance informatique sont limitées, mais l'exigence de maîtrise algorithmique et de transparence est élevée. L'analyse compare quatre approches.

|**Paramètre**|**Stack A : Minimaliste (Python/Hugo)**|**Stack B : JS/TS (Node/Astro)**|**Stack C : FreshRSS (PHP)**|**Stack D : Full-Stack (SQLite/FastAPI)**|
|---|---|---|---|---|
|**Langage**|Python|JavaScript / TypeScript|PHP|Python / JavaScript|
|**Stockage**|Fichiers JSON plats (Git)|Fichiers JSON plats (Git)|MariaDB / PostgreSQL|SQLite|
|**Complexité de déploiement**|Très faible (GitHub Actions)|Faible (GitHub Actions)|Moyenne (Docker / VPS requis)|Haute (Serveur API + Frontend)|
|**Transparence algorithmique**|Excellente|Excellente|Faible (outil clé en main)|Moyenne|
|**Pérennité (10+ ans)**|Maximale (Fichiers plats)|Haute|Dépend du mainteneur|Vulnérable à l'obsolescence des frameworks|

**Justification du choix (Stack A) :** La stack minimaliste orientée "Doc-as-Code" s'impose comme la solution optimale. Python dispose des bibliothèques les plus robustes pour l'ingestion d'API académiques (`httpx`) et la validation de schémas de données (`pydantic`). L'absence de serveur de base de données (SQLite ou PostgreSQL) élimine le besoin d'administration système. Les données résidant dans un fichier `db.json` versionné sur GitHub, elles sont nativement et trivialement lisibles par le moteur de templates de Hugo pour générer le site statique. Ce choix préserve le temps du doctorant tout en lui offrant un contrôle total sur le code qu'il souhaite comprendre. L'utilisation de FreshRSS est écartée comme infrastructure centrale car elle complexifie l'ingestion de données issues d'API REST (comme HAL ou CiNii) qui ne sont pas nativement au format RSS.

## 4. Sources et APIs à Surveiller

L'hétérogénéité des études radiophoniques impose une stratégie de captation multicanale. L'infrastructure doit composer avec des standards occidentaux, des protocoles spécifiques au monde académique japonais, et des éditeurs commerciaux aux pratiques variables.

### 4.1. Métadonnées Académiques Générales

- **Crossref REST API** : Crossref offre une API REST exhaustive pour les métadonnées de publications dotées d'un DOI. Les requêtes par ISSN de revue (`/journals/{issn}/works`) permettent de contourner l'absence de flux RSS chez certains éditeurs. L'étiquette de l'API exige l'utilisation d'une "Polite Pool" en fournissant une adresse e-mail valide dans l'en-tête de requête. Des limites de requêtes (rate limits) sont appliquées dynamiquement et annoncées via les en-têtes `X-Rate-Limit-Limit` et `X-Rate-Limit-Interval`. Le script d'ingestion devra obligatoirement analyser ces en-têtes et implémenter des pauses d'exécution pour éviter les blocages temporaires.
    
- **OpenAlex API** : Contrairement à Crossref qui se concentre sur les enregistrements de DOI, OpenAlex cartographie les entités de recherche (travaux, auteurs, concepts, sources). Cette API permet d'effectuer des recherches sur des réseaux conceptuels vastes (ex: _radio studies_, _sound studies_).
    
- **DOAJ (Directory of Open Access Journals)** : Expose une API facilitant l'identification et la récupération de données concernant des articles en libre accès.
    

### 4.2. Écosystème Japonais

- **CiNii Research / CiNii Articles** : Base de données centrale de l'Institut National d'Informatique (NII) du Japon. L'interrogation automatisée de CiNii via OpenSearch requiert obligatoirement l'obtention préalable d'un identifiant d'application (`appid`) via un formulaire d'enregistrement. Une fois l'identifiant obtenu, les requêtes s'effectuent sur `ci.nii.ac.jp/opensearch/fulltext`, en spécifiant des mots-clés (`q=ミニFM` ou `q=粉川哲夫`), des options de tri (`sortorder`), et des formats de réponse tels que RSS, Atom ou JSON-LD (`format=jsonld`).
    
- **J-STAGE** : Plateforme japonaise majeure pour la publication scientifique. Les conditions d'utilisation de J-STAGE interdisent explicitement le _scraping_ agressif des métadonnées publiées. Il est impératif d'utiliser la "J-STAGE WebAPI" dédiée, qui délivre des données bibliographiques au format XML.
    
- **NDL Search (National Diet Library)** : La bibliothèque de la Diète nationale offre des API SRU, OpenSearch et OpenURL. Leur utilisation requiert une stricte conformité aux règles d'attribution ; les développeurs doivent créditer la NDL et indiquer la source originelle des métadonnées lors de leur affichage public.
    

### 4.3. Écosystème SHS et Francophone

- **HAL (Archives Ouvertes)** : L'API de recherche repose sur le moteur Apache Solr. Le point d'entrée `api.archives-ouvertes.fr/search/` accepte des requêtes complexes, utilisant par exemple le paramètre `q=keyword_s:(radio OR "radio libre" OR podcast)` et le paramètre de filtre `fq=docType_s:(ART OR THESE)`. Les résultats peuvent être formatés en JSON, XML, BibTeX ou CSL, facilitant grandement l'intégration.
    
- **Calenda et OpenEdition** : Ces plateformes fournissent des données très structurées. Calenda dispose d'une API REST et d'un générateur de requêtes HTTP permettant de créer des flux XML filtrés selon des champs disciplinaires ou des mots-clés spécifiques. OpenEdition propose également plus de 600 flux de syndication couvrant ses différentes collections et numéros de revues.
    

### 4.4. Revues Spécialisées et Surveillance de Pages

Plusieurs revues fondamentales sont à surveiller. Les stratégies diffèrent selon les éditeurs :

- _RadioMorphoses_ (OpenEdition) : Flux RSS natif disponible.
    
- _Journal of Radio & Audio Media_ (Taylor & Francis) : Flux RSS souvent masqué ou discontinu ; l'ingestion par API Crossref via l'ISSN est recommandée.
    
- _Radio Journal: International Studies in Broadcast & Audio Media_ (Intellect) : Bien que des flux RSS soient parfois signalés , une double stratégie (RSS + Crossref) assure la robustesse.
    
- _Sound Studies_ et _Journal of Sonic Studies_ : Stratégies mixtes requises.
    

Pour les pages web institutionnelles, appels à contributions isolés ou plateformes dépourvues de tout flux syndiqué ou API (ex: annonces de colloques sur des sites de laboratoires), l'outil **changedetection.io** se révèle pertinent. Exposant lui-même une API REST et générant des flux de sortie au format Atom, il permet d'isoler une section HTML spécifique d'une page surveillée (via des sélecteurs CSS ou XPath) et de n'émettre une alerte que lorsqu'un changement textuel significatif y survient.

## 5. Modèle de Données Pivot (JSON Schema)

La réussite du processus de normalisation ("démodulation") réside dans un schéma de données interne exhaustif et prévisible. Le modèle Pydantic conçu pour valider les éléments (items) de veille s'établit comme suit :

JSON

```
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "RadioWatchItem",
  "type": "object",
  "required": [
    "id", "title", "source_name", "source_type", "language", "status", "discovered_at"
  ],
  "properties": {
    "id": {
      "type": "string",
      "description": "Identifiant stable. Généré via Hash SHA-256 du DOI si présent. En l'absence de DOI, Hash SHA-256 de (Titre normalisé + Date + URL)."
    },
    "title": {
      "type": "string",
      "description": "Titre principal de la publication (traduit, translittéré ou natif)."
    },
    "title_original": {
      "type": "string",
      "description": "Conserve l'encodage natif UTF-8, indispensable pour les caractères japonais (Kanji, Hiragana, Katakana) issus de CiNii ou NDL."
    },
    "authors": {
      "type": "array",
      "items": { "type": "string" }
    },
    "source_name": { "type": "string" },
    "source_type": {
      "type": "string",
      "enum": ["journal", "book", "cfp", "archive", "blog", "thesis", "dataset", "unknown"]
    },
    "language": {
      "type": "string",
      "enum": ["fr", "en", "ja", "unknown"]
    },
    "published_at": { "type": "string", "format": "date-time" },
    "discovered_at": { "type": "string", "format": "date-time" },
    "url": { "type": "string", "format": "uri" },
    "doi": { "type": "string" },
    "abstract": { "type": "string" },
    "summary": {
      "type": "string",
      "description": "Note de synthèse locale rédigée par le chercheur."
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" }
    },
    "keywords_matched": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Trace des éléments lexicaux ayant déclenché la conservation de l'item."
    },
    "relevance_score": { "type": "integer", "default": 0 },
    "status": {
      "type": "string",
      "enum": ["new", "to_read", "reading", "read", "ignored", "saved_to_zotero"]
    },
    "zotero_uri": {
      "type": "string",
      "description": "URI locale (zotero://select/items/...) pour pont logiciel."
    },
    "notes_path": {
      "type": "string",
      "description": "Chemin relatif vers le fichier de note associé dans Obsidian."
    },
    "rights": {
      "type": "string",
      "description": "Gestion impérative du copyright et de l'attribution (ex: CC BY, Copyright Editeur, Mention NDL )."
    },
    "source_feed": { "type": "string" },
    "raw": {
      "type": "object",
      "description": "Objet de débogage stockant la structure originale retournée par l'API."
    }
  }
}
```

**Prévention des doublons :** Le hachage cryptographique de l'identifiant est la clé de voûte de la déduplication. Le processus de normalisation évaluera également des similarités structurelles floues (fuzzy matching) sur les titres pour identifier des documents pré-publiés (preprints) ou des actes de colloques réédités.

## 6. Arborescence du Dépôt

La compartimentation des logiques applicatives assure une maintenance aisée. Le dépôt se divise entre les configurations déclaratives, les moteurs d'ingestion programmatiques et l'espace de persistance.

radio-watch/

├── README.md # Documentation d'amorçage

├── Makefile # Raccourcis pour tests et exécutions locales

├── requirements.txt # Dépendances Python (pydantic, httpx, feedparser)

├── config/

│ ├── sources.yaml # URLs, ISSN, endpoints et identifiants

│ ├── keywords.yaml # Matrices lexicales FR, EN, JA

│ └── scoring.yaml # Poids algorithmique de la fonction de pertinence

├── scripts/

│ ├── core/

│ │ ├── models.py # Schéma Pydantic (JSON Schema validateur)

│ │ ├── deduplicate.py # Algorithme de hachage et de comparaison floue

│ │ └── scoring.py # Moteur d'évaluation sémantique

│ ├── ingest/

│ │ ├── ingest_rss.py # Traitement Atom/RSS

│ │ ├── ingest_crossref.py# Interrogation respectueuse de Crossref

│ │ ├── ingest_hal.py # Requêtes Apache Solr sur HAL

│ │ ├── ingest_cinii.py # Appels OpenSearch avec authentification appid

│ │ ├── ingest_ndl.py # Traitement SRU NDL Search

│ │ └── ingest_jstage.py # Connecteur J-STAGE WebAPI (XML)

│ ├── export/

│ │ ├── export_obsidian.py# Générateur Markdown / Dataview

│ │ ├── export_csl.py # Formateur CSL-JSON pour Zotero

│ │ └── export_hugo.py # Distillateur de données publiques

│ └── pipeline.py # Orchestrateur global appelant les scripts

├── data/

│ ├── raw/ # Décharges (dumps) temporaires des API

│ ├── normalized/ # Fichier db.json (Base de connaissance de vérité)

│ ├── public/ # Données expurgées pour publication statique

│ └── logs/ # Traces d'erreurs, requêtes et dépassements de taux

├── site/ # Dépôt imbriqué Hugo (Générateur statique)

│ ├── content/ # Arborescence des pages (Markdown)

│ ├── data/ # Lien symbolique vers data/public/

│ └── layouts/ # Modèles HTML pour rendu et flux RSS XML

├── tests/

│ ├── test_ingest.py # Validations unitaires des connecteurs

│ └── test_models.py # Validation des contraintes Pydantic

└──.github/

└── workflows/

└── veille.yml # CI/CD et exécution chronologique (Cron)

## 7. Plan de Développement en Phases

L'approche de développement itératif sécurise chaque composant avant d'introduire une complexité supplémentaire. L'ensemble est pensé pour fournir un retour sur investissement cognitif immédiat au doctorant.

**Phase 0 — Cadrage & Infrastructures**

- **Objectif** : Initialiser l'environnement virtuel Python, l'arborescence des dossiers et structurer les fichiers YAML de configuration.
    
- **Fichiers** : `config/sources.yaml`, `config/keywords.yaml`, `config/scoring.yaml`.
    
- **Critère de réussite** : Le dépôt est fonctionnel, les dépendances sont installées et le fichier de configuration est validable par un linter YAML.
    

**Phase 1 — Prototype RSS et Normalisation**

- **Objectif** : Développer le script `ingest_rss.py` utilisant `feedparser` pour lire cinq flux de revues ou d'appels, et concevoir le modèle de validation Pydantic `models.py`.
    
- **Critère de réussite** : Production d'un fichier `db.json` contenant les premiers items validés avec un identifiant SHA-256 généré.
    
- **Risque** : Non-conformité des balises temporelles des flux RSS nécessitant un parsing tolérant des dates.
    

**Phase 2 — Sources Académiques Occidentales (Crossref / HAL)**

- **Objectif** : Coder `ingest_crossref.py` (interrogation par ISSN avec _Polite Pool_) et `ingest_hal.py` (requêtes Solr).
    
- **Critère de réussite** : Enrichissement de `db.json` avec des métadonnées contenant des DOI fiables et gestion adéquate des limites de requêtes (`X-Rate-Limit-Limit`).
    

**Phase 3 — Sources et API Japonaises**

- **Objectif** : Enregistrement et obtention du `appid` pour CiNii. Implémentation de `ingest_cinii.py`, `ingest_jstage.py` et `ingest_ndl.py`.
    
- **Critère de réussite** : Le système capture avec succès les encodages UTF-8 pour le vocabulaire japonais ciblé (粉川哲夫, ミニFM) et préserve l'intégrité des caractères dans le champ `title_original`.
    

**Phase 4 — Scoring Algorithmique et Tri**

- **Objectif** : Développer le script d'évaluation `scoring.py` qui attribue des points selon la présence de mots-clés dans les métadonnées.
    
- **Critère de réussite** : Les items atteignant un seuil défini (ex: +5) voient leur `status` transiter de `new` à `to_read`.
    

**Phase 5 — Export PKM (Zotero / Obsidian)**

- **Objectif** : Coder `export_obsidian.py` pour générer un fichier Markdown de synthèse hebdomadaire et `export_csl.py` pour produire un export CSL-JSON.
    
- **Critère de réussite** : Import manuel sans erreur dans Zotero via le fichier CSL-JSON et affichage cohérent du Markdown dans Obsidian.
    

**Phase 6 — Publication Web Statique (Hugo)**

- **Objectif** : Créer `export_hugo.py` pour distiller les données de `db.json` vers `site/data/public_veille.json`. Configurer les _data templates_ HTML de Hugo.
    
- **Critère de réussite** : Le site génère des pages web par taxonomie (Japon, Appels, Sound Studies) listant les ressources curatées.
    

**Phase 7 — RSS Personnel et Diffusion**

- **Objectif** : Concevoir le template XML `site/layouts/veille/rss.xml` permettant à Hugo de générer un flux Atom/RSS personnel listant les trouvailles publiques.
    
- **Critère de réussite** : Le flux est validé par le standard W3C Feed Validation Service.
    

**Phase 8 — Automatisation et GitHub Actions**

- **Objectif** : Rédiger le workflow YAML `.github/workflows/veille.yml`.
    
- **Critère de réussite** : Déclenchement quotidien (Cron) exécutant l'entièreté de la chaîne d'ingestion, enregistrant le nouveau `db.json` sur Git, et redéployant le site Hugo.
    

**Phase 9 — Durcissement, Logs et Gestion des Erreurs**

- **Objectif** : Implémenter des tests unitaires (`pytest`) systématiques pour le parsing des dates, le hachage cryptographique et capturer les exceptions réseau de `httpx`.
    
- **Critère de réussite** : Lors d'une indisponibilité temporaire d'une API, le système consigne une erreur (`WARNING`) dans `logs/api.log` mais termine son exécution sur les autres sources.
    

## 8. Stratégie de Publication sur Site (Hugo)

L'architecture s'appuyant sur des fichiers plats rend l'intégration au générateur de sites statiques Hugo triviale et élégante. Le fichier `public_veille.json` (préalablement purgé des abstracts sous droits pour respecter le droit d'auteur) est déposé dans le répertoire `site/data/`.

Le moteur de _Data Templates_ de Hugo permet alors de parcourir cet objet JSON. Les modèles de pages (`layouts/veille/list.html`) intègrent une logique de tri itératif :

- **Taxonomie par sources** : Génération de la page `/veille-radio/appels/` en filtrant la collection sur `if eq.source_type "cfp"`.
    
- **Taxonomie linguistique et thématique** : Création de la vue `/veille-radio/japon/` en isolant les items où le tableau `keywords_matched` contient des entrées provenant du dictionnaire japonais ou où `language` équivaut à `ja`.
    
- **Micro-éditorialisation** : La page d'index affiche le titre, les auteurs, le DOI sous forme de lien de redirection, et, de manière optionnelle, le champ `summary` où le chercheur a déposé une courte note personnelle explicative. L'interface demeure minimaliste, orientée vers le texte, respectant la sobriété académique.
    
- **Syndication sortante** : Le fichier `layouts/veille/rss.xml` compile ces mêmes entrées dans un format RSS 2.0 ou Atom, devenant ainsi la fréquence d'émission finale de l'antenne radiophonique.
    

## 9. Stratégie Zotero et Obsidian

La centralisation des données bibliographiques est indispensable pour l'écriture de la thèse.

- **Zotero** : L'infrastructure génère un export CSL-JSON. Le module Zotero Better BibTeX est capable d'importer ce format qui préserve une excellente fidélité des métadonnées (types d'articles, numéros, auteurs). Une fois l'item ajouté dans Zotero, l'identifiant interne de Zotero peut être copié dans le champ `zotero_uri` du fichier `db.json` (ex: `zotero://select/items/1_XXXXX`), créant un pont bidirectionnel cliquable. Bien que Zotero possède son propre agrégateur RSS , l'utilisation de cette infrastructure externe (l'antenne) permet un pré-filtrage sémantique algorithmique impossible à réaliser dans Zotero nativement.
    
- **Obsidian** : Le script Python produit un document Markdown hebdomadaire résumant l'activité de la veille. Chaque bloc Markdown est précédé d'un encart YAML formel. Cette pratique permet au plugin communautaire _Dataview_ d'Obsidian de lire ces fichiers comme une base de données locale, offrant au doctorant la possibilité de requêter dynamiquement sa veille directement dans son outil de prise de notes (PKM).
    

## 10. Risques Juridiques, Éthiques et Techniques

L'édification d'un système de moissonnage de métadonnées s'accompagne d'impératifs légaux et techniques de premier ordre, particulièrement dans un écosystème académique mondialisé.

- **Droit d'Auteur et Copyright (Résumés et Textes intégraux)** : De nombreux résumés (abstracts) figurant dans les bases de données (comme Crossref ou J-STAGE) sont soumis au copyright de l'éditeur scientifique commercial. La reproduction de ces résumés _in extenso_ sur le site public Hugo constitue une infraction. La stratégie de remédiation codée dans le script `export_hugo.py` consiste à purger ce champ avant le dépôt dans `site/data/`, ne conservant que le droit de citation classique (titre, auteur, source, DOI).
    
- **Conditions d'utilisation (Scraping vs. API)** : La plateforme japonaise J-STAGE précise expressément que le _scraping_ automatisé des pages web peut constituer une violation de la clause "Activités interdites" de ses conditions d'utilisation. Il est impératif d'utiliser la J-STAGE WebAPI officielle, qui fournit les données dans un cadre réglementaire défini et au format XML.
    
- **Attribution des sources (Licences CC et NDL)** : Les métadonnées obtenues via des institutions publiques comme la National Diet Library (NDL Search) via OpenSearch imposent l'ajout d'une clause d'attribution claire lors de la diffusion publique de ces données. L'antenne devra générer automatiquement la mention : _« Métadonnées extraites de NDL Search / J-STAGE »_ dans l'interface Hugo.
    
- **Gestion des limites d'interrogation (Rate Limiting)** : L'API de Crossref, fortement sollicitée à l'échelle mondiale, impose des limites dynamiques (Rate Limits) transmises dans les en-têtes de réponse HTTP. Le code Python d'ingestion doit implémenter un parseur d'en-tête scrutant `X-Rate-Limit-Limit` et `X-Rate-Limit-Interval`. L'algorithme doit appliquer un délai d'attente (backoff) si les limites s'approchent, garantissant que l'infrastructure reste une cliente éthique sur les réseaux académiques.
    

## 11. Roadmap

La concrétisation de l'antenne radiophonique suit un plan progressif de maturation technique :

- **v0.1 (Prototype Local)** : Capacité à lire cinq sources (RSS + HAL), valider les données via Pydantic, dédoublonner, et générer un rapport Markdown basique. Stockage local unique.
    
- **v0.2 (Écosystème Avancé)** : Intégration complète des API REST (Crossref, CiNii OpenSearch avec `appid`, J-STAGE). Mise en place effective du moteur de scoring pondéré et de l'export CSL-JSON pour Zotero.
    
- **v1.0 (Automatisation & Publication)** : Exécution de la chaîne complète via GitHub Actions. Déploiement automatisé du site Hugo contenant le filtrage taxonomique et le flux syndiqué RSS personnel. Robustesse des journaux d'erreurs face aux aléas du réseau.
    

---

## 12. Série Complète de Prompts Codex / Claude Code

Les vingt invites de commandes (prompts) suivantes constituent le cahier d'implémentation formel. Elles doivent être exécutées séquentiellement dans un assistant de codage.

**Prompt 1 — Initialisation du dépôt et structure**

> Contexte : Création de la structure d'une infrastructure de veille académique Python.
> 
> Objectif : Initialiser le dépôt, générer le `README.md` et le `requirements.txt`, et créer l'arborescence des dossiers.
> 
> Contraintes : Utiliser `pydantic`, `httpx`, `feedparser`, `pyyaml`. Créer les répertoires `config/`, `scripts/core/`, `scripts/ingest/`, `scripts/export/`, `data/raw/`, `data/normalized/`, `data/logs/`, `tests/`. Ne créer aucun script Python logique pour l'instant.
> 
> Fichiers : `requirements.txt`, `README.md`.
> 
> Tests : Lancer `tree` et afficher le résultat de `git status --short`. Résumer les actions.

**Prompt 2 — Fichiers de configuration YAML**

> Contexte : Configuration externe modifiable des cibles de la veille.
> 
> Objectif : Créer les trois fichiers YAML fondateurs dans `config/`.
> 
> Contraintes : `sources.yaml` doit inclure au moins Calenda (API URL) et RadioMorphoses (RSS URL). `keywords.yaml` doit inclure trois catégories (fr, en, ja) avec des termes comme "schizoanalyse", "radio studies", "ミニFM". `scoring.yaml` doit inclure une matrice d'addition/soustraction de points basée sur la présence de mots ou d'auteurs.
> 
> Fichiers : `config/sources.yaml`, `config/keywords.yaml`, `config/scoring.yaml`.
> 
> Tests : Exécuter une vérification simple de syntaxe YAML. Vérifier `git status`.

**Prompt 3 — Modèle de données pivot (Pydantic)**

> Contexte : Définition du schéma strict (Single Source of Truth) pour les items de veille.
> 
> Objectif : Créer `scripts/core/models.py`.
> 
> Contraintes : Définir la classe `RadioWatchItem` héritant de Pydantic `BaseModel`. Inclure les champs : id (string, obligatoire), title, title_original (pour préserver l'UTF-8 japonais natif), authors (list), source_name, source_type, language, abstract, url, doi, relevance_score (int, defaut 0), status (enum : new, to_read, ignored). Ajouter une méthode interne `generate_id()` calculant un hash SHA-256 basé sur le DOI ou (title + date).
> 
> Tests : Créer `tests/test_models.py` validant la création d'un objet valide et rejetant un objet invalide. Lancer `pytest`.

**Prompt 4 — Ingestion RSS minimale**

> Contexte : Base de la captation de données (Antenne).
> 
> Objectif : Créer `scripts/ingest/ingest_rss.py`.
> 
> Contraintes : Lire `config/sources.yaml` pour trouver les URLs de type `rss`. Utiliser `feedparser`. Transformer les entrées extraites en objets correspondant au schéma de `models.py` (sans validation stricte à cette étape de sauvegarde). Sauvegarder un dictionnaire listant ces objets dans `data/raw/rss_dump.json`.
> 
> Tests : Exécuter le script sur une URL RSS fictive. Vérifier l'apparition de `rss_dump.json`. Vérifier `git status --short`. Ne faire qu'une fonctionnalité simple.

**Prompt 5 — Algorithme de normalisation et dédoublonnage**

> Contexte : Filtrage cryptographique et validation structurelle des métadonnées brutes.
> 
> Objectif : Créer `scripts/core/normalize.py`.
> 
> Contraintes : Le script parcourt les fichiers dans `data/raw/`. Il tente d'instancier un objet Pydantic valide pour chaque entrée. Il lit la base principale `data/normalized/db.json` (qu'il crée si elle n'existe pas). Il insère l'objet uniquement si son `id` (hash SHA-256) n'est pas déjà présent dans la base.
> 
> Fichiers : `scripts/core/normalize.py`.
> 
> Tests : Lancer le script deux fois de suite avec les mêmes données brutes et s'assurer (via des assertions locales) qu'aucun doublon n'est inséré.

**Prompt 6 — Moteur de scoring par mots-clés**

> Contexte : Évaluation de la pertinence algorithmique de la recherche documentaire.
> 
> Objectif : Créer `scripts/core/scoring.py`.
> 
> Contraintes : Lire `data/normalized/db.json` et `config/scoring.yaml`. Pour chaque item avec le statut `new`, analyser les champs `title` et `abstract` avec les expressions régulières des mots-clés. Additionner les points. Si le score dépasse 5, changer le statut à `to_read`. Sinon, le changer à `ignored`. Mettre à jour `db.json`.
> 
> Tests : Générer un jeu d'essai JSON, lancer le script et vérifier le changement de statut.

**Prompt 7 — Exportation Markdown pour Obsidian**

> Contexte : Transfert de la veille dans un gestionnaire de notes local (PKM).
> 
> Objectif : Créer `scripts/export/export_obsidian.py`.
> 
> Contraintes : Lire `db.json`. Extraire les items avec le statut `to_read`. Générer un fichier Markdown nommé `veille-YYYY-WW.md`. Le fichier doit contenir un entête YAML (frontmatter) lisible par Dataview, et lister les items sous forme de structure de titres (H2, H3), avec le lien et l'abstract formaté. Changer le statut à `read` en base après export.
> 
> Tests : Lancer le script et vérifier la présence syntaxique correcte du fichier Markdown généré.

**Prompt 8 — Intégration de l'API Crossref (Polite Pool et Rate Limit)**

> Contexte : Moissonnage par ISSN pour les éditeurs commerciaux sans RSS.
> 
> Objectif : Créer `scripts/ingest/ingest_crossref.py`.
> 
> Contraintes : Utiliser `httpx`. Lire les ISSN dans `sources.yaml`. Appeler `/journals/{issn}/works` avec des filtres temporels. Ajouter obligatoirement un header `mailto` pour la Polite Pool. Analyser rigoureusement les headers de réponse HTTP `X-Rate-Limit-Limit` et `X-Rate-Limit-Interval`. Implémenter un délai d'attente (sleep) si la limite est approchée. Sauvegarder dans `data/raw/crossref_dump.json`.
> 
> Tests : Exécuter un appel HTTP simulé (mock) avec des en-têtes de limitation et vérifier le backoff temporel.

**Prompt 9 — Intégration de l'API HAL (Archives ouvertes)**

> Contexte : Moissonnage des thèses et articles francophones.
> 
> Objectif : Créer `scripts/ingest/ingest_hal.py`.
> 
> Contraintes : Utiliser l'API de recherche Apache Solr de HAL (`api.archives-ouvertes.fr/search/`). Construire dynamiquement la requête avec les paramètres `q=keyword_s:(...)` en utilisant les termes de `config/keywords.yaml` et `fq=docType_s:(ART OR THESE)`. Extraire les résultats formatés en JSON et les conformer à la structure Pydantic attendue pour stockage brut.
> 
> Fichiers : `scripts/ingest/ingest_hal.py`.
> 
> Tests : Lancer le script avec une limite fixée à 5 résultats et vérifier le format de sortie `hal_dump.json`.

**Prompt 10 — Intégration de Calenda / OpenEdition**

> Contexte : Captation des appels à contributions académiques en sciences sociales.
> 
> Objectif : Créer `scripts/ingest/ingest_openedition.py`.
> 
> Contraintes : Pour Calenda, utiliser le générateur REST (`calenda.org/api/generateur.php`) pour générer les requêtes basées sur le dictionnaire "radio". Récupérer les items XML/RSS. Associer `source_type` à `cfp` (Call for Papers).
> 
> Tests : Vérifier que le formatage identifie correctement le champ des dates limites de soumission si disponibles.

**Prompt 11 — Intégration de CiNii OpenSearch (Japon)**

> Contexte : Recherche des travaux japonais sur la radio libre. Cette API requiert un jeton (appid).
> 
> Objectif : Créer `scripts/ingest/ingest_cinii.py`.
> 
> Contraintes : Le script doit impérativement lire une variable d'environnement `CINII_APPID`. L'URL d'appel (`ci.nii.ac.jp/opensearch/fulltext`) doit recevoir le jeton et la requête `q=`. Exiger le format `format=jsonld`. Veiller méticuleusement à ce que l'encodage de la requête URL et de l'enregistrement JSON cible respecte l'UTF-8 pour les termes japonais.
> 
> Tests : Lancer le script avec un `appid` fictif, capturer l'erreur HTTP 403/400 et vérifier qu'elle est loguée correctement.

**Prompt 12 — Intégration de NDL Search (National Diet Library)**

> Contexte : Recherche de monographies et d'archives japonaises.
> 
> Objectif : Créer `scripts/ingest/ingest_ndl.py`.
> 
> Contraintes : Interroger l'API SRU ou OpenSearch de NDL Search. Analyser le XML retourné. Obligation absolue : ajouter la mention "Métadonnées extraites de NDL Search" dans le champ `rights` pour chaque objet Pydantic généré, afin de respecter les conditions de licence publiques.
> 
> Tests : Valider la présence de la chaîne d'attribution `rights` dans l'objet de test résultant.

**Prompt 13 — Intégration de J-STAGE WebAPI**

> Contexte : Captation sécurisée des métadonnées des revues scientifiques japonaises.
> 
> Objectif : Créer `scripts/ingest/ingest_jstage.py`.
> 
> Contraintes : Interdiction stricte de faire du scraping de DOM. Utiliser exclusivement les appels autorisés par la J-STAGE WebAPI pour la recherche bibliographique. Analyser le résultat au format XML (similaire à JATS) et l'insérer dans l'objet de veille brut. Mettre en place un traitement respectueux des limites serveur.
> 
> Tests : Valider l'exécution locale, vérifier `git status --short`.

**Prompt 14 — Exportation CSL-JSON pour Zotero**

> Contexte : Facilitation du processus d'intégration bibliographique par lot.
> 
> Objectif : Créer `scripts/export/export_csl.py`.
> 
> Contraintes : Parcourir `db.json` pour isoler les items avec un score de pertinence validé (`to_read` ou `saved_to_zotero`). Mapper les champs de `models.py` vers la spécification standard CSL-JSON (type, title, author, issued, DOI, URL). Enregistrer le fichier final dans `data/public/zotero_export.csljson`.
> 
> Tests : Vérifier la conformité du schéma CSL-JSON généré par rapport aux standards.

**Prompt 15 — Ordonnancement par un Pipeline Maître**

> Contexte : Consolidation de la chaîne exécutive Python.
> 
> Objectif : Créer `scripts/pipeline.py`.
> 
> Contraintes : Ce script doit orchestrer de manière séquentielle tous les modules créés. 1. Lancer les modules `ingest_*` dans des blocs `try/except` (un échec ne doit pas stopper le pipeline). 2. Lancer `normalize.py`. 3. Lancer `scoring.py`. 4. Lancer `export_obsidian.py` et `export_csl.py`. 5. Logger les temps d'exécution et le nombre d'entrées traitées dans `data/logs/pipeline.log`.
> 
> Fichiers : `scripts/pipeline.py`.
> 
> Tests : Lancer `python scripts/pipeline.py` et vérifier le fichier de log.

**Prompt 16 — Ségrégation Légale des Données Publiques (Hugo)**

> Contexte : Préparation des données pour publication web en respectant le copyright.
> 
> Objectif : Créer `scripts/export/export_hugo.py`.
> 
> Contraintes : Lire `db.json`. Filtrer uniquement les éléments jugés intéressants pour le public (ex: statut personnalisé ou score élevé). Règle absolue : effacer (mettre à null) le champ `abstract` pour purger la donnée des violations possibles de copyright commercial. Exporter le fichier sécurisé vers `site/data/public_veille.json`.
> 
> Tests : Créer un test unitaire qui vérifie qu'aucun abstract ne "fuit" dans le fichier public.

**Prompt 17 — Création des Templates Web (Hugo Layouts)**

> Contexte : Interface graphique de l'antenne radiophonique sur le site statique.
> 
> Objectif : Créer la hiérarchie de templates Hugo dans le dossier `site/`.
> 
> Contraintes : Créer `site/layouts/veille/list.html` et un modèle pour afficher une source unique. Le modèle `list.html` doit itérer (`range`) sur le fichier `.Site.Data.public_veille`. Mettre en forme le HTML en affichant proprement le `title_original` (japonais) et la traduction. Ajouter les mentions légales issues du champ `rights` (ex: attribution NDL).
> 
> Tests : Initialiser un mini site Hugo pour vérifier que la compilation des layouts ne retourne pas d'erreur syntaxique.

**Prompt 18 — Création du Flux RSS Personnel (Syndication)**

> Contexte : L'antenne de veille doit également émettre publiquement.
> 
> Objectif : Créer le fichier `site/layouts/veille/rss.xml`.
> 
> Contraintes : Rédiger un template Hugo valide générant une structure XML RSS 2.0 ou Atom. Boucler sur les données de `public_veille.json` (limitées aux 50 dernières entrées basées sur `discovered_at`). Assurer que la balise `<link>` redirige vers le DOI ou l'URL de la source originelle.
> 
> Tests : Valider manuellement le rendu de la sortie XML. Vérifier `git status --short`.

**Prompt 19 — Automatisation Chronologique (GitHub Actions)**

> Contexte : Déploiement en "pilote automatique" (cron job).
> 
> Objectif : Créer le fichier YAML `.github/workflows/veille.yml`.
> 
> Contraintes : Définir un événement déclencheur `schedule: cron: '0 2 * * *'`. Instancier une machine virtuelle Ubuntu, installer Python 3.11, restaurer le cache PIP (via `actions/setup-python`), injecter le secret `CINII_APPID` depuis GitHub Secrets. Exécuter `python scripts/pipeline.py`. Configurer un _Git Auto-Commit_ pour enregistrer automatiquement les modifications du fichier `db.json` sur le dépôt maître.
> 
> Fichiers : `.github/workflows/veille.yml`.
> 
> Tests : Valider la structure syntaxique du YAML de GitHub Actions.

**Prompt 20 — Audit de Sécurité, Logs et Préparation v0.1**

> Contexte : Clôture architecturale de la version 0.1 publiable et audit.
> 
> Objectif : Créer `Makefile` et consolider les logs.
> 
> Contraintes : Créer un `Makefile` contenant les commandes rapides `make install`, `make test`, `make run`. Vérifier l'implémentation de la capture de toutes les requêtes fautives (`httpx.TimeoutException`, erreurs HTTP 40x/50x) pour qu'elles se déversent dans `data/logs/api.log` avec horodatage, garantissant qu'aucune faille silencieuse ne corrompe l'automatisation. Mettre à jour `README.md` avec les instructions d'installation locales.
> 
> Tests : Exécuter `make test`. Afficher un résumé des actions accomplies, l'état final via `git status`, et annoncer la validation de la version v0.1 du projet. Ne rien faire d'autre.
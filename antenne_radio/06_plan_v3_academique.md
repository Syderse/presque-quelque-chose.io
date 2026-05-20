# Antenne Radio v3 — Plan d'intégration académique robuste

```text
Note d'exécution :
- Les sources académiques restent enabled: false par défaut.
- Les runs live se font une source à la fois.
- Toute activation durable doit être précédée d'un audit légal, de tests mockés, d'un run live inspecté et d'un handoff documenté.
- Tous les chemins de l'antenne sont à résoudre depuis le dossier réel du module antenne_radio/. Ne jamais créer de doublon à la racine si un fichier équivalent existe déjà dans antenne_radio/.
```

## Contexte et enjeux académiques

L'intégration de sources académiques massives comme **OpenAlex, DOAJ, Persée, CAIRN** et le catalogue complet **OpenEdition OPML** constitue le chantier majeur de la v3.
Ces sources permettent d'étendre de façon spectaculaire la couverture scientifique de la veille, mais posent trois risques majeurs :
1. **L'inondation par faux positifs (le bruit technique)** : Des recherches sur "radio frequency", radiothérapie, astronomie radio (trous noirs), ou capteurs de télécommunication peuvent rapidement submerger la base de données.
2. **La redondance (doublons)** : Les mêmes publications sont fréquemment référencées en parallèle sur plusieurs plateformes (ex: HAL et OpenAlex, ou Persée et DOAJ).
3. **Le statut légal & éthique** : Chaque plateforme possède ses propres licences d'accès, limites d'utilisation de l'API, et politiques quant au stockage ou à la republication des résumés (abstracts).

### Principes directeurs de la v3 (Discipline Lightweight)
- **Désactivation par défaut (`enabled: false`)** : Aucun nouveau connecteur académique ne doit être activé par défaut en production tant que :
  - Son audit légal individuel n'est pas versé à `LEGAL_AUDIT.md` ;
  - Ses tests unitaires mockés complets ne sont pas validés ;
  - Un run live isolé sur échantillon n'a pas été inspecté manuellement.
- **Volume et politesse d'API (Polite Pool)** : Implémenter systématiquement des limites strictes de résultats par requête (max 30 ou 50 items) et insérer les contacts requis (`mailto`) dans le pool de politesse.
- **Ciblage conceptuel strict** : Utiliser les classifications thématiques fines (subfields OpenAlex, keywords ciblés, listes manuelles de revues) dès l'appel réseau plutôt que de moissonner largement.
- **Dédoublonnage non destructeur** : Fusionner intelligemment les métadonnées sans altérer l'identifiant unique stable créé initialement.
- **Qualification active à l'ingestion (Gate)** : Rejeter directement de la base les articles académiques hors-sujet ou de pertinence faible (score < 2 ou < 3) dès l'ingestion pour éviter de polluer `db.json`.

---

## Architecture des connecteurs académiques

```
antenne_radio/scripts/ingest/ingest_openalex.py   ← Connecteur API REST OpenAlex (Polite Pool, Subfields)
antenne_radio/scripts/ingest/ingest_doaj.py       ← Connecteur API REST DOAJ (Keywords stricts)
antenne_radio/scripts/ingest/ingest_persee.py     ← Moissonneur OAI-PMH Persée (Parsing XML natif)
antenne_radio/scripts/ingest/ingest_opml.py       ← Parseur OPML OpenEdition (Parsing XML natif, revues choisies)
```
> [!IMPORTANT]
> Pour respecter la discipline *lightweight* et l'éco-conception d'AGENTS.md, **aucun parser XML ou HTML tiers ne doit être installé**. Tous les moissonneurs (Persée OAI-PMH, OpenEdition OPML) doivent utiliser exclusivement le module natif Python `xml.etree.ElementTree`.

---

## Séquence de 6 prompts pour la v3 académique

---

### Prompt 1 — Audit légal des sources universitaires (DOAJ, OpenEdition, CAIRN, Persée)

**Périmètre :** Documentation éthique et juridique (`antenne_radio/LEGAL_AUDIT.md` et `antenne_radio/01_RESSOURCES_SUIVIES.md`).

```text
Objectif : Auditer la conformité juridique, les licences de métadonnées et les conditions d'indexation des grandes sources académiques avant tout développement technique.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repère les chemins réels des fichiers avant d’en créer de nouveaux ;
- ne lance aucune ingestion live non demandée ;
- ne crée aucun cron ;
- ne crée aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores ou chemins locaux.
- Tous les chemins de l'antenne sont à résoudre depuis le dossier réel du module antenne_radio/. Ne jamais créer de doublon à la racine si un fichier équivalent existe déjà dans antenne_radio/.

Tâches :
1. Analyser et documenter les règles de réutilisation des métadonnées pour :
   - **DOAJ** : Politique de réutilisation (libre/CC0), conditions d'appel de l'API Search.
   - **OpenEdition** : Droit d'indexation des flux du catalogue, attribution et citation des revues.
   - **CAIRN** : Limitations de moissonnage, droit d'indexer les titres et métadonnées minimales de revues sans abstract.
   - **Persée** : Politique de moissonnage OAI-PMH, licences des métadonnées (Dublin Core) et obligations légales de citation.
2. Définir les contraintes éthiques et techniques obligatoires :
   - Interdiction formelle de stocker ou de publier les abstracts/résumés pour CAIRN et Persée (sauf accord explicite ou licence ouverte documentée).
   - Obligation d'identifier poliment l'agent utilisateur du projet (User-Agent explicite avec adresse mail de contact).
3. Consigner les verdicts, contraintes d'usage et URLs officielles consultées dans `antenne_radio/LEGAL_AUDIT.md`.
4. Mettre à jour `antenne_radio/01_RESSOURCES_SUIVIES.md` en miroir pour marquer ces sources comme auditées et en attente d'implémentation.

Vérification : Le fichier `antenne_radio/LEGAL_AUDIT.md` est enrichi avec un verdict précis et des conditions techniques strictes pour chaque source académique. Aucun code de connecteur n'est encore produit.

Ajoute un bref handoff dans antenne_radio/codex_memoire_materielle.md :
- fichiers modifiés ;
- commandes lancées ;
- résultats réels ;
- limites restantes ;
- prochaine étape recommandée.
```

---

### Prompt 2 — Ingestion OpenAlex ciblée et polie

**Périmètre :** Nouveau script d'ingestion (`antenne_radio/scripts/ingest/ingest_openalex.py`), configuration (`antenne_radio/config/sources.yaml`) et tests.

```text
Objectif : Créer le connecteur API REST OpenAlex en appliquant un ciblage conceptuel rigoureux et un mécanisme de Polite Pool.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repère les chemins réels des fichiers avant d’en créer de nouveaux ;
- ne lance aucune ingestion live non demandée ;
- ne crée aucun cron ;
- ne crée aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores ou chemins locaux.
- Tous les chemins de l'antenne sont à résoudre depuis le dossier réel du module antenne_radio/. Ne jamais créer de doublon à la racine si un fichier équivalent existe déjà dans antenne_radio/.

Tâches :
1. Créer le script `antenne_radio/scripts/ingest/ingest_openalex.py` interrogeant l'API OpenAlex (`https://api.openalex.org/works`) :
   - **Ciblage Conceptuel Strict** : Filtrer impérativement dès la requête HTTP par subfield thématique fin, en utilisant `primary_topic.subfield.id:1710` (Communication Studies) pour écarter à la racine le bruit des sciences dures (télécoms, médecine).
   - **Polite Pool** : Extraire une adresse email de contact depuis la configuration ou une variable d'environnement locale (`OPENALEX_MAILTO`) et l'injecter systématiquement en paramètre `mailto=` dans chaque requête.
   - **Fenêtre Temporelle & Volumes** : Limiter la recherche aux publications des 18 derniers mois (540 jours). Par défaut, requêter uniquement les 30 derniers jours pour la veille courante, et n'activer la récupération historique (bootstrap sur 18 mois) que via une option `--bootstrap`. Imposer un plafond de sécurité matériel (hard limit) à **50 items maximum** récupérés par exécution.
2. Écrire le dump brut dans `antenne_radio/data/raw/openalex_latest.json`.
3. Déclarer la source `openalex` dans `antenne_radio/config/sources.yaml` avec le statut obligatoire **`enabled: false`** par défaut.
4. Écrire des tests unitaires mockés rigoureux dans `antenne_radio/tests/test_ingest_openalex.py` (simulant l'API OpenAlex et testant la présence du contact email, des subfields de filtrage et du plafond de volume).
5. Lancer `make test`.

Vérification : `make test` passe avec succès. Le script interroge de façon isolée et polie l'API d'OpenAlex et respecte le cloisonnement.

Ajoute un bref handoff dans antenne_radio/codex_memoire_materielle.md :
- fichiers modifiés ;
- commandes lancées ;
- résultats réels ;
- limites restantes ;
- prochaine étape recommandée.
```

---

### Prompt 3 — Ingestion DOAJ (REST) et Persée (OAI-PMH avec parsing XML natif)

**Périmètre :** Ingestors dédiés (`antenne_radio/scripts/ingest/ingest_doaj.py` et `antenne_radio/scripts/ingest/ingest_persee.py`), configuration (`antenne_radio/config/sources.yaml`) et tests.

```text
Objectif : Développer les connecteurs API DOAJ et moissonneur OAI-PMH Persée en respectant les dates de publication réelles et en utilisant exclusivement le parser XML natif.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repère les chemins réels des fichiers avant d’en créer de nouveaux ;
- ne lance aucune ingestion live non demandée ;
- ne crée aucun cron ;
- ne crée aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores ou chemins locaux.
- Tous les chemins de l'antenne sont à résoudre depuis le dossier réel du module antenne_radio/. Ne jamais créer de doublon à la racine si un fichier équivalent existe déjà dans antenne_radio/.

Tâches :
1. **Ingestor DOAJ** :
   - Créer `antenne_radio/scripts/ingest/ingest_doaj.py` interrogeant l'API Search de DOAJ (`https://doaj.org/api/v4/search/articles/`).
   - Construire une requête stricte ciblant les études de média ou de radio (`(radio OR podcast OR broadcasting)`).
   - Appliquer la fenêtre temporelle de 18 mois et un hard limit de **30 items max** par run.
2. **Ingestor Persée** :
   - Créer `antenne_radio/scripts/ingest/ingest_persee.py` utilisant le protocole moissonneur OAI-PMH (`https://www.persee.fr/oai`).
   - Effectuer un moissonnage ciblé au format Dublin Core (`metadataPrefix=oai_dc`) avec mots-clés (`radio OR podcast`) dans le titre ou les sujets.
   - **Garde-fou Éco-conception** : Parser le XML Dublin Core renvoyé par l'OAI-PMH en utilisant exclusivement le module natif de Python `xml.etree.ElementTree` (aucune bibliothèque tierce de type lxml ou BeautifulSoup).
   - **Contrainte de date Persée** : Distinguer impérativement la date de publication originale de l'article de la date de mise à jour du record OAI-PMH. La fenêtre de filtrage de 18 mois doit être appliquée à la **date de publication réelle**, afin d'éviter d'ingérer de vieux articles ré-indexés récemment.
3. Écrire les dumps bruts dans `antenne_radio/data/raw/doaj_latest.json` et `antenne_radio/data/raw/persee_latest.json`.
4. Déclarer les sources `doaj` et `persee` dans `antenne_radio/config/sources.yaml` avec le statut obligatoire **`enabled: false`** par défaut.
5. Écrire des tests unitaires mockés complets dans `antenne_radio/tests/test_ingest_doaj.py` et `antenne_radio/tests/test_ingest_persee.py` validant les filtres, le respect des dates et la récupération sans réseau.
6. Lancer `make test`.

Vérification : Les deux scripts ingèrent isolément les flux sans réseau via mocks, et `make test` passe à 100%.

Ajoute un bref handoff dans antenne_radio/codex_memoire_materielle.md :
- fichiers modifiés ;
- commandes lancées ;
- résultats réels ;
- limites restantes ;
- prochaine étape recommandée.
```

---

### Prompt 4 — Ingestion CAIRN et catalogue OpenEdition OPML (revues sélectionnées)

**Périmètre :** Ingestor de fichiers de catalogue OPML (`antenne_radio/scripts/ingest/ingest_opml.py`), configuration (`antenne_radio/config/sources.yaml`) et normalisation.

```text
Objectif : Intégrer les revues francophones choisies sur CAIRN et extraire sélectivement les flux du catalogue OPML d'OpenEdition en utilisant exclusivement le parser XML natif.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repère les chemins réels des fichiers avant d’en créer de nouveaux ;
- ne lance aucune ingestion live non demandée ;
- ne crée aucun cron ;
- ne crée aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores ou chemins locaux.
- Tous les chemins de l'antenne sont à résoudre depuis le dossier réel du module antenne_radio/. Ne jamais créer de doublon à la racine si un fichier équivalent existe déjà dans antenne_radio/.

Tâches :
1. **Éviter le moissonnage massif indifférencié** :
   - Établir une liste manuelle et ciblée de revues en sciences de la communication et études sonores (ex: *Radiomorphoses*, *Volume!*, *Biens symboliques*, *Réseaux*, *Questions de communication*).
   - Pour CAIRN, intégrer les flux RSS stables correspondant uniquement à ces revues choisies.
2. **Parseur OpenEdition OPML** :
   - Créer le script `antenne_radio/scripts/ingest/ingest_opml.py` (ou étendre l'ingestion RSS) pour lire localement ou moissonner le fichier OPML d'OpenEdition.
   - **Garde-fou Éco-conception** : Parser le fichier OPML (structure XML) en utilisant uniquement le module natif Python `xml.etree.ElementTree`.
   - Filtrer et extraire uniquement les flux RSS des revues validées correspondant aux thématiques son/médias/communication.
3. S'assurer que tous les items issus de ces flux reçoivent la catégorie publique `source_category: académique` lors de l'attribution et sont normalisés proprement avec `kind: rss`.
4. Intégrer l'appel au parseur OPML dans la logique globale et déclarer les sources correspondantes dans `antenne_radio/config/sources.yaml` avec le statut **`enabled: false`** par défaut.
5. Écrire des cas de test unitaire mockant le fichier OPML et s'assurant du filtrage strict des revues.
6. Lancer `make test`.

Vérification : Le parseur OPML extrait uniquement les revues thématiques et les items sont correctement typés sous la catégorie `académique`. `make test` passe.

Ajoute un bref handoff dans antenne_radio/codex_memoire_materielle.md :
- fichiers modifiés ;
- commandes lancées ;
- résultats réels ;
- limites restantes ;
- prochaine étape recommandée.
```

---

### Prompt 5 — Scoring renforcé, Qualification Active et Dédoublonnage inter-sources

**Périmètre :** Configuration de scoring (`antenne_radio/config/keywords.yaml`, `antenne_radio/config/scoring.yaml`), scripts de normalisation (`antenne_radio/scripts/core/normalize.py`) et tests associés.

```text
Objectif : Protéger la base de données de l'inondation en durcissant le filtrage du bruit technique, en appliquant une qualification active à la volée et en mettant en œuvre un dédoublonnage académique robuste.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repère les chemins réels des fichiers avant d’en créer de nouveaux ;
- ne lance aucune ingestion live non demandée ;
- ne crée aucun cron ;
- ne crée aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores ou chemins locaux.
- Tous les chemins de l'antenne sont à résoudre depuis le dossier réel du module antenne_radio/. Ne jamais créer de doublon à la racine si un fichier équivalent existe déjà dans antenne_radio/.

Tâches :
1. **Pénalisation du bruit technique SHS/Dures** :
   - Ajuster les listes de mots-clés négatifs dans `antenne_radio/config/keywords.yaml` en ajoutant des termes de bruit très stricts pour les sciences dures (ex: `radiography`, `radiotherapy`, `irradiation`, `radioactive`, `radio telescope`, `radio emission`, `electromagnetic radiation`, `spectrum sensing`, `cognitive radio`, `SDR`, `5G`, `6G`, `mimo`, `beamforming`).
   - Assurer des pénalités dissuasives dans `antenne_radio/config/scoring.yaml` pour ces catégories (`negative_noise: -10`, `technical_radio_noise: -4`).
2. **Qualification Active (Gate d'ingestion)** :
   - Afin d'éviter de stocker des milliers de notices académiques non pertinentes dans `antenne_radio/data/normalized/db.json`, implémenter un filtre de qualification à la volée dans `antenne_radio/scripts/core/normalize.py` (ou `scoring.py`).
   - Si un item issu d'une source académique (OpenAlex, DOAJ, Persée, Cairn) obtient un score de pertinence initial insuffisant (< 2 ou < 3) ou ne contient aucun mot-clé de `radio_core` ou `podcast`, il doit être **immédiatement rejeté** de l'ingestion et ne jamais être écrit en base de données.
3. **Dédoublonnage inter-sources robuste** :
   - Mettre en place un système de déduplication strict dans `antenne_radio/scripts/core/normalize.py` :
     - **Par DOI normalisé** : Comparer les DOIs nettoyés (retrait du préfixe `https://doi.org/`, mise en minuscules).
     - **Par Titre normalisé** (si DOI absent) : Nettoyer ponctuation, espaces multiples et casse pour repérer les doublons.
     - **Fusion des métadonnées** : En cas de doublon, fusionner les données (conserver les tags, préférer le lien de dépôt HAL s'il offre le texte intégral, ou OpenAlex pour des métadonnées plus riches).
     - **Préservation de l'ID stable** : Conserver obligatoirement l'identifiant unique stable créé lors de l'ingestion initiale pour ne jamais casser l'indexation externe ou les favoris de l'utilisateur.
4. Écrire des cas de tests unitaires complets validant le filtrage du bruit à la volée, le rejet d'articles non pertinents et la fusion de notices doublonnées.
5. Lancer `make test`.

Vérification : `make test` passe avec succès. Les items académiques bruyants sont rejetés avant écriture, et la fusion de doublons HAL/OpenAlex préserve l'ID stable d'origine.

Ajoute un bref handoff dans antenne_radio/codex_memoire_materielle.md :
- fichiers modifiés ;
- commandes lancées ;
- résultats réels ;
- limites restantes ;
- prochaine étape recommandée.
```

---

### Prompt 6 — Ingestion globale, tests unitaires, validation & handoff final v3

**Périmètre :** Intégration dans le pipeline (`antenne_radio/scripts/pipeline.py`), exécution complète, recette et documentation.

```text
Objectif : Orchestrer l'ensemble des connecteurs académiques dans le pipeline global, exécuter une recette complète, et documenter l'état final.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repère les chemins réels des fichiers avant d’en créer de nouveaux ;
- ne lance aucune ingestion live non demandée ;
- ne crée aucun cron ;
- ne crée aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores ou chemins locaux.
- Tous les chemins de l'antenne sont à résoudre depuis le dossier réel du module antenne_radio/. Ne jamais créer de doublon à la racine si un fichier équivalent existe déjà dans antenne_radio/.

Tâches :
1. Intégrer tous les nouveaux ingestors académiques (OpenAlex, DOAJ, Persée, Cairn/OPML) dans le script d'orchestration global `antenne_radio/scripts/pipeline.py` en ajoutant des options CLI explicites pour les ignorer au besoin (ex: `--skip-openalex`, `--skip-doaj`, etc.).
2. Configurer une adresse email réelle dans l'environnement local pour la politesse des requêtes.
3. **Règle stricte d'activation temporaire pour test** : Ne pas laisser les sources académiques activées par défaut après le test. Pour chaque run live isolé, activer temporairement une seule source à la fois dans `antenne_radio/config/sources.yaml` (`enabled: true`), exécuter le run ultra-limité, inspecter minutieusement l'échantillon, puis remettre immédiatement `enabled: false` sauf validation explicite documentée.
4. Lancer le pipeline global via `make run` pour tester l'intégration technique de bout en bout de toutes les sources de manière unitaire et contrôlée.
5. Générer le JSON public via `make export-public`.
6. Lancer un build de validation Hugo complet.
7. **Scans anti-fuite exhaustifs** : Vérifier que le JSON `static/antenne-radio/index.json` et les pages publiques générées respectent rigoureusement la whitelist stricte de la v2. Aucun abstract académique (DOAJ, Persée, etc.) ou score ne doit fuiter.
8. Mettre à jour la documentation d'architecture et les mémoires :
   - `antenne_radio/README.md` (connecteurs académiques v3 et commandes).
   - `antenne_radio/01_RESSOURCES_SUIVIES.md` (statuts finaux v3).
   - `antenne_radio/LEGAL_AUDIT.md` (verdicts universitaires complétés).
   - `docs/CHANTIERS.md` (marquer la v3 comme terminée).
9. Mettre à jour `antenne_radio/codex_memoire_materielle.md` avec le bilan d'intégration complet, les compteurs de notices académiques ajoutées, et les statistiques de rejet.

Vérification : Le pipeline s'exécute avec succès, les tests passent à 100%, et aucune fuite de données privées n'est présente dans les fichiers publics. La v3 académique est close et validée localement.

Ajoute un bref handoff dans antenne_radio/codex_memoire_materielle.md :
- fichiers modifiés ;
- commandes lancées ;
- résultats réels ;
- limites restantes ;
- prochaine étape recommandée.
```

---

## Résumé des fichiers concernés par prompt (v3)

| Prompt | Fichiers principaux impactés |
|---:|---|
| 1 | `antenne_radio/LEGAL_AUDIT.md`, `antenne_radio/01_RESSOURCES_SUIVIES.md` |
| 2 | `antenne_radio/scripts/ingest/ingest_openalex.py`, `antenne_radio/tests/test_ingest_openalex.py`, `antenne_radio/config/sources.yaml` |
| 3 | `antenne_radio/scripts/ingest/ingest_doaj.py`, `antenne_radio/scripts/ingest/ingest_persee.py`, `antenne_radio/tests/test_ingest_doaj.py`, `antenne_radio/tests/test_ingest_persee.py`, `antenne_radio/config/sources.yaml` |
| 4 | `antenne_radio/scripts/ingest/ingest_opml.py`, `antenne_radio/tests/test_ingest_opml.py`, `antenne_radio/config/sources.yaml` |
| 5 | `antenne_radio/config/keywords.yaml`, `antenne_radio/config/scoring.yaml`, `antenne_radio/scripts/core/normalize.py`, `antenne_radio/tests/test_normalize.py`, `antenne_radio/tests/test_scoring.py` |
| 6 | `antenne_radio/scripts/pipeline.py`, `antenne_radio/tests/test_pipeline.py`, `antenne_radio/README.md`, `antenne_radio/01_RESSOURCES_SUIVIES.md`, `antenne_radio/LEGAL_AUDIT.md`, `docs/CHANTIERS.md`, `antenne_radio/codex_memoire_materielle.md` |

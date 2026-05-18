Oui, cette division est exactement la bonne. Je reformulerais le projet ainsi : **v0.1 = une antenne privée, locale, testée, bêtement fiable** ; les intégrations plus ambitieuses deviennent des “cartouches” ajoutables une par une.

Ton document original proposait déjà cette logique : une architecture en couches, fichiers plats, ingestion, normalisation, scoring, exports privés/publics, puis automatisation ; il mentionnait aussi que la v0.1 pouvait se limiter à “RSS + HAL”, validation Pydantic, dédoublonnage et rapport Markdown. Je te propose donc de **retirer encore davantage** pour arriver à une vraie première base stable.

## Principe de la v0.1

La v0.1 ne doit pas être “l’antenne complète”. Elle doit être :

**Un pipeline local qui lit quelques flux RSS/Atom + HAL, normalise les résultats dans un `db.json`, applique un scoring simple, et génère un rapport Markdown pour Obsidian.**

Pourquoi ce périmètre est bon : `feedparser` est fait pour parser RSS et Atom en Python, y compris RSS 2.0 et Atom 1.0 ; HAL expose une API de recherche avec sorties JSON, Atom, BibTeX, RSS, etc. ; Pydantic permet de définir des modèles et de générer des schémas JSON ; pytest fournit `tmp_path`, très pratique pour tester des scripts qui lisent/écrivent des fichiers sans toucher aux vraies données. ([Feedparser](https://feedparser.readthedocs.io/en/stable/introduction.html?utm_source=chatgpt.com "Introduction — feedparser 6.0.12 documentation"))

## Ce qu’on garde pour v0.1

À garder :

|Élément|Pourquoi|
|---|---|
|`config/sources.yaml`|Modifier les sources sans toucher au code.|
|`config/keywords.yaml`|Faire évoluer ton champ de veille facilement.|
|`config/scoring.yaml`|Garder le scoring explicable.|
|RSS/Atom via `feedparser`|Simple, robuste, peu risqué.|
|HAL|Première vraie API académique, mais stable et documentée.|
|`RadioWatchItem` Pydantic|Schéma pivot dès le début.|
|`data/raw/`|Garder les données brutes pour déboguer.|
|`data/normalized/db.json`|Base unique, lisible, versionnable.|
|`export_obsidian.py`|Sortie immédiatement utile pour ton travail.|
|tests unitaires|Pas de système fragile qui “marche une fois”.|
|`Makefile`|`make test`, `make run`, `make clean-data` si besoin.|
|workflow GitHub Actions manuel|Seulement `workflow_dispatch`, pas encore de cron automatique.|

GitHub Actions peut être déclenché manuellement avec `workflow_dispatch`, et les workflows planifiés utilisent aussi un événement `schedule` en syntaxe cron ; mais pour v0.1, je garderais le déclenchement manuel, parce que l’auto-commit quotidien est un risque inutile au début. ([GitHub Docs](https://docs.github.com/actions/using-workflows/events-that-trigger-workflows?utm_source=chatgpt.com "Events that trigger workflows"))

## Ce qu’on exclut explicitement de v0.1

À reporter :

|Élément|Version cible|
|---|---|
|CiNii, NDL, J-STAGE|v0.3|
|Crossref / OpenAlex|v0.2|
|Zotero CSL-JSON|v0.2 ou v0.3|
|Hugo public|v0.2/v0.3|
|Flux RSS sortant public|v0.3|
|changedetection.io|v0.3|
|auto-commit GitHub Actions|v0.2 seulement après tests|
|LLM/résumés automatiques|beaucoup plus tard|
|scraping de pages|à éviter par défaut|

Hugo reste une très bonne cible ultérieure parce qu’il peut lire des sources locales ou distantes en JSON, YAML, TOML, XML ou CSV, mais ce n’est pas nécessaire pour la première base agrégative. ([Hugo](https://gohugo.io/content-management/data-sources/?utm_source=chatgpt.com "Data sources"))

# Objectifs v0.1

## Objectif 0 — Créer le dépôt minimal

Résultat attendu : une arborescence simple, sans logique métier prématurée.

```text
radio-watch/
├── README.md
├── Makefile
├── requirements.txt
├── config/
│   ├── sources.yaml
│   ├── keywords.yaml
│   └── scoring.yaml
├── scripts/
│   ├── core/
│   │   ├── models.py
│   │   ├── normalize.py
│   │   ├── scoring.py
│   │   └── io.py
│   ├── ingest/
│   │   ├── ingest_rss.py
│   │   └── ingest_hal.py
│   ├── export/
│   │   └── export_obsidian.py
│   └── pipeline.py
├── data/
│   ├── raw/
│   ├── normalized/
│   ├── exports/
│   └── logs/
└── tests/
```

Pas de `site/`, pas de `scripts/ingest_cinii.py`, pas de `export_hugo.py`, pas de `export_csl.py`.

## Objectif 1 — Définir un schéma pivot sobre

Pour v0.1, je ferais ce modèle :

```text
id
title
title_original
authors
source_name
source_type
language
published_at
discovered_at
url
doi
abstract
tags
keywords_matched
negative_keywords_matched
relevance_score
score_explanation
status
source_feed
source_api
raw
```

Statuts v0.1 :

```text
new
candidate
to_read
ignored
exported
```

Je préfère `candidate` à un passage direct `new → ignored`, parce que ton domaine est trop subtil : un texte peut être intéressant sans contenir les bons mots-clés.

## Objectif 2 — Lire des flux RSS/Atom

Le premier connecteur doit faire peu de choses :

1. Lire `sources.yaml`.
    
2. Prendre les sources `type: rss`.
    
3. Parser avec `feedparser`.
    
4. Sauvegarder un dump brut dans `data/raw/rss_<timestamp>.json`.
    
5. Ne pas encore décider de la pertinence.
    

Important : **l’ingestion ne doit pas scorer**. Elle capte seulement.

## Objectif 3 — Ajouter HAL comme première API académique

HAL est le seul connecteur non-RSS que je mettrais dans la v0.1. Il permet de chercher dans une API Solr avec des filtres et plusieurs formats de sortie, dont JSON, RSS, Atom et BibTeX. ([API HAL](https://api.archives-ouvertes.fr/docs/search?utm_source=chatgpt.com "API HAL API de recherche HAL"))

Pour v0.1, ne fais pas une requête trop intelligente. Fais simple :

- mots-clés français/anglais ;
    
- types : articles, thèses, communications éventuellement ;
    
- limite basse, par exemple 20 résultats ;
    
- sortie JSON ;
    
- dump brut séparé dans `data/raw/hal_<timestamp>.json`.
    

## Objectif 4 — Normaliser sans perdre le brut

Le normaliseur transforme les dumps en `RadioWatchItem`.

Règles :

- si DOI : `id = sha256("doi:" + doi_normalized)` ;
    
- sinon si URL : `id = sha256("url:" + canonical_url)` ;
    
- sinon : `id = sha256("fallback:" + title + published_at + source_name)` ;
    
- ne jamais écraser un item existant sans raison ;
    
- conserver `raw` pour vérifier les erreurs.
    

## Objectif 5 — Dédupliquer prudemment

En v0.1, pas de fuzzy matching automatique destructeur.

Règle simple :

- même `id` : doublon, on ignore ;
    
- titre très proche : on ne supprime pas, on ajoute éventuellement `possible_duplicate: true` plus tard ;
    
- tout ce qui est ambigu reste dans la base.
    

## Objectif 6 — Scorer de manière lisible

Le scoring doit produire une explication, pas juste un nombre.

Exemple :

```text
+4 radio libre dans title
+3 podcast dans abstract
+5 Guattari dans abstract
-6 radiologie dans title
```

Statuts :

```text
score >= 6 → to_read
score entre 2 et 5 → candidate
score < 2 → ignored
```

Je garderais les `ignored` dans `db.json`, au moins au début, pour voir ce que le système rejette.

## Objectif 7 — Exporter vers Obsidian

La sortie v0.1 doit être un fichier Markdown :

```text
data/exports/veille-2026-W21.md
```

Structure :

```markdown
---
type: veille-radio
week: 2026-W21
generated_at: ...
items_count: ...
---

# Veille radio — 2026-W21

## À lire

### Titre
- Source :
- Auteur(s) :
- Date :
- URL :
- Score :
- Pourquoi retenu :
- Résumé/abstract :
```

Pour v0.1, je ne changerais pas automatiquement le statut en `exported`, ou alors seulement avec une option `--mark-exported`. Sinon tu risques de perdre de vue des items.

## Objectif 8 — Pipeline local

Un seul script :

```text
python scripts/pipeline.py
```

Il exécute :

```text
ingest_rss
ingest_hal
normalize
score
export_obsidian
```

Chaque étape doit être dans un `try/except`, avec log. Si HAL échoue, le RSS doit continuer. Si un flux RSS est mort, les autres doivent continuer.

## Objectif 9 — Tests et audit

Critères de réussite v0.1 :

```text
make install
make test
make run
```

Doivent fonctionner.

Et après `make run`, on doit avoir :

```text
data/raw/*.json
data/normalized/db.json
data/exports/veille-YYYY-WW.md
data/logs/pipeline.log
```

# Série de prompts Codex pour construire la v0.1

Je te conseille de les lancer **un par un**, dans cet ordre. Chaque prompt force Codex à ne pas faire trop, à tester, et à ne pas inventer des intégrations.

## Prompt 1 — Initialiser la structure v0.1

```text
Objectif : initialiser une v0.1 minimale et locale du projet radio-watch.

Contexte :
Je construis une antenne de veille en études radiophoniques. Cette v0.1 doit être volontairement simple : RSS/Atom + HAL + normalisation Pydantic + scoring + export Markdown Obsidian. Ne pas ajouter Crossref, OpenAlex, CiNii, NDL, J-STAGE, Zotero CSL, Hugo, changedetection.io, cron automatique ou LLM.

Tâches :
1. Inspecte l’état courant du dépôt avec `git status --short`.
2. Crée l’arborescence :
   - config/
   - scripts/core/
   - scripts/ingest/
   - scripts/export/
   - data/raw/
   - data/normalized/
   - data/exports/
   - data/logs/
   - tests/
3. Crée requirements.txt avec les dépendances minimales :
   - pydantic
   - httpx
   - feedparser
   - pyyaml
   - pytest
   - python-dateutil
4. Crée README.md avec :
   - but du projet ;
   - périmètre strict de v0.1 ;
   - hors-périmètre explicite ;
   - commandes prévues : make install, make test, make run.
5. Crée un Makefile minimal avec install, test, run, clean-data.
6. Ne crée aucun connecteur complexe à ce stade.

Contraintes :
- Pas de code réseau pour l’instant.
- Pas d’intégration japonaise.
- Pas d’auto-commit.
- Pas de Hugo.
- Ne pas remplacer des fichiers existants sans raison.

Tests :
- Lancer `python --version`.
- Lancer `git status --short`.
- Résumer les fichiers créés et les limites connues.
```

## Prompt 2 — Créer les fichiers de configuration

```text
Objectif : créer la configuration déclarative de la v0.1.

Contexte :
Le projet doit rester modifiable sans changer le code. Les sources, mots-clés et règles de scoring doivent vivre dans config/.

Tâches :
1. Inspecte le dépôt.
2. Crée config/sources.yaml avec deux familles :
   - sources RSS/Atom : quelques entrées d’exemple désactivables avec enabled: true/false ;
   - source HAL : une entrée `hal` avec enabled: true, limit: 20, et les paramètres nécessaires.
3. Crée config/keywords.yaml avec catégories :
   - radio_core
   - radio_free
   - sound_studies
   - podcast
   - guattari_institutional_psychotherapy
   - japan_later
   - negative_noise
4. Crée config/scoring.yaml avec :
   - poids par catégorie ;
   - seuils : to_read >= 6, candidate >= 2, ignored < 2 ;
   - champs à examiner : title, abstract, tags.
5. Ajoute des commentaires YAML utiles mais pas trop longs.

Contraintes :
- Ne code aucun connecteur.
- Inclure quelques mots-clés japonais dans `japan_later`, mais ne pas créer d’intégration japonaise.
- Inclure des mots-clés négatifs comme radiologie, radiofréquence, radioastronomie, wireless engineering.
- Prévoir un champ `enabled` pour désactiver une source sans l’effacer.

Tests :
- Écrire un mini test ou une commande Python qui charge les trois fichiers YAML et vérifie qu’ils sont valides.
- Lancer pytest si un test est créé.
- Terminer par git status et résumé.
```

## Prompt 3 — Créer le modèle Pydantic

```text
Objectif : définir le schéma pivot v0.1.

Contexte :
Toutes les sources doivent être normalisées vers un modèle unique RadioWatchItem. Le modèle doit rester sobre mais assez souple pour des articles, appels, billets, thèses, notices et ressources diverses.

Tâches :
1. Crée scripts/core/models.py.
2. Définis :
   - SourceType enum : journal_article, cfp, thesis, book, chapter, blog, archive, unknown.
   - WatchStatus enum : new, candidate, to_read, ignored, exported.
   - RadioWatchItem BaseModel.
3. Champs requis :
   - id
   - title
   - source_name
   - source_type
   - language
   - status
   - discovered_at
4. Champs optionnels :
   - title_original
   - authors
   - published_at
   - url
   - doi
   - abstract
   - tags
   - keywords_matched
   - negative_keywords_matched
   - relevance_score
   - score_explanation
   - source_feed
   - source_api
   - raw
5. Crée une fonction stable `generate_stable_id()` :
   - DOI prioritaire ;
   - URL ensuite ;
   - fallback titre + date + source.
6. Crée une fonction de normalisation simple du DOI et des URL.

Contraintes :
- Ne pas appeler le réseau.
- Ne pas écrire dans data/.
- Ne pas ajouter de logique de scoring ici.
- Le modèle doit être testable isolément.

Tests :
- Crée tests/test_models.py.
- Tester un item minimal valide.
- Tester la génération d’id par DOI.
- Tester la génération d’id par URL.
- Tester qu’un item sans title est rejeté.
- Lancer pytest.
- Terminer par git status et résumé.
```

## Prompt 4 — Ajouter les utilitaires d’entrée/sortie JSON

```text
Objectif : centraliser les lectures/écritures de fichiers JSON pour éviter les duplications.

Contexte :
Le projet va lire/écrire des dumps bruts, db.json et des exports. Il faut des fonctions robustes, testées, qui créent les dossiers si besoin et écrivent de manière stable.

Tâches :
1. Crée scripts/core/io.py.
2. Ajoute :
   - read_json(path, default)
   - write_json(path, data)
   - append_log(path, message, level="INFO")
   - utc_now_iso()
   - ensure_parent_dir(path)
3. write_json doit :
   - créer le dossier parent ;
   - écrire en UTF-8 ;
   - préserver les caractères japonais ;
   - indenter le JSON ;
   - trier les clés si pertinent.
4. Les fonctions doivent utiliser pathlib.

Contraintes :
- Pas de réseau.
- Pas de dépendance inutile.
- Pas de modification du schéma Pydantic sauf si absolument nécessaire.

Tests :
- Crée tests/test_io.py avec tmp_path.
- Vérifie qu’un fichier JSON est écrit puis relu.
- Vérifie que les caractères japonais ne sont pas échappés inutilement.
- Vérifie qu’un log est créé.
- Lancer pytest.
- Terminer par git status et résumé.
```

## Prompt 5 — Ingestion RSS/Atom minimale

```text
Objectif : créer le premier connecteur v0.1 : RSS/Atom.

Contexte :
Cette étape doit seulement capter les données. Elle ne doit pas scorer, ne doit pas normaliser définitivement, et ne doit pas écrire db.json. Elle produit un dump brut dans data/raw/.

Tâches :
1. Crée scripts/ingest/ingest_rss.py.
2. Lis config/sources.yaml.
3. Sélectionne uniquement les sources :
   - enabled: true
   - type: rss
4. Utilise feedparser pour parser chaque flux.
5. Pour chaque entrée, extraire autant que possible :
   - title
   - link
   - published
   - updated
   - authors
   - summary
   - source_name
   - source_feed
6. Sauvegarde le résultat brut dans data/raw/rss_latest.json.
7. Logue les erreurs dans data/logs/api.log sans interrompre tout le script.

Contraintes :
- Si un flux échoue, continuer avec les autres.
- Ne pas écrire data/normalized/db.json.
- Ne pas scorer.
- Ne pas faire de scraping HTML.
- Ajouter une option CLI `--config` et `--output` si simple.

Tests :
- Crée une fixture locale RSS ou Atom dans tests/fixtures/.
- Teste le parsing sans appel réseau.
- Teste qu’une entrée contient title/link/source_name.
- Lancer pytest.
- Terminer par git status et résumé des limites.
```

## Prompt 6 — Ingestion HAL minimale

```text
Objectif : ajouter le connecteur HAL v0.1.

Contexte :
HAL est la seule API académique non-RSS autorisée dans cette v0.1. Il faut rester simple : requête limitée, sortie JSON, dump brut. Pas de Crossref, pas d’OpenAlex.

Tâches :
1. Crée scripts/ingest/ingest_hal.py.
2. Lis config/sources.yaml et config/keywords.yaml.
3. Construis une requête HAL simple à partir de quelques mots-clés sélectionnés.
4. Limite les résultats à une valeur configurable, par défaut 20.
5. Demande une sortie JSON.
6. Sauvegarde dans data/raw/hal_latest.json.
7. Logue erreurs HTTP, timeouts et réponses inattendues dans data/logs/api.log.

Contraintes :
- Utiliser httpx avec timeout.
- Ne pas écrire db.json.
- Ne pas scorer.
- Ne pas ajouter Crossref/OpenAlex.
- Prévoir des fonctions séparées : build_query(), fetch_hal(), parse_response().
- Les tests ne doivent pas dépendre d’un vrai appel réseau.

Tests :
- Utiliser une fixture JSON HAL dans tests/fixtures/.
- Tester build_query().
- Tester parse_response() sur fixture.
- Tester qu’un timeout simulé est logué proprement si possible.
- Lancer pytest.
- Terminer par git status et résumé.
```

## Prompt 7 — Normalisation et dédoublonnage vers db.json

```text
Objectif : transformer les dumps bruts RSS/HAL en RadioWatchItem et alimenter db.json sans doublons.

Contexte :
Les connecteurs écrivent dans data/raw/. Cette étape lit rss_latest.json et hal_latest.json, transforme les entrées en RadioWatchItem, puis les ajoute à data/normalized/db.json.

Tâches :
1. Crée scripts/core/normalize.py.
2. Implémente :
   - normalize_rss_entry()
   - normalize_hal_entry()
   - load_existing_db()
   - merge_items_without_duplicates()
   - save_db()
3. Crée data/normalized/db.json si absent.
4. Ne pas écraser un item existant avec le même id.
5. Trier les items par discovered_at ou published_at de façon stable.
6. Conserver le champ raw.
7. Ajouter source_api = rss ou hal.

Contraintes :
- Pas de fuzzy matching destructeur.
- Pas de suppression automatique.
- Pas de scoring ici.
- Si une entrée est invalide, la loguer et continuer.

Tests :
- Crée tests/test_normalize.py.
- Tester normalisation RSS depuis fixture.
- Tester normalisation HAL depuis fixture.
- Tester que deux passages identiques ne créent pas de doublons.
- Tester qu’une entrée invalide ne casse pas tout.
- Lancer pytest.
- Terminer par git status et résumé.
```

## Prompt 8 — Scoring explicable

```text
Objectif : ajouter un scoring lexical simple, transparent et configurable.

Contexte :
Le scoring doit aider à trier, pas décider définitivement. Il doit expliquer pourquoi un item est retenu ou ignoré.

Tâches :
1. Crée scripts/core/scoring.py.
2. Lis data/normalized/db.json.
3. Lis config/keywords.yaml et config/scoring.yaml.
4. Pour chaque item dont status est new :
   - examiner title, abstract, tags ;
   - appliquer les poids positifs ;
   - appliquer les poids négatifs ;
   - remplir keywords_matched ;
   - remplir negative_keywords_matched ;
   - remplir relevance_score ;
   - remplir score_explanation.
5. Statuts :
   - score >= seuil to_read : to_read
   - score >= seuil candidate : candidate
   - sinon : ignored
6. Écrire db.json.

Contraintes :
- Ne pas modifier les items déjà exported.
- Ne pas supprimer les ignored.
- Regex insensible à la casse pour français/anglais.
- Gestion correcte UTF-8.
- Le scoring doit être déterministe.

Tests :
- Crée tests/test_scoring.py.
- Tester un item très pertinent.
- Tester un item bruité type radiologie.
- Tester un item candidate.
- Tester que score_explanation est non vide.
- Lancer pytest.
- Terminer par git status et résumé.
```

## Prompt 9 — Export Markdown Obsidian

```text
Objectif : générer un rapport Markdown hebdomadaire lisible dans Obsidian.

Contexte :
La sortie utile de v0.1 est un fichier Markdown dans data/exports/. Il doit lister les items to_read et candidate, avec les raisons du score.

Tâches :
1. Crée scripts/export/export_obsidian.py.
2. Lis data/normalized/db.json.
3. Génère data/exports/veille-YYYY-WW.md.
4. Inclure un frontmatter YAML :
   - type: veille-radio
   - generated_at
   - week
   - items_to_read
   - items_candidate
5. Structure :
   - À lire
   - Candidats
   - Ignorés intéressants éventuellement, seulement si option activée
6. Pour chaque item :
   - titre
   - auteurs
   - source
   - date
   - lien
   - score
   - explication
   - abstract si disponible
7. Ajouter une option `--mark-exported` qui passe seulement les to_read exportés en exported. Par défaut, ne pas changer les statuts.

Contraintes :
- Ne pas générer CSL-JSON.
- Ne pas écrire dans un vault Obsidian réel.
- Ne pas dépendre de Dataview.
- Markdown simple et robuste.

Tests :
- Crée tests/test_export_obsidian.py.
- Utiliser tmp_path.
- Vérifier que le fichier est créé.
- Vérifier qu’il contient les sections attendues.
- Vérifier que les caractères japonais restent lisibles.
- Lancer pytest.
- Terminer par git status et résumé.
```

## Prompt 10 — Pipeline local

```text
Objectif : créer le pipeline v0.1 complet et local.

Contexte :
Je veux pouvoir lancer une seule commande pour exécuter ingestion RSS, ingestion HAL, normalisation, scoring et export Markdown.

Tâches :
1. Crée scripts/pipeline.py.
2. Orchestrer dans cet ordre :
   - ingest_rss
   - ingest_hal
   - normalize
   - scoring
   - export_obsidian
3. Chaque étape doit être isolée :
   - log début ;
   - log fin ;
   - try/except ;
   - une étape échouée ne doit pas empêcher les étapes suivantes si les données nécessaires existent.
4. Écrire data/logs/pipeline.log.
5. Ajouter des arguments CLI :
   - --skip-rss
   - --skip-hal
   - --skip-export
   - --mark-exported
6. Mettre à jour Makefile :
   - make run lance le pipeline ;
   - make test lance pytest.

Contraintes :
- Pas de cron.
- Pas d’auto-commit.
- Pas de GitHub Actions encore.
- Pas d’intégration japonaise.
- Pas de publication Hugo.

Tests :
- Crée tests/test_pipeline.py si raisonnable, ou au minimum tester les fonctions d’orchestration sans appels réseau.
- Lancer pytest.
- Lancer make test.
- Lancer make run si les sources réelles sont configurées.
- Terminer par git status et un bilan clair : ce qui fonctionne, ce qui reste fragile, prochains pas.
```

## Prompt 11 — Audit v0.1 et documentation d’usage

```text
Objectif : consolider la v0.1 avant toute extension.

Contexte :
Avant d’ajouter Crossref, OpenAlex, CiNii, NDL, J-STAGE, Zotero ou Hugo, je veux une base stable, documentée et testée.

Tâches :
1. Inspecte tout le dépôt.
2. Vérifie que le périmètre v0.1 est respecté.
3. Lance :
   - make test
   - make run
4. Vérifie l’existence de :
   - data/raw/rss_latest.json
   - data/raw/hal_latest.json
   - data/normalized/db.json
   - data/exports/veille-YYYY-WW.md
   - data/logs/pipeline.log
5. Mets à jour README.md avec :
   - installation ;
   - configuration des sources ;
   - lancement ;
   - lecture du rapport Obsidian ;
   - dépannage ;
   - limites de v0.1 ;
   - roadmap v0.2.
6. Ajoute une section “Ne pas faire en v0.1” :
   - pas de scraping ;
   - pas d’auto-commit ;
   - pas de publication publique ;
   - pas d’API japonaise ;
   - pas de Zotero automatique.

Contraintes :
- Ne pas ajouter de nouvelle fonctionnalité.
- Ne pas refactorer massivement.
- Corriger seulement les bugs nécessaires pour que v0.1 soit stable.

Sortie attendue :
- Résumé des tests.
- État git.
- Liste des fichiers principaux.
- Liste des limites connues.
- Recommandation claire : prêt ou pas prêt pour tag v0.1.
```

# Après v0.1 : petites améliorations ciblées

Une fois cette base stable, je ferais les ajouts dans cet ordre :

|Version|Ajout|Pourquoi|
|---|---|---|
|v0.1.1|Meilleure liste de flux RSS/Atom|Augmenter la couverture sans changer l’architecture.|
|v0.1.2|Meilleur scoring négatif|Réduire le bruit.|
|v0.1.3|Export Obsidian plus joli|Améliorer ton usage quotidien.|
|v0.2|Crossref ou OpenAlex|Ajouter des revues sans RSS.|
|v0.2.1|Export CSL-JSON manuel|Préparer Zotero sans automatiser trop tôt.|
|v0.2.2|GitHub Actions manuel|Tester en CI sans cron.|
|v0.3|CiNii ou NDL, un seul à la fois|Entrer dans l’écosystème japonais prudemment.|
|v0.4|Hugo public expurgé|Publication seulement quand les droits sont propres.|

La règle d’or : **une extension = un connecteur ou un export, jamais les deux à la fois.**
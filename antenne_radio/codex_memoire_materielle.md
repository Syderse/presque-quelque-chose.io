# Mémoire matérielle - antenne radio

## Reprise rapide pour nouvelle conversation

- Toujours commencer par `git status --short`, puis lire `docs/AGENTS.md`, ce fichier, et seulement les morceaux utiles de `antenne_radio/00_plan.md`.
- `docs/CODEX_HANDOFF.md` était absent lors des prompts 5 à 7 ; la source de vérité opérationnelle est donc l'état réel des fichiers + cette mémoire.
- Le sous-projet vit dans `antenne_radio/` et reste local : pas de cron, pas d'auto-commit, pas de GitHub Actions, pas de publication Hugo, pas de Crossref/OpenAlex/CiNii/NDL/J-STAGE, pas de scraping HTML, pas de LLM.
- Le flux v0.1 est complet : ingestion RSS + ingestion HAL -> normalisation `RadioWatchItem` -> scoring lexical -> export Markdown Obsidian -> orchestration par `scripts/pipeline.py`.
- L'environnement local utilisé ici : `.venv` créé dans `antenne_radio/`, dépendances installées depuis `requirements.txt`, tests lancés avec `make test`.
- Attention Git : le worktree large contient déjà des changements hors périmètre antenne (`.agent/rules/hugo-antigravity.md` supprimé, `docs/AGENTS.md` modifié, `antenne_radio/00_plan.md` modifié). Ne pas revert.
- Attention nettoyage : `git diff --check` global signale un whitespace déjà présent dans `antenne_radio/00_plan.md:301`; ne pas confondre avec les fichiers du chantier.

## État actuel du pipeline antenne

- `config/sources.yaml` contient trois RSS activés (`Radio Survivor`, `Journal of Radio & Audio Media`, `Sounding Out!` blog), trois sources RSS/Atom désactivées (`Transom`, `Sounding Out! podcast`, exemple Atom), et une source `hal` activée avec `limit: 20`, catégories `radio_free`/`podcast`, `keyword_limit: 10`, champs HAL enrichis, filtres langue `fr/en` et tri `producedDate_tdate desc`.
- `config/keywords.yaml` contient les catégories utiles au scoring : `radio_core`, `radio_free`, `sound_studies`, `podcast`, `guattari_institutional_psychotherapy`, `japan_later`, `negative_noise`, `technical_radio_noise`.
- `config/scoring.yaml` existe déjà : poids `radio_core: 3`, `radio_free: 3`, `sound_studies: 2`, `podcast: 2`, `guattari_institutional_psychotherapy: 2`, `japan_later: 1`, `negative_noise: -6`, `technical_radio_noise: -2`; seuils `to_read >= 6`, `candidate >= 2`, `ignored < 2`; multiplicateurs de champs `title: 2`, `abstract: 1`, `tags: 2`.
- `scripts/core/models.py` définit `RadioWatchItem`, `SourceType`, `WatchStatus`, `normalize_doi()`, `normalize_url()`, `generate_stable_id()`.
- `scripts/core/io.py` fournit `read_json()`, `write_json()`, `append_log()`, `utc_now_iso()`, `ensure_parent_dir()`.
- `scripts/ingest/ingest_rss.py` écrit `data/raw/rss_latest.json` et logue dans `data/logs/api.log`.
- `scripts/ingest/ingest_hal.py` écrit `data/raw/hal_latest.json` et logue dans `data/logs/api.log`.
- `scripts/core/normalize.py` lit les deux dumps, crée/fusionne `data/normalized/db.json`, déduplique strictement par `id`, garde `raw`, et ne score pas.
- `scripts/core/scoring.py` lit `db.json`, `keywords.yaml` et `scoring.yaml`, score seulement les items `new`, conserve les `exported`, et écrit les champs `keywords_matched`, `negative_keywords_matched`, `relevance_score`, `score_explanation`, `status`.
- `scripts/export/export_obsidian.py` lit `db.json`, génère `data/exports/veille-YYYY-WW.md`, et peut marquer seulement les `to_read` exportés via `--mark-exported`.
- `scripts/pipeline.py` orchestre le flux complet, logue chaque étape dans `data/logs/pipeline.log`, continue après erreur d'étape quand les données suivantes existent, et expose `--skip-rss`, `--skip-hal`, `--skip-export`, `--mark-exported`.
- `Makefile` : `make run` lance `scripts/pipeline.py`, `make test` lance `.venv/bin/pytest`.

## Données présentes après prompts 5 à 7

- `data/raw/rss_latest.json` existe : dernier run réel connu = 52 entrées RSS/Atom. `Radio Survivor` a fourni 52 entrées ; `Transom` a renvoyé statut 301 et 0 entrée avec warning de parsing.
- `data/raw/hal_latest.json` existe : dernier run réel connu = 20 documents HAL, `num_found` HAL annoncé à 27210 pour la requête `(radio OR "radio libre" OR podcast OR radiophonie OR "radios libres" OR podcasting)`.
- `data/normalized/db.json` existe et est un tableau JSON de `RadioWatchItem`, pas un objet avec clé `items`.
- Dernier état mesuré de `db.json` après scoring : 72 items, `source_api` dans `["hal", "rss"]`, `raw` présent sur 72/72 items, distribution `to_read=56`, `candidate=11`, `ignored=5`, `exported=0`.
- `data/exports/veille-2026-21.md` existe après export réel du 2026-05-18 : frontmatter `veille-radio`, `items_to_read: 56`, `items_candidate: 11`, sections `À lire` et `Candidats`.
- Dernier `make run` réel du 2026-05-18 : pipeline OK, `failed_steps=none`, RSS `entry_count=52` avec 1 erreur Transom connue, HAL `result_count=20`, normalisation `added_count=0`, scoring `scored_count=0` et `skipped_count=72`, export `56 to_read` et `11 candidate`.
- Le deuxième passage de `scripts/core/normalize.py` était idempotent : 0 ajout sur les mêmes dumps.
- `data/logs/api.log` contient au moins les warnings RSS Transom ; les étapes futures peuvent y ajouter les erreurs API et doivent créer `data/logs/pipeline.log` au prompt 10.

## Contrats de données à préserver

- `db.json` doit rester lisible, UTF-8, indenté et trié par clés via `write_json()`.
- Ne pas écraser un item existant avec le même `id` lors d'une fusion ; le scoring peut modifier les champs de l'item existant, mais il ne doit pas recréer de doublon.
- Ne jamais supprimer automatiquement les `ignored`; ils servent à auditer le bruit.
- Ne pas modifier les items `exported` au prompt 8, sauf décision explicite ultérieure.
- `source_api` dans les items normalisés doit rester la famille du connecteur (`rss` ou `hal`), pas l'URL de l'API HAL.
- `source_feed` est renseigné côté RSS ; HAL garde l'URL dans le dump brut mais pas dans `source_api`.
- Le champ `raw` doit être conservé dans les étapes 8 à 10.
- `language` vaut souvent `und` côté RSS/HAL actuel ; ne pas supposer qu'il y a toujours `fr` ou `en`.
- `source_type` est provisoire : RSS -> `blog`, HAL -> `journal_article`. Le scoring/export ne doit pas dépendre fortement de cette inférence.

## 2026-05-18 - Initialisation v0.1 locale

- Branche locale créée : `antenne_radio`.
- Squelette projet ajouté sous `antenne_radio/`, sans toucher au `Makefile` ni au `README.md` racine du site Hugo.
- Périmètre v0.1 documenté : RSS/Atom, HAL, normalisation Pydantic, scoring lexical, export Markdown Obsidian.
- Hors-périmètre maintenu : Crossref, OpenAlex, CiNii, NDL, J-STAGE, Zotero CSL, Hugo, changedetection.io, cron automatique, LLM, intégration japonaise spécialisée.
- Aucun connecteur et aucun code réseau ajoutés à ce stade.

## 2026-05-18 - Configuration déclarative v0.1

- Fichiers ajoutés dans `antenne_radio/config/` : `sources.yaml`, `keywords.yaml`, `scoring.yaml`.
- Les sources gardent un champ `enabled` pour activation/désactivation sans suppression.
- `japan_later` contient seulement des mots-clés japonais pour une reprise future, sans intégration japonaise.
- `negative_noise` isole les faux positifs comme radiologie, radiofréquence, radioastronomie et wireless engineering.
- Un test PyYAML dédié vérifie la validité et la cohérence minimale des trois fichiers.

## 2026-05-18 - Modèle pivot Pydantic

- `scripts/core/models.py` définit `SourceType`, `WatchStatus` et `RadioWatchItem`.
- Le modèle reste isolé : aucune écriture `data/`, aucun réseau, aucune logique de scoring.
- Les fonctions pures `normalize_doi`, `normalize_url` et `generate_stable_id` produisent des identifiants déterministes avec priorité DOI, puis URL, puis titre/date/source.
- `tests/test_models.py` couvre l'item minimal, les IDs DOI/URL et le rejet d'un item sans titre.

## 2026-05-18 - Utilitaires JSON et logs

- `scripts/core/io.py` centralise `read_json`, `write_json`, `append_log`, `utc_now_iso` et `ensure_parent_dir`.
- `write_json` crée le dossier parent, écrit en UTF-8, garde les caractères japonais lisibles, indente et trie les clés.
- Les tests `tmp_path` couvrent lecture/écriture JSON, caractères japonais non échappés, valeur par défaut et création de log.

## 2026-05-18 - Connecteur RSS/Atom brut

- `scripts/ingest/ingest_rss.py` lit `config/sources.yaml`, sélectionne les sources activées de type/kind `rss` ou `atom`, parse avec `feedparser` et écrit `data/raw/rss_latest.json`.
- Le dump reste brut : champs extraits utiles, entrée feedparser conservée dans `raw`, métadonnées de sources et erreurs ; aucune écriture dans `data/normalized/db.json`, aucun scoring, aucun scraping HTML.
- Les tests ajoutent `tests/fixtures/sample_rss.xml` et `tests/test_ingest_rss.py` pour valider le parsing sans réseau, les champs `title`/`link`/`source_name`, la non-création de `db.json` et la continuité après erreur.
- Run réel du 2026-05-18 : 52 entrées, toutes depuis Radio Survivor ; Transom retourne un warning de parsing avec statut 301 et 0 entrée, logué dans `data/logs/api.log`.
- Vérification : `make test` dans `antenne_radio/` passe avec 18 tests.

## 2026-05-18 - Connecteur HAL brut

- `scripts/ingest/ingest_hal.py` lit `config/sources.yaml` et `config/keywords.yaml`, construit une requête simple depuis quelques mots-clés positifs, appelle HAL avec `httpx` et écrit `data/raw/hal_latest.json`.
- Fonctions séparées ajoutées : `build_query()`, `fetch_hal()`, `parse_response()`, plus une construction de paramètres limitée (`rows`, `wt=json`, champs, tri, filtres langue).
- Le connecteur reste strictement brut : aucun scoring, aucune écriture dans `data/normalized/db.json`, aucun connecteur Crossref/OpenAlex.
- Les tests ajoutent `tests/fixtures/hal_response.json` et `tests/test_ingest_hal.py` pour couvrir la requête, le parsing fixture, l'appel `httpx.MockTransport` sans réseau et un timeout simulé logué.
- Run réel du 2026-05-18 : 20 documents HAL écrits, `num_found` HAL annoncé à 27210 pour la requête `(radio OR "radio libre" OR podcast OR radiophonie OR "radios libres" OR podcasting)`.
- Limite observée : la requête brute large capte aussi du bruit technique type RF/spectrum sensing ; le filtrage appartiendra aux étapes normalisation/scoring, pas au connecteur.
- Vérification : `make test` dans `antenne_radio/` passe avec 22 tests.

## 2026-05-18 - Normalisation RSS/HAL vers db.json

- `scripts/core/normalize.py` transforme les dumps `data/raw/rss_latest.json` et `data/raw/hal_latest.json` en `RadioWatchItem`.
- Fonctions ajoutées : `normalize_rss_entry()`, `normalize_hal_entry()`, `load_existing_db()`, `merge_items_without_duplicates()`, `save_db()`.
- La fusion déduplique strictement par `id`, ne remplace pas un item existant, ne fait pas de fuzzy matching et ne supprime rien.
- Les items conservent `raw`, gardent `status=new`, ne reçoivent aucun score, et utilisent `source_api` limité à `rss` ou `hal`.
- `data/normalized/db.json` a été créé depuis les dumps réels : 72 items au total, puis deuxième passage idempotent avec 0 ajout.
- Les tests `tests/test_normalize.py` couvrent RSS fixture, HAL fixture, double passage sans doublon et entrée invalide loguée sans interrompre le traitement.
- Vérification : `make test` dans `antenne_radio/` passe avec 26 tests.

## 2026-05-18 - Scoring lexical explicable

- `scripts/core/scoring.py` applique les poids de `config/scoring.yaml` aux catégories de `config/keywords.yaml` sur `title`, `abstract` et `tags`.
- Les regex sont déterministes, UTF-8, insensibles à la casse, avec bordures pour les termes français/anglais afin que `radio` ne matche pas `radiofrequency` ou `radiology`.
- Chaque mot-clé est compté au plus une fois par champ ; l'explication détaille les contributions sous la forme `poids catégorie x multiplicateur champ`.
- Le scoring ne modifie que les items `status=new`; les items `exported`, `candidate`, `to_read` ou `ignored` existants sont conservés tels quels.
- `tests/test_scoring.py` couvre item très pertinent, bruit radiology/radiofrequency, candidate, explication non vide, et non-modification d'un item `exported`.
- Run réel sur `data/normalized/db.json` : 72 items scorés, distribution `to_read=56`, `candidate=11`, `ignored=5`.
- Vérification : `make test` dans `antenne_radio/` passe avec 31 tests.
- Fragilité observée : plusieurs items HAL techniques restent `candidate` parce qu'ils contiennent seulement `radio` dans l'abstract ; c'est acceptable pour v0.1 mais à réviser si la liste candidate devient trop bruyante.

## 2026-05-18 - Export Markdown Obsidian

- `scripts/export/export_obsidian.py` génère un rapport Markdown hebdomadaire `data/exports/veille-YYYY-WW.md` à partir des items scorés.
- Le frontmatter contient `type: veille-radio`, `generated_at`, `week`, `items_to_read`, `items_candidate`.
- Les sections par défaut sont `À lire` et `Candidats`; `Ignorés intéressants` n'apparaît qu'avec l'option `--include-ignored`.
- Chaque item affiche titre, auteurs, source, date, lien, score, explication, et abstract si disponible. Les abstracts RSS HTML sont conservés dans un bloc Markdown simple.
- Par défaut, l'export ne change pas `db.json`; avec `--mark-exported`, seuls les items `to_read` exportés passent en `exported`, les `candidate` restent `candidate`.
- `tests/test_export_obsidian.py` couvre création du fichier, sections attendues, caractères japonais lisibles, non-modification par défaut, et `--mark-exported`.
- Run réel du 2026-05-18 : `data/exports/veille-2026-21.md`, 56 items `to_read`, 11 `candidate`, aucun statut modifié.
- Vérification : `make test` dans `antenne_radio/` passe avec 37 tests.

## 2026-05-18 - Pipeline local v0.1 complet

- `scripts/pipeline.py` orchestre dans l'ordre `ingest_rss`, `ingest_hal`, `normalize`, `scoring`, `export_obsidian`.
- Chaque étape écrit `START`, `OK`, `ERROR` ou `SKIP` dans `data/logs/pipeline.log`; une exception d'étape est capturée et n'empêche pas les étapes suivantes.
- Arguments CLI : `--skip-rss`, `--skip-hal`, `--skip-export`, `--mark-exported`.
- `tests/test_pipeline.py` couvre l'ordre d'orchestration, la continuité après erreur, les options de skip et le passage de `mark_exported`, sans appels réseau.
- `antenne_radio/Makefile` lance maintenant le pipeline avec `make run`; `make test` reste `.venv/bin/pytest`.
- `antenne_radio/README.md` a été corrigé pour ne plus annoncer un `make run` inerte.
- Vérifications : `.venv/bin/pytest` passe avec 41 tests, `make test` passe avec 41 tests, `make run` réel passe avec `Pipeline ok`.
- Hors-périmètre maintenu : pas de cron, pas d'auto-commit, pas de GitHub Actions, pas de publication Hugo, pas d'intégration japonaise spécialisée.

## Fragilités et décisions à garder en tête

- Le RSS Transom a produit des warnings de parsing avec statut 301 et reste déclaré mais désactivé ; ne pas le supprimer sans décision explicite.
- HAL reste bruité malgré le resserrement de Conversation 2 ; le scoring négatif et les prochains réglages de bruit restent les bons leviers avant tout nouveau connecteur.
- Les tests existants évitent les appels réseau avec fixtures et `httpx.MockTransport`; conserver cette discipline.
- Les fichiers de données réels `data/raw/*.json`, `data/normalized/db.json` et futurs exports peuvent devenir volumineux mais restent acceptés en v0.1 pour audit local.
- `.venv`, `.pytest_cache` et `__pycache__` peuvent exister localement après tests ; ne pas les intégrer volontairement.
- Si une future conversation repart de zéro, ne pas relancer les prompts 1 à 10 : la v0.1 locale est complète. Reprendre par audit léger, réglages scoring/export, ou stabilisation de distribution selon besoin.

## 2026-05-18 - Audit v0.1 et documentation d'usage

- Lecture de `docs/AGENTS.md`, `antenne_radio/codex_memoire_materielle.md` et `antenne_radio/00_plan.md` avant intervention.
- Audit du périmètre : les connecteurs actifs restent RSS/Atom + HAL ; pas de Crossref, OpenAlex, CiNii, NDL, J-STAGE, Zotero automatique, Hugo public, scraping, cron, auto-commit ou LLM.
- `make test` passe avec 41 tests.
- Premier `make run` en sandbox sans réseau : pipeline techniquement OK mais dumps RSS/HAL vides et erreurs DNS dans `data/logs/api.log`. Fragilité à garder en tête : toujours vérifier les compteurs et les logs.
- `make run` relancé avec accès réseau : pipeline OK, `failed_steps=none`, RSS 52 entrées, HAL 20 résultats, db 72 items, export `data/exports/veille-2026-21.md` avec 56 `to_read` et 11 `candidate`.
- Artefacts vérifiés : `data/raw/rss_latest.json`, `data/raw/hal_latest.json`, `data/normalized/db.json`, `data/exports/veille-2026-21.md`, `data/logs/pipeline.log`.
- Documentation débutant ajoutée en fin de `README.md` : installation, configuration, lancement, lecture Obsidian, dépannage, limites v0.1, ne-pas-faire v0.1, roadmap v0.2.
- Registre humain des sources créé : `RESSOURCES_SUIVIES.md`.

## 2026-05-19 - Gel du périmètre v1 après audit réel

- Objectif du chantier : clore la reprise, fixer un périmètre v1 court à partir de l'état réel, et ne pas commencer la conversation 2.
- Fichiers modifiés : `antenne_radio/V1_SCOPE.md` créé ; `antenne_radio/codex_memoire_materielle.md` mis à jour.
- Commandes lancées : `git status --short` au début ; lectures ciblées de `docs/AGENTS.md`, de cette mémoire et de `antenne_radio/04_master_plan.md` ; comptage de `data/normalized/db.json` ; `git diff --check -- antenne_radio/V1_SCOPE.md` ; `make test`.
- Tests : `make test` passe avec 41 tests sous Python 3.14.5 / pytest 9.0.3. Le contrôle `git diff --check -- antenne_radio/V1_SCOPE.md` passe.
- Compteurs observés dans `data/normalized/db.json` : fichier présent, 72 items, statuts `to_read=56`, `candidate=11`, `ignored=5`, `source_api` `rss=52`, `hal=20`, champ `raw` présent sur 72/72 items.
- Décisions prises : la v1 est une v1 minimale forte, pas encyclopédique ; elle inclut la consolidation RSS/HAL, scoring, dédoublonnage non destructeur, export Obsidian, export Zotero manuel, au plus un connecteur occidental après audit, contrat public + audit légal, Hugo sobre seulement si légalement acceptable, GitHub Action manuelle sans cron ni auto-commit.
- Reports confirmés : CiNii, NDL, J-STAGE, `changedetection.io`, scraping, flux RSS sortant public, cron, auto-commit, écriture automatique Zotero/Obsidian, LLM, service permanent et interface d'administration.
- Limites restantes : Transom reste fragile ; HAL reste large et bruité ; un pipeline peut finir OK malgré un épisode réseau vide, donc les futurs audits doivent toujours lire les compteurs et logs ; aucune décision légale/publication n'est encore prise.
- Prochain chantier recommandé : Conversation 2, Prompt 3, audit des sources actuelles RSS/HAL et de leur documentation, sans nouvelle API complexe.

Handoff prêt à copier :

```text
Objectif : démarrer la Conversation 2 du master plan v1 par l'audit des sources RSS/HAL existantes.

Avant toute action, lance `git status --short`.
Lis `docs/AGENTS.md`, `antenne_radio/codex_memoire_materielle.md`, `antenne_radio/V1_SCOPE.md`, `antenne_radio/README.md`, `antenne_radio/RESSOURCES_SUIVIES.md` et la Conversation 2 de `antenne_radio/04_master_plan.md`.

État de départ confirmé le 2026-05-19 : v0.1 complète, `make test` passe avec 41 tests, `data/normalized/db.json` contient 72 items (`to_read=56`, `candidate=11`, `ignored=5`), `source_api` `rss=52` et `hal=20`, `raw` présent partout. Ne relance pas les anciens prompts v0.1. Ne commence pas Crossref/OpenAlex, Hugo, cron, auto-commit, scraping ou LLM.
```

## 2026-05-19 - Clôture du chantier sources RSS/HAL

- Objectif du chantier : clore la Conversation 2 en appliquant les ajustements simples issus de l'audit, puis vérifier et documenter l'état RSS/HAL sans commencer la Conversation 3.
- Fichiers modifiés pendant les Prompts 4 et 5 : `antenne_radio/config/sources.yaml`, `antenne_radio/RESSOURCES_SUIVIES.md`, `antenne_radio/codex_memoire_materielle.md`, et les artefacts régénérés `data/raw/rss_latest.json`, `data/raw/hal_latest.json`, `data/normalized/db.json`, `data/exports/veille-2026-21.md`.
- Commandes lancées : `git status --short` ; lectures de `docs/AGENTS.md`, de cette mémoire, de `config/sources.yaml` et de `RESSOURCES_SUIVIES.md` ; `make test` ; `make run` ; contrôles `jq` sur les dumps et `db.json` ; inspection des 80 dernières lignes de `data/logs/api.log` et `data/logs/pipeline.log` ; contrôle de correspondance entre `sources.yaml` et `RESSOURCES_SUIVIES.md`.
- Tests : `make test` passe avec 41 tests sous Python 3.14.5 / pytest 9.0.3.
- Run final du 2026-05-19 11:08 JST : pipeline OK, `failed_steps=none`, RSS `entry_count=144`, HAL `result_count=20`, normalisation `added_count=0`, `saved_count=187`, scoring `scored_count=0`, `skipped_count=187`, export `97 to_read` et `55 candidate`.
- Compteurs observés dans `data/normalized/db.json` : 187 items, `source_api` `rss=144` et `hal=43`, statuts `to_read=97`, `candidate=55`, `ignored=35`, champ `raw` présent sur 187/187 items.
- Sources gardées actives : `radio_survivor` (52 entrées), `journal_radio_audio_media` (42 entrées), `sounding_out_blog` (50 entrées), `hal` (20 documents au dernier run, `num_found=931`).
- Sources ajoutées : `journal_radio_audio_media` via flux RSS Taylor & Francis `hjrs20`, et `sounding_out_blog` via flux WordPress `https://soundstudiesblog.com/feed/`.
- Sources désactivées ou laissées inactives : `transom` désactivé après 0 entrée, statut 301 et warnings feedparser répétés ; `sounding_out_podcast` ajouté désactivé pour éviter le doublon thématique avant décision sur les podcasts ; `example_disabled_journal` reste désactivé.
- HAL corrigé par configuration seulement : requête effective générée depuis `keyword_categories: [radio_free, podcast]` et `keyword_limit: 10`, sans mot isolé `radio`; champs demandés enrichis avec DOI, date complète, langue et type de document.
- Logs : `api.log` ne montre pas de nouvelle erreur après désactivation de Transom ; `pipeline.log` confirme deux runs post-ajustement OK, le second idempotent.
- Source rejetée pour ce chantier : RadioDoc Review reste pertinente, mais aucun flux RSS/Atom stable n'a été vérifié ; ne pas l'ajouter sans URL de flux claire.
- Limites restantes : HAL est nettement moins large (`num_found` ramené d'environ 27219 à 931), mais reste bruité par des podcasts et documents généraux ; les nouveaux flux RSS augmentent fortement le volume à relire ; le scoring n'a pas encore été rééquilibré pour cette nouvelle couverture.
- Prochain chantier recommandé : Conversation 3 du master plan, scoring/bruit/faux positifs/doublons non destructeurs, sans modifier les sources sauf nécessité constatée.

Handoff prêt à copier :

```text
Objectif : démarrer la Conversation 3 du master plan v1 : scoring, bruit, faux positifs et doublons non destructeurs.

Avant toute action, lance `git status --short`. Relis `docs/AGENTS.md`, `antenne_radio/codex_memoire_materielle.md`, `antenne_radio/V1_SCOPE.md`, `antenne_radio/README.md`, `antenne_radio/RESSOURCES_SUIVIES.md`, `antenne_radio/config/sources.yaml`, `antenne_radio/config/keywords.yaml`, `antenne_radio/config/scoring.yaml`, et la Conversation 3 de `antenne_radio/04_master_plan.md`.

État confirmé le 2026-05-19 11:08 JST : `make test` passe avec 41 tests ; dernier `make run` OK avec RSS 144 entrées, HAL 20 résultats, `db.json` 187 items (`to_read=97`, `candidate=55`, `ignored=35`), `source_api` `rss=144` et `hal=43`, `raw` présent partout. Sources actives : Radio Survivor, Journal of Radio & Audio Media, Sounding Out! blog, HAL resserré. Transom est désactivé ; Sounding Out! podcast est déclaré mais désactivé ; RadioDoc Review n'est pas ajouté faute de flux stable. Ne pas commencer Crossref/OpenAlex, CiNii/NDL/J-STAGE, scraping, Hugo, cron, auto-commit ou LLM.
```

## 2026-05-19 - Clôture Conversation 3 scoring/bruit

- Objectif du chantier : améliorer le signal sans perdre des items intéressants, sans nouvelle source, sans export public, sans suppression et sans fuzzy matching destructeur.
- Fichiers modifiés : `antenne_radio/config/keywords.yaml`, `antenne_radio/config/scoring.yaml`, `antenne_radio/tests/test_scoring.py`, `antenne_radio/codex_memoire_materielle.md`.
- Règle ajoutée : nouvelle catégorie `technical_radio_noise` pour le bruit HAL où `radio` désigne réseaux, spectre ou physique (`cognitive radio`, `spectrum sensing`, `dynamic spectrum access`, `5G`, `6G`, `LoRa`, `LoRaWAN`, `UWB`, `V2X`, `channel charting`, `radio telescope`, `radio emission`, `electromagnetic radiation`, `solar wind`, `X-rays`, etc.).
- Pondération ajoutée : `technical_radio_noise: -2`, plus douce que `negative_noise: -6`; seuils inchangés (`to_read >= 6`, `candidate >= 2`) et poids `podcast` inchangé.
- Code scoring : `scripts/core/scoring.py` n'a pas été modifié ; la configuration suffit.
- Doublons : aucun champ `possible_duplicate` n'a été ajouté dans cette passe, car l'audit Prompt 6 n'a trouvé aucun doublon exact DOI/URL/titre ; garder l'idée pour un futur marquage déterministe non destructeur.
- Tests ajoutés : item SHS/radio conservé en `to_read`, item podcast + radio libre favorisé, bruit radiologie/radiofréquence conservé, bruit télécom/radio technique pénalisé, item technique ambigu maintenu en `candidate`.
- Vérifications : `make test` passe avec 45 tests sous Python 3.14.5 / pytest 9.0.3 ; `make run` réel du 2026-05-19 11:23 JST passe avec `failed_steps=none`.
- Compteurs persistés après `make run` : `db.json` reste à 187 items, `to_read=97`, `candidate=55`, `ignored=35`, `rss=144`, `hal=43`; le run a fait RSS `entry_count=144`, HAL `result_count=20`, normalisation `added_count=0`, scoring `scored_count=0`, `skipped_count=187`, export `97 to_read` et `55 candidate`.
- Simulation de rescore complet sans écriture avec la nouvelle configuration : `to_read=92`, `candidate=49`, `ignored=46`; côté HAL seulement, `to_read` passerait de 11 à 6, `candidate` de 26 à 20, `ignored` de 6 à 17 ; RSS resterait stable (`to_read=86`, `candidate=29`, `ignored=29`).
- Bons items vérifiés comme non ignorés en simulation : `Voices from the Margins: How Community Radio Constructs Identity and Enables Participation in Rural Ghana`, `Mapping Three Decades of Radio and Audio Scholarship`, `En réseau, Histoire, Anarchie et Droit" dans "Au Tours du Droit" sur Radio Béton`, `Récits des eaux et des rives`, `Manuel d'analyse du podcast natif.`.
- Bruit traité en simulation : `Safe Queue and Energy-Aware Scheduling in Cognitive Radio Networks`, `Investigating Spectrum Sensing in CR-IoT Networks`, `Unlocking Vehicular Communications: Scaling V2X Traffic on 5G SA`, `Supermassive Black Hole Winds in X-rays`, `Joint Estimation... LuSEE-Night` passent en `ignored`; `Review of Radio Counter-Counter Unmanned Aerial Systems` descend seulement en `candidate`.
- Limite importante : le pipeline ne rescoring pas les items déjà `to_read`, `candidate` ou `ignored`; les nouveaux réglages s'appliquent aux futurs items `new`, ou à un rescore explicite à concevoir plus tard.
- Autre limite : le bruit podcast généraliste HAL reste présent ; ne pas baisser le poids `podcast` sans nouvelle QA, car cela ferait perdre des candidates intéressantes.
- Prochain chantier recommandé : avant ou au démarrage de la Conversation 4, décider s'il faut un mode de rescore/dry-run explicite et un marquage de doublons déterministe non destructeur ; ne pas ajouter cron, Hugo public, LLM ou nouvelles APIs sans gate dédiée.

Handoff prêt à copier :

```text
Objectif : reprendre après la Conversation 3 du master plan v1, sans relancer les prompts déjà faits.

Avant toute action, lance `git status --short`. Relis `docs/AGENTS.md`, `antenne_radio/codex_memoire_materielle.md`, puis seulement la prochaine section utile de `antenne_radio/04_master_plan.md`.

État confirmé le 2026-05-19 : `make test` passe avec 45 tests ; `make run` réel passe avec `failed_steps=none`, RSS `entry_count=144`, HAL `result_count=20`, normalisation `added_count=0`, scoring `scored_count=0`, `skipped_count=187`. `db.json` contient 187 items persistés (`to_read=97`, `candidate=55`, `ignored=35`, `rss=144`, `hal=43`). La nouvelle configuration ajoute `technical_radio_noise: -2` pour pénaliser le bruit HAL radio/télécom/physique. Un rescore simulé sans écriture donnerait `to_read=92`, `candidate=49`, `ignored=46`, avec les bons items radio/SHS conservés. Attention : le pipeline ne rescoring pas les items déjà classés ; ne pas modifier leurs statuts sans commande explicite de rescore/dry-run. Ne commence pas Crossref/OpenAlex, CiNii/NDL/J-STAGE, scraping, Hugo public, cron, auto-commit ou LLM sans demande explicite.
```

## 2026-05-19 - Clôture Conversation 4 exports privés

- Objectif du chantier : rendre les exports privés plus lisibles et ajouter un export Zotero manuel, sans automatisation intrusive et sans commencer la Conversation 5.
- Format Zotero choisi : CSL JSON, parce qu'il mappe directement les champs de `RadioWatchItem`, supporte mieux UTF-8/URL/abstracts que BibTeX pour ce besoin, et reste importable manuellement dans Zotero.
- Commandes d'export : `.venv/bin/python scripts/export/export_obsidian.py` pour `data/exports/veille-YYYY-WW.md`; `.venv/bin/python scripts/export/export_csl.py` pour `data/exports/zotero-veille-YYYY-WW.csl.json`.
- Fichiers modifiés ou créés pendant les Prompts 10 et 11 : `scripts/export/export_obsidian.py`, `scripts/export/export_csl.py`, `tests/test_export_obsidian.py`, `tests/test_export_csl.py`, `README.md`, `data/exports/veille-2026-21.md`, `data/exports/zotero-veille-2026-21.csl.json`, et ce fichier de mémoire.
- Amélioration Obsidian : les abstracts HTML sont nettoyés à l'export, les entités HTML décodées, les abstracts vides type `. <br />` masqués, et une ligne DOI apparaît si `item.doi` existe.
- Export CSL JSON : par défaut, seuls les items `to_read` et `candidate` sont exportés; `--include-ignored` existe mais reste explicite; `db.json` n'est pas modifié.
- Mapping CSL minimal : `id`, `type` approximatif depuis `source_type`, `title`, `container-title`, `issued`, `accessed`, `author` en `literal`, `URL`, `DOI` si présent, `language` sauf `und`, `abstract` nettoyé, `keyword` depuis tags + mots-clés matchés.
- Tests : `.venv/bin/pytest tests/test_export_obsidian.py tests/test_export_csl.py` passe avec 16 tests; `make test` passe avec 55 tests sous Python 3.14.5 / pytest 9.0.3.
- QA réelle du 2026-05-19 : export Obsidian généré avec 97 `to_read` et 55 `candidate`; export CSL généré avec 152 items, 152 URL, 115 avec auteurs, 152 dates `issued`, 126 abstracts, types `webpage=115` et `article-journal=37`.
- Vérifications UTF-8 : `data/exports/veille-2026-21.md` est `text/plain; charset=utf-8`; `data/exports/zotero-veille-2026-21.csl.json` est `application/json; charset=utf-8`; les tests gardent aussi un cas japonais.
- Vérification DOI : la base réelle contient actuellement 0 DOI (`db_with_doi=0`), donc l'export réel contient 0 champ `DOI`; les tests couvrent néanmoins le mapping DOI pour les futurs items.
- Vérification non-destructive : hash SHA-256 de `data/normalized/db.json` identique avant/après exports (`f03ed39089436207cfb0fb2e338cf5d38e48c965299d5bc3c9b2d6d74d25e25a`).
- Limites de mapping : `authors` peut contenir des biographies ou blocs longs venus des flux, donc exporté en CSL `literal`; `source_type` reste provisoire (`blog` -> `webpage`, HAL -> `article-journal`); les abstracts nettoyés peuvent garder du boilerplate de source; aucun enrichissement DOI n'est tenté.
- Prochain chantier recommandé : Conversation 5 du master plan, audit d'une API occidentale unique Crossref ou OpenAlex, sans intégrer les deux et sans toucher à la publication publique avant l'audit légal dédié.

Handoff prêt à copier :

```text
Objectif : démarrer la Conversation 5 du master plan v1 : décider entre Crossref, OpenAlex ou un report documenté.

Avant toute action, lance `git status --short`. Relis `docs/AGENTS.md`, `antenne_radio/codex_memoire_materielle.md`, `antenne_radio/README.md`, `antenne_radio/RESSOURCES_SUIVIES.md`, les scripts d'export privés, puis seulement la Conversation 5 de `antenne_radio/04_master_plan.md`.

État confirmé le 2026-05-19 : `make test` passe avec 55 tests. Les exports privés existent : `data/exports/veille-2026-21.md` et `data/exports/zotero-veille-2026-21.csl.json`. Le format Zotero manuel retenu est CSL JSON. L'export CSL contient 152 items (`to_read` + `candidate`), 152 URL, 115 auteurs, 152 dates, 126 abstracts, mais 0 DOI car `db.json` ne contient actuellement aucun DOI. Le hash de `data/normalized/db.json` reste inchangé après exports. Ne commence pas CiNii/NDL/J-STAGE, scraping, Hugo public, cron, auto-commit, LLM ou publication publique.
```

## 2026-05-19 - QA Conversation 5 API occidentale

- Objectif du chantier : vérifier que l'ajout Crossref issu des Prompts 12 et 13 est propre, sans commencer la Conversation 6.
- Décision Crossref/OpenAlex : Crossref est retenu comme unique connecteur occidental préparé, pour le suivi de revues par ISSN et la récupération future de DOI; OpenAlex est reporté pour éviter une découverte large plus bruyante et une deuxième complexité API dans le même lot.
- Conditions d'usage retenues : source désactivée par défaut (`crossref.enabled: false`), activation seulement avec `CROSSREF_MAILTO`, aucun secret dans le dépôt, `User-Agent` explicite, `mailto` transmis aux requêtes, `rows: 20`, requêtes séquentielles, `polite_delay_seconds: 1`, timeouts, et erreurs 403/429/500 classées dans le dump brut.
- Fichiers modifiés ou créés pour le chantier Crossref/QA : `config/sources.yaml`, `RESSOURCES_SUIVIES.md`, `scripts/ingest/ingest_crossref.py`, `scripts/pipeline.py`, `scripts/core/normalize.py`, `tests/test_config.py`, `tests/test_ingest_crossref.py`, `tests/test_normalize.py`, `tests/test_pipeline.py`, `data/raw/crossref_latest.json`, `data/raw/rss_latest.json`, `data/raw/hal_latest.json`, `data/exports/veille-2026-21.md`, et ce fichier.
- Tests : `make test` passe avec 65 tests sous Python 3.14.5 / pytest 9.0.3.
- Run QA du 2026-05-19 15:43 JST : `make run` passe avec `Pipeline ok`, `failed_steps=none`; Crossref est exécuté en chemin désactivé contrôlé (`result_count=0`, erreur `disabled`) car `CROSSREF_MAILTO` est absent localement.
- Compteurs RSS/HAL observés au même run : RSS `entry_count=144` (`Radio Survivor=52`, `Journal of Radio & Audio Media=42`, `Sounding Out!=50`), HAL `result_count=20`, `num_found=931`, sans erreur HAL dans le dump.
- Compteurs normalisés observés : `db.json` contient 187 items, `rss=144`, `hal=43`, `crossref=0`, statuts `to_read=97`, `candidate=55`, `ignored=35`, champ `raw` présent sur 187/187 items, DOI présents sur 0 item.
- Idempotence et doublons : le dernier pipeline indique `normalize added_count=0`; un second passage direct de `scripts/core/normalize.py` sauvegarde 187 items avec `0 added`; le hash SHA-256 de `db.json` reste `f03ed39089436207cfb0fb2e338cf5d38e48c965299d5bc3c9b2d6d74d25e25a`; doublons exacts observés : `id=0`, `doi=0`, `url=0`.
- Logs : `pipeline.log` confirme le run QA OK; `api.log` ne reçoit pas de nouvelle erreur pendant le run Crossref désactivé, mais conserve d'anciens essais Crossref en erreur avec `radio@example.org` (`403`, `429`, `500`, puis réponse vide). Ne pas les interpréter comme le résultat du run QA final.
- Limites : aucun appel live Crossref n'a été lancé dans cette QA faute de `CROSSREF_MAILTO`; le connecteur reste donc validé par tests mockés et par chemin désactivé réel. Avant activation, fournir une vraie adresse de contact locale, puis lancer un run limité et relire `api.log`, `pipeline.log`, `data/raw/crossref_latest.json` et les doublons DOI/URL.
- Prochain chantier recommandé : Conversation 6, audit légal et contrat public, seulement dans une nouvelle demande explicite; ne pas automatiser, publier, scraper ou ajouter OpenAlex avant ce gate.

Handoff prêt à copier :

```text
Objectif : reprendre après la Conversation 5 du master plan v1, sans relancer les prompts déjà faits et sans commencer une publication publique par accident.

Avant toute action, lance `git status --short`. Relis `docs/AGENTS.md`, `antenne_radio/codex_memoire_materielle.md`, `antenne_radio/RESSOURCES_SUIVIES.md`, `antenne_radio/config/sources.yaml`, puis seulement la prochaine section utile de `antenne_radio/04_master_plan.md`.

État confirmé le 2026-05-19 15:43 JST : `make test` passe avec 65 tests; `make run` passe avec `failed_steps=none`; RSS produit 144 entrées, HAL 20 résultats (`num_found=931`), `db.json` contient 187 items (`rss=144`, `hal=43`, `crossref=0`; `to_read=97`, `candidate=55`, `ignored=35`), aucun doublon exact ID/DOI/URL. Crossref a été ajouté mais reste désactivé par défaut; il nécessite une vraie variable locale `CROSSREF_MAILTO` avant tout appel live. OpenAlex est reporté. Le prochain chantier recommandé est la Conversation 6 (contrat public et audit légal), uniquement si l'utilisateur le demande explicitement. Ne pas ajouter OpenAlex, CiNii/NDL/J-STAGE, scraping, Hugo public, cron, auto-commit ou LLM.
```

## 2026-05-19 - Clôture Conversation 6 contrat public et audit légal

- Objectif du chantier : clore le contrat public avant tout export public, sans publier, sans intégrer Hugo et sans commencer la Conversation 7.
- Fichiers créés ou modifiés : `antenne_radio/LEGAL_AUDIT.md` créé pendant le Prompt 16 ; `antenne_radio/codex_memoire_materielle.md` mis à jour pendant le Prompt 17.
- Commandes et lectures : `git status --short` au début ; relecture de `docs/AGENTS.md`, de cette mémoire, de `antenne_radio/04_master_plan.md` Conversations 6 Prompts 15-17, de `antenne_radio/LEGAL_AUDIT.md`, et vérifications ciblées de la whitelist et des champs interdits.
- Verdict légal global : publiable partiellement seulement. Il n'y a pas de feu vert pour republier la base actuelle, les dumps bruts, les exports privés ou les abstracts. Un futur JSON public ne peut être qu'un index minimal de liens et de métadonnées strictement whitelisted, avec attribution.
- Contrat public provisoire : aucun export public n'existe encore ; les exports actuels restent privés ; toute publication doit passer par une transformation de minimisation, des tests anti-fuite et une nouvelle QA.
- Whitelist publique stricte envisagée : `id`, `title`, `url`, `doi`, `published_at`, `source_name`, `source_type`, `language`, `source_family`, `attribution_id`. Les champs `schema_version`, `generated_at` et `sources` peuvent exister au niveau export, sans données privées.
- Champs interdits en public : `raw`, `abstract`, logs, notes privées, chemins locaux, secrets, champs de debug, `status`, `relevance_score`, `score_explanation`, `keywords_matched`, `negative_keywords_matched`, `discovered_at`, `source_feed`, `source_api` brut, `title_original`, `errors`, `raw_responses`, `ignored`, tout champ douteux. `authors` et `tags` restent exclus de la v0 publique stricte sauf audit et whitelist ultérieurs.
- Sources RSS actives : Radio Survivor, Journal of Radio & Audio Media / Taylor & Francis, et Sounding Out! sont publiables partiellement seulement, comme index de liens avec titre, URL, date, nom de source et attribution. Ne pas republier summaries RSS, excerpts, contenu HTML, images, commentaires, bios auteurs, médias, abstracts ou dumps raw.
- HAL : publiable avec attribution pour des métadonnées strictes et prudentes, en tenant compte de la contrainte de réutilisation non commerciale ; ne pas publier abstracts, fichiers, textes intégraux, raw ou lots enrichis non audités.
- Crossref : métadonnées publiables avec attribution en principe, mais connecteur à reporter côté public tant que `CROSSREF_MAILTO` réel n'a pas été configuré et qu'un run live limité n'a pas été audité. Ne pas publier abstracts Crossref, raw, erreurs, mailto ou champs de debug.
- Sources prévues ou inactives à reporter : Transom, Sounding Out! podcast, OpenAlex, CiNii, NDL, J-STAGE et RadioDoc Review restent hors publication publique tant qu'un audit officiel source par source n'est pas fait.
- Limites restantes : `LEGAL_AUDIT.md` est un audit minimal de prudence, pas un avis juridique ; aucun export public ni test anti-fuite n'a encore été implémenté ; aucun appel live Crossref valide n'a été vérifié ; aucun audit item par item ne permet de publier les abstracts ; les auteurs et tags peuvent contenir du bruit ou des données ambiguës.
- Prochain chantier recommandé : export public désactivé ou privé seulement. Avant toute Conversation 7, vérifier explicitement que la publication reste inactive ou privée tant qu'une whitelist codée et testée n'existe pas.
- Tests Prompt 17 : `make test` n'est pas nécessaire si seuls `LEGAL_AUDIT.md` et cette mémoire sont modifiés, car aucun fichier de code, config ou données générées n'est touché.

Handoff prêt à copier :

```text
Objectif : reprendre après la Conversation 6 du master plan v1 par un chantier "export public désactivé ou privé seulement", sans commencer l'intégration Hugo publique.

Avant toute action, lance `git status --short`. Relis `docs/AGENTS.md`, `antenne_radio/codex_memoire_materielle.md`, `antenne_radio/LEGAL_AUDIT.md`, puis seulement la prochaine section utile de `antenne_radio/04_master_plan.md`.

État confirmé le 2026-05-19 JST : `LEGAL_AUDIT.md` existe. Verdict légal global : publiable partiellement seulement. Whitelist publique stricte : `id`, `title`, `url`, `doi`, `published_at`, `source_name`, `source_type`, `language`, `source_family`, `attribution_id`. Interdits : `raw`, logs, notes privées, chemins locaux, secrets, champs de debug, `abstract`, `status`, scores/explications, mots-clés de scoring, erreurs, `raw_responses`, champs douteux. RSS publics seulement comme index de liens ; HAL métadonnées strictes avec attribution/non-commercial ; Crossref reporté jusqu'à `CROSSREF_MAILTO` réel + run live limité ; sources inactives reportées. Ne crée pas d'intégration Hugo publique, ne publie aucun abstract, ne publie pas `raw`, ne lance pas cron/auto-commit/scraping/LLM/OpenAlex/CiNii/NDL/J-STAGE.
```

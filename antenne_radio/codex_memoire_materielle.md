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

- `config/sources.yaml` contient deux RSS activés (`Transom`, `Radio Survivor`), un exemple Atom désactivé, et une source `hal` activée avec `limit: 20`, champs HAL, filtres langue `fr/en` et tri `producedDate_tdate desc`.
- `config/keywords.yaml` contient les catégories utiles au scoring : `radio_core`, `radio_free`, `sound_studies`, `podcast`, `guattari_institutional_psychotherapy`, `japan_later`, `negative_noise`.
- `config/scoring.yaml` existe déjà : poids `radio_core: 3`, `radio_free: 3`, `sound_studies: 2`, `podcast: 2`, `guattari_institutional_psychotherapy: 2`, `japan_later: 1`, `negative_noise: -6`; seuils `to_read >= 6`, `candidate >= 2`, `ignored < 2`; multiplicateurs de champs `title: 2`, `abstract: 1`, `tags: 2`.
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

- Le RSS Transom actuel produit un warning de parsing avec statut 301 ; ne pas faire échouer tout le pipeline pour cela.
- HAL capte du bruit technique parce que la requête volontairement large contient `radio`; le scoring négatif est précisément là pour abaisser ce bruit, pas pour changer le connecteur.
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

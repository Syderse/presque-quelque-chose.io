# radio-watch / antenne_radio

`antenne_radio` est une petite antenne de veille pour suivre des textes, billets et notices utiles aux études radiophoniques. Elle fonctionne d'abord en local : elle interroge des sources choisies, range les résultats dans des fichiers JSON, applique un score lexical simple, puis produit des exports privés ou publics selon des règles très strictes.

Elle n'est pas un service permanent. Elle ne tourne pas toute seule, ne crée pas de commit, ne publie pas de données brutes et ne lance aucun traitement caché.

## Ce que fait le projet

Le pipeline local peut :

- lire des flux RSS/Atom configurés ;
- interroger HAL ;
- préparer un connecteur Crossref, désactivé par défaut tant qu'une adresse `CROSSREF_MAILTO` réelle n'est pas fournie ;
- normaliser les résultats dans `data/normalized/db.json` ;
- attribuer un statut avec un scoring lexical explicable ;
- générer un rapport Markdown privé pour Obsidian ;
- générer un export CSL JSON privé pour Zotero ;
- générer un JSON public minimal pour la page Hugo, seulement avec les champs autorisés par l'audit légal.

Le pipeline public ne doit jamais exposer les données de travail internes : pas de `raw`, pas de logs, pas d'abstracts, pas de scores, pas d'explications de score, pas de chemins locaux, pas de secrets.

## Ce que le projet ne fait pas

Par défaut, l'antenne ne fait pas ceci :

- pas de cron ;
- pas d'auto-commit ;
- pas de publication automatique ;
- pas de scraping HTML ;
- pas de résumé LLM ;
- pas d'écriture automatique dans Zotero ou Obsidian ;
- pas d'appel Crossref live sans activation explicite et adresse de contact locale ;
- pas d'OpenAlex, CiNii, NDL ou J-STAGE dans l'état actuel.

## Où sont les fichiers

Depuis la racine du dépôt, le module vit dans `antenne_radio/`.

Les fichiers à connaître :

- `README.md` : ce mode d'emploi.
- `Makefile` : commandes courantes.
- `requirements.txt` : dépendances Python.
- `config/sources.yaml` : sources suivies ou gardées en réserve.
- `config/keywords.yaml` : mots-clés positifs et négatifs.
- `config/scoring.yaml` : poids et seuils du scoring.
- `01_RESSOURCES_SUIVIES.md` : registre humain des sources.
- `LEGAL_AUDIT.md` : limites de publication publique.
- `scripts/pipeline.py` : orchestration de la récolte.
- `data/raw/` : dumps bruts locaux.
- `data/normalized/db.json` : base locale normalisée.
- `data/exports/` : exports privés Markdown et CSL JSON.
- `data/logs/` : journaux locaux du pipeline.

Le workflow GitHub Actions de tests vit à la racine du dépôt : `.github/workflows/tests.yml`.

## Première installation locale

Prérequis :

- Python disponible avec la commande `python3`.
- Une connexion internet seulement quand tu veux lancer une vraie récolte avec `make run`.

Depuis la racine du dépôt :

```sh
cd antenne_radio
make install
```

Cette commande crée `.venv/` dans `antenne_radio/`, puis installe les dépendances depuis `requirements.txt`. Les commandes du `Makefile` utilisent ensuite cet environnement automatiquement.

## Vérifier que tout tient

Avant de toucher aux sources ou de lancer une récolte, lance :

```sh
cd antenne_radio
make test
```

`make test` lance la suite de tests avec `.venv/bin/pytest`. Cette commande ne doit pas appeler les sources live et ne demande pas de secret.

Si `make test` échoue parce que `.venv/bin/pytest` n'existe pas, relance :

```sh
make install
make test
```

## Récolte manuelle hebdomadaire

La routine simple, une fois par semaine :

1. Ouvre un terminal à la racine du dépôt.
2. Regarde l'état Git avant de commencer :

```sh
git status --short
```

3. Va dans le module :

```sh
cd antenne_radio
```

4. Vérifie les tests :

```sh
make test
```

5. Lance volontairement la récolte :

```sh
make run
```

`make run` interroge les sources activées, normalise les résultats, applique le scoring et génère le rapport Markdown privé. C'est la commande qui peut faire des appels réseau. Elle ne doit pas être transformée en cron sans décision explicite.

6. Lis le résultat annoncé par le terminal, puis vérifie les journaux si quelque chose semble vide ou étrange :

```sh
tail -n 50 data/logs/pipeline.log
tail -n 50 data/logs/api.log
```

7. Ouvre les exports générés dans `data/exports/` pour lire la veille.

Après un run réussi, les fichiers importants sont généralement :

- `data/raw/rss_latest.json`
- `data/raw/hal_latest.json`
- `data/raw/crossref_latest.json`
- `data/normalized/db.json`
- `data/exports/veille-YYYY-WW.md`
- `data/logs/pipeline.log`
- `data/logs/api.log`

Un pipeline peut finir techniquement "ok" même si une source a renvoyé peu de résultats. Il faut donc lire les compteurs et les logs, surtout après une erreur réseau.

## Rapport Obsidian privé

Le rapport Markdown est écrit dans `data/exports/`, par exemple `data/exports/veille-2026-21.md`.

Il sert à la lecture privée. Il peut contenir des informations qui ne doivent pas être publiées telles quelles : abstracts, score, explication de score, auteurs, tags ou détails de sélection.

Le script ne modifie pas ton vault Obsidian. Tu peux importer ou déplacer le fichier manuellement selon ton propre usage.

Par défaut, l'export ne change pas les statuts dans `db.json`. L'option suivante existe, mais elle doit rester un choix explicite :

```sh
.venv/bin/python scripts/pipeline.py --mark-exported
```

## Export Zotero privé

Pour générer un fichier CSL JSON importable manuellement dans Zotero :

```sh
.venv/bin/python scripts/export/export_csl.py
```

Le fichier est écrit dans `data/exports/`, par exemple `data/exports/zotero-veille-2026-21.csl.json`.

Cet export reste privé. Il ne synchronise rien avec Zotero, ne modifie pas `db.json` et ne doit pas être publié automatiquement.

## Export public minimal Hugo

Le projet possède aussi un export public expurgé pour la section Hugo `/antenne-radio/`.

Pour le générer volontairement :

```sh
make export-public
```

Cette commande écrit `../static/antenne-radio/index.json` en respectant la version de schéma `antenne-radio-public-v0`. Elle ne doit publier que cette whitelist par item :

- `id`
- `title`
- `url`
- `doi`
- `published_at`
- `source_name`
- `source_type`
- `language`
- `source_family`
- `attribution_id`

Tout le reste est interdit en public, notamment `raw`, `abstract`, logs, notes privées, chemins locaux, secrets, statuts, scores, explications, mots-clés internes, auteurs et tags.

Avant toute publication, relis `LEGAL_AUDIT.md` et relance les tests. En cas de doute, ne publie pas.

## CI manuelle GitHub Actions

Le dépôt contient un workflow de test manuel : `.github/workflows/tests.yml`.

Ce workflow sert uniquement à vérifier que la suite de tests de `antenne_radio/` passe dans GitHub Actions. Il ne lance pas `make run`, ne récolte aucune source live, ne génère aucun export, ne publie rien et ne demande aucun secret.

Pour le lancer dans GitHub :

1. Va dans l'onglet `Actions` du dépôt.
2. Choisis `Antenne Radio Tests`.
3. Clique sur `Run workflow`.
4. Garde la branche proposée ou choisis celle que tu veux tester.
5. Clique de nouveau sur `Run workflow`.

Le workflow fait seulement ceci :

- checkout du dépôt ;
- installation de Python 3.12 ;
- cache pip basé sur `antenne_radio/requirements.txt` ;
- `make install` dans `antenne_radio/` ;
- `make test` dans `antenne_radio/`.

Il est déclenché par `workflow_dispatch` uniquement. Il n'y a pas de déclenchement sur `push`, pas de déclenchement sur `pull_request`, pas de cron et pas d'auto-commit.

## Modifier les sources

Les sources se règlent dans `config/sources.yaml`.

Règles simples :

- `enabled: true` active une source.
- `enabled: false` garde une source documentée mais inactive.
- Toute modification de source doit être reportée dans `01_RESSOURCES_SUIVIES.md`.
- Après modification, lance `make test`.
- Pour une vraie récolte, lance ensuite `make run` manuellement.

Pour Crossref, ne mets jamais une adresse personnelle ou un secret directement dans le dépôt. Utilise une variable d'environnement locale si tu décides de l'activer :

```sh
export CROSSREF_MAILTO="adresse-de-contact@example.org"
make run
```

Ne configure pas cette variable dans la CI de tests tant que le but est seulement de vérifier la suite locale.

## Nettoyage local

Pour supprimer les données générées et repartir de zéro :

```sh
make clean-data
```

Attention : cette commande supprime les dumps, la base normalisée, les exports et les logs locaux sous `data/`. Ne l'utilise pas si tu veux conserver l'historique de veille.

## Dépannage rapide

Si une source ne répond pas, regarde d'abord :

```sh
tail -n 50 data/logs/api.log
```

Si le pipeline semble avoir sauté une étape, regarde :

```sh
tail -n 50 data/logs/pipeline.log
```

Si HAL produit trop de bruit technique, commence par `config/keywords.yaml` et `config/scoring.yaml`.

Si le rapport Markdown est vide alors que `db.json` contient des items, vérifie les statuts : l'export privé affiche surtout les items `to_read` et `candidate`.

Si le JSON public contient un champ non prévu par la whitelist, ne publie pas et corrige `scripts/export/export_public.py` ou ses tests avant de continuer.

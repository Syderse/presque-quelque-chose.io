# radio-watch / antenne_radio

`antenne_radio` est une petite antenne de veille pour les études radiophoniques et sonores. Elle interroge des sources choisies (flux RSS, HAL, Crossref, OpenAlex), normalise les résultats dans `data/normalized/db.json`, applique un score lexical, puis produit des exports privés (Obsidian, Zotero) et un index public minimal pour la page Hugo `/antenne-radio/`.

Elle ne tourne pas toute seule, ne crée pas de commit, ne publie pas de données brutes, et ne lance aucun traitement caché.

## Ce que fait le projet

- lire des flux RSS/Atom configurés ;
- interroger HAL, Crossref (6 revues), OpenAlex (19 profils de veille) ;
- normaliser et dédupliquer dans `data/normalized/db.json` ;
- élaguer les notices de travail de plus de 18 mois (sauf `status: exported`) ;
- appliquer un scoring lexical explicable (mots-clés positifs/négatifs, plancher de confiance académique) ;
- générer un rapport Markdown privé pour Obsidian ;
- générer un export CSL JSON privé pour Zotero ;
- générer un JSON public minimal pour Hugo, limité aux champs autorisés par l'audit légal.

## Ce que le projet ne fait pas

- pas de cron ;
- pas d'auto-commit ni de push automatique ;
- pas de scraping HTML ;
- pas de résumé LLM ;
- pas d'écriture automatique dans Zotero ou Obsidian ;
- pas d'appels API live sans adresse de contact locale (`CROSSREF_MAILTO` / `OPENALEX_MAILTO`) ;
- pas de CiNii, NDL, J-STAGE live (reportés à une éventuelle V4).

## État de clôture — Plan final (2026-05-25)

Recette locale finale complète (Prompt 4) :

- `make test` : **172 tests passent**.
- `make run` : pipeline terminé `failed_steps=none`, interrogeant HAL, les RSS, les revues Crossref activées, les profils OpenAlex, avec pruning 18 mois inclus.
- `make export-public` : items publics générés sous schéma `antenne-radio-public-v0`.
- `pnpm run build` depuis la racine : build Hugo réussi.

Compteurs réels après recette (Prompt 1, 2026-05-25) :

- `data/normalized/db.json` : **660 items** — `to_read=292`, `candidate=266`, `ignored=102`.
- `static/antenne-radio/index.json` : **505 items publics**, 28 sources.
- Doublons DOI : **0**.

## Philosophie de maintenance

L'antenne est un outil léger de veille, non une archive. Elle suit deux règles fondamentales :

- **Horizon de pertinence (18 mois)** : à chaque `make run` ou `make weekly`, le pipeline élague de `db.json` les notices de travail (`to_read`, `candidate`, `ignored`, `new`) publiées ou découvertes il y a plus de 18 mois. Les notices marquées `exported` (curation humaine) sont toujours préservées.
- **Curation humaine protégée** : les statuts humains (`to_read`, `ignored`, `exported`) ne sont jamais écrasés silencieusement par le pipeline. Le score machine est dynamique et réversible ; l'arbitrage humain est stable.

## Routine hebdomadaire — une seule commande

```sh
cd antenne_radio
make weekly
```

Cette commande :

1. charge `.env.local` (secrets locaux non commités) ;
2. lance la récolte complète (RSS + HAL + Crossref + OpenAlex) ;
3. normalise et déduplique ;
4. élague les notices de travail de plus de 18 mois ;
5. rescore la base restante ;
6. génère l'export public `static/antenne-radio/index.json` ;
7. affiche un **récapitulatif** : compteurs `db.json` par statut, items publics, sources, doublons DOI ;
8. lance un **scan anti-fuite** sur l'index public — échoue bruyamment si une clé interdite ou un e-mail non autorisé apparaît ;
9. imprime les commandes `git` exactes à lancer soi-même pour publier (geste conscient).

`make weekly` n'effectue **aucun commit ni push**. À la fin, copier-coller les trois commandes affichées :

```sh
git add static/antenne-radio/index.json
git commit -m "veille antenne-radio YYYY-MM-DD"
git push
```

## Lecture des compteurs

Après `make weekly`, le récapitulatif indique :

| Ligne | Lecture |
|---|---|
| `to_read : NNN` | Articles à lire (score ≥ 6) |
| `candidate : NNN` | Candidats intéressants (score ≥ 2) |
| `ignored : NNN` | Bruit écarté automatiquement |
| `exported : NNN` | Curations humaines conservées |
| `Doublons DOI : 0` | Déduplication saine |
| `Index public : NNN items` | Notices publiques exportées |

Si le scan anti-fuite affiche `[ÉCHEC]`, ne pas publier. Corriger d'abord dans `scripts/export/export_public.py` et relancer `make weekly`.

## Où sont les fichiers

Depuis la racine du dépôt, le module vit dans `antenne_radio/`.

| Fichier | Rôle |
|---|---|
| `README.md` | Ce mode d'emploi |
| `Makefile` | Commandes courantes |
| `requirements.txt` | Dépendances Python |
| `config/sources.yaml` | Sources suivies (actives/inactives) |
| `config/keywords.yaml` | Mots-clés positifs et négatifs |
| `config/scoring.yaml` | Poids et seuils du scoring + plancher académique |
| `01_RESSOURCES_SUIVIES.md` | Registre humain des sources |
| `LEGAL_AUDIT.md` | Audit légal et limites de publication |
| `scripts/pipeline.py` | Orchestration de la récolte |
| `scripts/core/prune.py` | Élagage 18 mois |
| `scripts/weekly_report.py` | Récapitulatif + scan anti-fuite |
| `data/raw/` | Dumps bruts locaux |
| `data/normalized/db.json` | Base locale normalisée |
| `data/exports/` | Exports privés Markdown et CSL JSON |
| `data/logs/` | Journaux locaux du pipeline |

## Première installation locale

Prérequis : Python disponible avec la commande `python3`. Depuis le répertoire `antenne_radio/` :

```sh
make install
```

Cette commande crée `.venv/` et installe les dépendances depuis `requirements.txt`.

## Vérifier que tout tient

```sh
make test
```

`make test` lance les tests avec `.venv/bin/pytest`. Ne fait aucun appel réseau, ne demande aucun secret.

## Récolte seule (sans récapitulatif complet)

```sh
make run
```

`make run` interroge les sources activées, normalise, élague, applique le scoring et génère le rapport Markdown privé.

```sh
make export-public
```

`make export-public` génère `static/antenne-radio/index.json` uniquement.

## Export public — whitelist stricte

La whitelist varie selon la famille de source.

**Sources éditoriales (RSS/blogs)** — 10 clés :
`id`, `title`, `url`, `doi`, `published_at`, `source_name`, `source_type`, `language`, `source_family`, `attribution_id`.

**Sources bibliographiques (Crossref, OpenAlex, HAL)** — 13 clés (+ 3) :
`id`, `title`, `url`, `doi`, `published_at`, `source_name`, `source_type`, `language`, `source_family`, `attribution_id`, `authors`, `container_title`, `item_type`.

Tout le reste est interdit en public : `raw`, `abstract`, logs, notes, statuts, scores, explications, mots-clés internes, chemins locaux, secrets.

Avant toute publication, relis `LEGAL_AUDIT.md` et relance les tests.

## Secrets API (Crossref et OpenAlex)

Ne jamais écrire `CROSSREF_MAILTO` ou `OPENALEX_MAILTO` dans le dépôt. Créer un fichier `.env.local` à la racine du dépôt (ignoré par `.gitignore`) :

```sh
CROSSREF_MAILTO=adresse-de-contact@example.org
OPENALEX_MAILTO=adresse-de-contact@example.org
```

`make run` et `make weekly` chargent ce fichier automatiquement. Sans ces variables, les connecteurs Crossref et OpenAlex écrivent `missing_mailto` localement et ne font aucun appel réseau.

## CI manuelle GitHub Actions

Le workflow `.github/workflows/tests.yml` lance uniquement `make test` — aucun appel réseau, aucun secret. Il est déclenché manuellement depuis l'onglet `Actions` du dépôt (`workflow_dispatch`).

## Modifier les sources

1. Éditer `config/sources.yaml` (`enabled: true` / `false`).
2. Mettre à jour `01_RESSOURCES_SUIVIES.md`.
3. Lancer `make test`.
4. Lancer `make weekly` (ou `make run` puis `make export-public`).

## Nettoyage local

```sh
make clean-data
```

Supprime les dumps, la base normalisée, les exports et les logs. Ne pas utiliser si tu veux conserver l'historique de veille.

## Dépannage rapide

```sh
tail -n 50 data/logs/pipeline.log
tail -n 50 data/logs/api.log
```

- Source silencieuse → vérifier `api.log` pour les erreurs réseau.
- Rapport Markdown vide → vérifier que `db.json` contient des items `to_read` ou `candidate`.
- Index public avec une clé non prévue → ne pas publier, corriger `export_public.py`.
- Scan anti-fuite en échec → identifier la source du problème avec `make weekly` et corriger avant tout push.

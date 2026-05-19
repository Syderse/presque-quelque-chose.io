# radio-watch / antenne_radio

`radio-watch` est une antenne locale de veille en études radiophoniques. Elle produit des fichiers locaux, sans service vivant exécuté par Netlify à chaque visite.

Le principe de v0.1 est simple : générer localement les données de veille, les normaliser, les scorer, puis exporter des fichiers Markdown compatibles Obsidian. Le site ne doit recevoir que des fichiers déjà produits au moment du build.

## Périmètre strict v0.1

- Ingestion RSS/Atom.
- Ingestion HAL.
- Normalisation avec Pydantic.
- Scoring lexical simple.
- Export Markdown Obsidian.
- Exécution locale et manuelle.

Le pipeline v0.1 reste local et manuel : il n’ajoute ni cron, ni auto-commit, ni publication Hugo.

## Hors-périmètre v0.1

- Crossref.
- OpenAlex.
- CiNii.
- NDL.
- J-STAGE.
- Zotero CSL ou synchronisation automatique Zotero.
- Intégration Hugo.
- `changedetection.io`.
- Cron automatique.
- Résumés ou traitements LLM.
- Scraping.
- Intégration japonaise spécialisée.

## Commandes

Depuis ce dossier :

```sh
make install
make test
make run
```

`make run` lance le pipeline complet : ingestion RSS/Atom, ingestion HAL, normalisation, scoring lexical et export Markdown dans `data/exports/`.

## Documentation d'usage pour débutants

Cette antenne se lance depuis le dossier `antenne_radio/`. Elle ne publie rien toute seule : elle lit des sources configurées, écrit des fichiers locaux dans `data/`, puis génère un rapport Markdown que tu peux ouvrir dans Obsidian.

### Installation

Pré-requis :

- Python 3 disponible avec la commande `python3`.
- Une connexion internet pour récupérer les sources RSS/HAL lors de `make run`.

Depuis la racine du site :

```sh
cd antenne_radio
make install
```

Cette commande crée un environnement Python local dans `.venv/` puis installe les dépendances de `requirements.txt`. Tu n'as pas besoin d'activer manuellement l'environnement virtuel pour les commandes Makefile : `make test` et `make run` utilisent directement `.venv/`.

### Configuration des sources

Les sources vivent dans `config/sources.yaml`.

- `rss_atom` liste les flux RSS ou Atom.
- `hal` configure la recherche HAL.
- `enabled: true` active une source.
- `enabled: false` garde une source en réserve sans la lancer.
- `limit` limite le nombre de résultats HAL récupérés.

La liste lisible des ressources actuellement suivies est maintenue dans `RESSOURCES_SUIVIES.md`. Quand tu ajoutes, désactives ou modifies une source dans `config/sources.yaml`, mets aussi ce fichier à jour.

Les mots-clés vivent dans `config/keywords.yaml`. Les règles de score vivent dans `config/scoring.yaml`. Pour v0.1, il vaut mieux ajuster ces fichiers plutôt que toucher au code.

### Lancement courant

Pour vérifier que la base tient :

```sh
make test
```

Pour lancer toute la veille :

```sh
make run
```

Après un run réussi, les fichiers importants sont :

- `data/raw/rss_latest.json` : dernier dump RSS/Atom.
- `data/raw/hal_latest.json` : dernier dump HAL.
- `data/normalized/db.json` : base normalisée unique.
- `data/exports/veille-YYYY-WW.md` : rapport Markdown hebdomadaire.
- `data/exports/zotero-veille-YYYY-WW.csl.json` : export CSL JSON manuel pour Zotero, si tu le génères.
- `data/logs/pipeline.log` : journal des étapes du pipeline.
- `data/logs/api.log` : erreurs ou avertissements des sources.

`make clean-data` supprime les dumps, la base, les exports et les logs locaux. À utiliser seulement si tu veux repartir de zéro.

### Lecture du rapport Obsidian

Le rapport est un fichier Markdown simple dans `data/exports/`, par exemple `data/exports/veille-2026-21.md`.

Dans Obsidian, tu peux soit ouvrir ce dossier comme partie de ton coffre, soit déplacer/copier le fichier manuellement dans ton coffre. Le script ne modifie jamais ton vrai vault Obsidian.

Le rapport contient :

- un frontmatter avec la semaine et les compteurs ;
- une section `À lire` pour les items `to_read` ;
- une section `Candidats` pour les items `candidate` ;
- pour chaque item : titre, auteurs, source, date, lien, score, explication et abstract si disponible.

Par défaut, l'export ne marque pas les items comme `exported`. L'option avancée existe, mais elle doit être explicite :

```sh
.venv/bin/python scripts/pipeline.py --mark-exported
```

### Export Zotero manuel

Un export CSL JSON manuel peut être généré sans API Zotero et sans synchronisation :

```sh
.venv/bin/python scripts/export/export_csl.py
```

Le fichier est écrit dans `data/exports/`, par exemple `data/exports/zotero-veille-2026-21.csl.json`. Il contient par défaut les items `to_read` et `candidate`, avec titre, auteurs, source, date, URL, DOI si disponible, type bibliographique approximatif et abstract privé si disponible.

Tu peux ensuite importer ce fichier manuellement dans Zotero avec l'import de fichier standard. Le script ne modifie pas `db.json` et n'écrit pas dans ta bibliothèque Zotero.

### Export public minimal pour Hugo

Après audit légal, un export public expurgé peut être généré :

```sh
make export-public
```

Cette commande écrit `../static/antenne-radio/index.json`, utilisé par la page Hugo `/antenne-radio/`. Le JSON public est limité à une whitelist stricte par item :

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

Il exclut les données brutes, résumés, journaux d'exécution, notes privées, chemins locaux, secrets, statuts, scores, explications, mots-clés internes, auteurs et tags. Les items `ignored` et les sources non auditées ne sont pas exportés.

La page Hugo reste sobre et sans JavaScript dédié. Elle affiche seulement les métadonnées publiques et les liens d'origine. La section désactive ses sorties RSS pour éviter un flux public sortant.

### Dépannage

Si `make test` dit que `.venv/bin/pytest` est introuvable, relance :

```sh
make install
```

Si `make run` finit avec peu ou pas de résultats, lis d'abord :

```sh
tail -n 50 data/logs/pipeline.log
tail -n 50 data/logs/api.log
```

Une erreur réseau peut produire un dump RSS/HAL vide. Dans ce cas, ne conclus pas que les sources sont mortes : relance `make run` avec une connexion valide.

Le warning Transom actuel est connu : le flux répond avec une redirection/statut 301 et peut produire un avertissement de parsing. Le pipeline continue grâce aux autres sources.

Si HAL renvoie des résultats trop techniques, commence par ajuster `config/keywords.yaml` ou `config/scoring.yaml`. Le connecteur HAL doit rester simple en v0.1.

Si le rapport est vide alors que `db.json` contient des items, vérifie les statuts dans `data/normalized/db.json` : seuls `to_read` et `candidate` apparaissent par défaut.

### Limites de v0.1

- Le scoring est lexical et explicable, pas intelligent.
- Le dédoublonnage est volontairement strict : même ID seulement.
- Les abstracts bruts peuvent contenir du HTML venu des flux ; les exports privés les nettoient au mieux sans modifier la source.
- Le pipeline est local et manuel.
- Le pipeline continue après certaines erreurs de source : il faut lire les logs.
- Les fichiers `data/` sont des fichiers plats locaux, pas une base de données serveur.
- Aucun résumé LLM n'est généré.

### Ne pas faire en v0.1

- Pas de scraping.
- Pas d'auto-commit.
- Pas de publication publique.
- Pas d'API japonaise.
- Pas de Zotero automatique.

### Roadmap v0.2

La v0.2 doit rester incrémentale : une extension à la fois.

- Ajouter Crossref ou OpenAlex, mais pas les deux dans le même chantier.
- Préparer un export CSL-JSON manuel, sans synchronisation Zotero automatique.
- Tester éventuellement une GitHub Action manuelle, sans cron.
- Garder CiNii, NDL et J-STAGE pour une phase ultérieure.
- Garder Hugo public pour plus tard, seulement avec un export expurgé et assumé.

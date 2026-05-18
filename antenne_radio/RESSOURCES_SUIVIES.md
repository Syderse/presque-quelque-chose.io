# Ressources suivies par l'antenne radio

Dernière vérification : 2026-05-18 16:47 JST avec `make run`.

Source technique : `config/sources.yaml`. Ce fichier est la liste humaine à tenir à jour quand une source est ajoutée, désactivée ou modifiée.

## Sources actives

| ID | Nom | Famille | URL ou API | Sortie | Dernier état observé |
|---|---|---|---|---|---|
| `transom` | Transom | RSS | `https://transom.org/feed/` | `data/raw/rss_latest.json` | Activée, mais 0 entrée au dernier run ; statut 301 et warning de parsing. |
| `radio_survivor` | Radio Survivor | RSS | `https://www.radiosurvivor.com/feed/` | `data/raw/rss_latest.json` | Activée ; 52 entrées au dernier run ; statut 200. |
| `hal` | HAL radio studies search | API HAL | `https://api.archives-ouvertes.fr/search/` | `data/raw/hal_latest.json` | Activée ; 20 documents au dernier run ; `num_found` annoncé : 27210. |

## Paramètres HAL actuels

- Requête générée au dernier run : `(radio OR "radio libre" OR podcast OR radiophonie OR "radios libres" OR podcasting)`.
- Limite : 20 résultats.
- Langues filtrées : `fr`, `en`.
- Tri : `producedDate_tdate desc`.
- Champs demandés : `docid`, `title_s`, `abstract_s`, `keyword_s`, `authorFullName_s`, `producedDateY_i`, `uri_s`.

## Sources déclarées mais inactives

| ID | Nom | Famille | URL | Raison |
|---|---|---|---|---|
| `example_disabled_journal` | Example journal feed to replace | Atom | `https://example.org/radio-studies.atom` | Exemple désactivé, à remplacer par une vraie source si utile. |

## Ressources explicitement non suivies en v0.1

- Crossref.
- OpenAlex.
- CiNii.
- NDL.
- J-STAGE.
- Zotero automatique.
- Pages HTML à scraper.
- Publication Hugo publique.

## Procédure de mise à jour

1. Modifier `config/sources.yaml`.
2. Mettre à jour ce fichier.
3. Lancer `make test`.
4. Lancer `make run`.
5. Vérifier `data/logs/api.log`, `data/logs/pipeline.log` et les compteurs dans `data/raw/*.json`.

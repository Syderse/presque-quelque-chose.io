# Ressources suivies par l'antenne radio

Dernière vérification : 2026-05-19 11:08 JST avec `make run`.

Source technique : `config/sources.yaml`. Ce fichier est la liste humaine à tenir à jour quand une source est ajoutée, désactivée ou modifiée.

## Sources actives

| ID | Nom | Famille | URL ou API | Sortie | Dernier état observé |
|---|---|---|---|---|---|
| `radio_survivor` | Radio Survivor | RSS | `https://www.radiosurvivor.com/feed/` | `data/raw/rss_latest.json` | Activée ; 52 entrées au dernier run ; statut 200. |
| `journal_radio_audio_media` | Journal of Radio & Audio Media | RSS | `https://www.tandfonline.com/action/showFeed?type=etoc&feed=rss&jc=hjrs20` | `data/raw/rss_latest.json` | Activée ; 42 entrées au dernier run ; statut 200. |
| `sounding_out_blog` | Sounding Out! | RSS | `https://soundstudiesblog.com/feed/` | `data/raw/rss_latest.json` | Activée ; 50 entrées au dernier run ; statut 200. |
| `hal` | HAL radio studies search | API HAL | `https://api.archives-ouvertes.fr/search/` | `data/raw/hal_latest.json` | Activée ; 20 documents au dernier run ; `num_found` annoncé : 931. |

## Paramètres HAL actuels

- Requête générée au dernier run : `("radio libre" OR podcast OR "radios libres" OR podcasting OR "free radio" OR baladodiffusion OR "pirate radio" OR "audio storytelling" OR "community radio" OR "serialized audio")`.
- Le champ `hal.query` dans `config/sources.yaml` sert de référence humaine ; la requête effective est générée par `scripts/ingest/ingest_hal.py` depuis `keyword_categories` et `keyword_limit`.
- Catégories HAL : `radio_free`, `podcast`.
- Limite de mots-clés HAL : 10.
- Limite : 20 résultats.
- Langues filtrées : `fr`, `en`.
- Tri : `producedDate_tdate desc`.
- Champs demandés : `docid`, `title_s`, `abstract_s`, `keyword_s`, `authorFullName_s`, `doiId_s`, `doi_s`, `producedDate_tdate`, `producedDateY_i`, `language_s`, `docType_s`, `uri_s`.

## Sources déclarées mais inactives

| ID | Nom | Famille | URL | Raison |
|---|---|---|---|---|
| `transom` | Transom | RSS | `https://transom.org/feed/` | Désactivé le 2026-05-19 : 0 entrée, statut 301 et warning feedparser répété sur plusieurs variantes de flux. |
| `sounding_out_podcast` | Sounding Out! podcast | RSS | `https://feeds.feedburner.com/SoundingOutPodcast` | Flux valide, mais gardé désactivé pour éviter un doublon thématique avant décision sur les podcasts. |
| `example_disabled_journal` | Example journal feed to replace | Atom | `https://example.org/radio-studies.atom` | Exemple désactivé, à remplacer par une vraie source si utile. |
| `crossref` | Crossref radio journals | API Crossref | `https://api.crossref.org` | Ajouté désactivé après audit Prompt 12 : activation seulement avec identification polie via `CROSSREF_MAILTO`, limite basse et dumps bruts. |

## Paramètres Crossref préparés

- État : désactivé par défaut (`crossref.enabled: false`).
- Identification polie : variable locale `CROSSREF_MAILTO`; aucune adresse personnelle n'est inscrite dans le dépôt.
- Limite basse : `rows: 20`, requêtes séquentielles, `polite_delay_seconds: 1`.
- Revue configurée pour démarrage contrôlé : `Journal of Radio & Audio Media`, ISSN `1937-6529` et `1937-6537`.
- Sortie brute prévue : `data/raw/crossref_latest.json`.

## Ressources explicitement non suivies en v0.1

- OpenAlex.
- CiNii.
- NDL.
- J-STAGE.
- Zotero automatique.
- Pages HTML à scraper.
- Publication Hugo publique.
- RadioDoc Review : ressource pertinente, mais aucun flux RSS/Atom clair vérifié pendant l'audit ; ne pas ajouter sans URL de flux stable.

## Procédure de mise à jour

1. Modifier `config/sources.yaml`.
2. Mettre à jour ce fichier.
3. Lancer `make test`.
4. Lancer `make run`.
5. Vérifier `data/logs/api.log`, `data/logs/pipeline.log` et les compteurs dans `data/raw/*.json`.

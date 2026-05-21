# Ressources suivies par l'antenne radio

Dernière recette locale complète V3 : 2026-05-21 17:15 JST avec `make test`, `make run`, `make export-public` et `pnpm run build`.
Dernière mise à jour documentaire : 2026-05-21 JST avec l'activation de Crossref (plusieurs revues) et d'OpenAlex en live.

Compteurs d'activation V3 : RSS/Atom 239 entrées ; HAL 20 documents ; Crossref actif sur plusieurs revues ; OpenAlex actif sur plusieurs profils et la revue ciblée ; `db.json` trié et mis à jour.

Source technique : `config/sources.yaml`. Ce fichier est la liste humaine à tenir à jour quand une source est ajoutée, désactivée ou modifiée.

## Audit venues et réseaux prioritaires

Statuts humains utilisés : `actif`, `inactif configuré`, `candidat`, `reporté`.

| Cible | Statut humain | Classement | Points d'accès stables repérés | Décision |
|---|---|---|---|---|
| Radio Journal: International Studies in Broadcast & Audio Media | `actif` | Activable via Crossref ; RSS Intellect à valider techniquement | Page officielle Intellect/Intellect Discover ; ISSN `1476-4504`, e-ISSN `2040-1388` ; DOI Intellect de type `10.1386/rjao...` ; page Intellect Discover annonçant un RSS "Latest Articles" | Ajouté dans `crossref.journals` sous `radio_journal`, `enabled: true`. Ne pas dupliquer `journal_radio_audio_media` : c'est une autre revue. |
| Sound Studies: An Interdisciplinary Journal | `actif` | Activable via Crossref ; RSS Taylor & Francis probable à valider | Page officielle Taylor & Francis `https://www.tandfonline.com/journals/rfso20` ; ISSN `2055-1940`, e-ISSN `2055-1959` ; DOI de type `10.1080/20551940...` ; source OpenAlex recherchable par ISSN | Ajouté dans `crossref.journals` sous `sound_studies_journal`, `enabled: true`. Complète `sounding_out_blog` sans le remplacer. |
| JSS / Journal of Sonic Studies | `actif` | Activable via OpenAlex ; Crossref à vérifier ; RSS dédié non confirmé | Page officielle Research Catalogue/JSS ; ISSN `2212-6252` ; DOIs JSS de type `10.22501/JSS...` ; indexation DOAJ et OpenAlex signalée par ISSN Portal/DOAJ | Ajouté comme profil OpenAlex par `primary_location.source.issn`, `enabled: true`. Ne pas utiliser le flux global Research Catalogue comme source JSS. |
| Resonance: The Journal of Sound and Culture | `actif` | Activable via Crossref ; RSS UC Press non confirmé | Page officielle Scholastica/UC Press ; e-ISSN `2688-867X` ; DOI UC Press de type `10.1525/res...` ; revue trimestrielle en ligne | Ajouté dans `crossref.journals` sous `resonance_journal`, `enabled: true`. Ne pas scraper `online.ucpress.edu`. |
| IAMCR Music, Audio, Radio and Sound Working Group | `reporté` | Réseau à suivre par annonces ; pas activable automatiquement | Page officielle IAMCR MARS/MAR avec appels, newsletters et événements ; aucun RSS/API stable repéré pour la page du groupe | Veille manuelle ou semi-manuelle seulement. Pas de scraping HTML ; pas d'ajout à `config/sources.yaml` tant qu'un flux officiel stable n'est pas identifié. |
| ECREA Radio and Sound Section | `reporté` | Réseau à suivre par annonces ; pas activable automatiquement | Page officielle ECREA Radio and Sound ; ECREA Weekly Digest général ; aucun RSS/API stable repéré pour la section | Veille manuelle via page section/Weekly Digest. Pas de scraping HTML ; pas d'ajout à `config/sources.yaml` tant qu'un flux officiel stable n'est pas identifié. |
| MeCCSA Radio & Audio Studies | `actif` | Réseau suivi par RSS/annonces | Flux WordPress officiel `https://radiostudiesnetworkreadinggroup.wordpress.com/feed/`, déjà configuré sous `meccsa_radio_audio_studies` | Déjà couvert : enrichir la fiche humaine, ne pas créer de doublon. |

Notes de non-duplication :

- `journal_radio_audio_media` couvre déjà Journal of Radio & Audio Media par RSS Taylor & Francis et par Crossref contrôlé.
- `sounding_out_blog` couvre déjà Sounding Out! par RSS ; ce n'est pas la revue Taylor & Francis `Sound Studies`.
- Les réseaux IAMCR/ECREA sont pertinents intellectuellement, mais restent reportés côté pipeline faute de flux officiel stable et spécifique.

## Sources actives

| ID | Nom | Famille | URL ou API | Sortie | Dernier état observé |
|---|---|---|---|---|---|
| `radio_survivor` | Radio Survivor | RSS | `https://www.radiosurvivor.com/feed/` | `data/raw/rss_latest.json` | Activée ; 52 entrées au dernier run ; statut 200. |
| `radiomorphoses` | Radiomorphoses | RSS | `https://journals.openedition.org/radiomorphoses/backend?format=rssdocuments` | `data/raw/rss_latest.json` | Activée ; 10 entrées au dernier run ; statut 200. |
| `radio_fanch` | Radio Fañch | RSS | `https://radiofanch.blogspot.com/feeds/posts/default?alt=rss` | `data/raw/rss_latest.json` | Activée ; 25 entrées au dernier run ; statut 200. |
| `les_radios_libres` | Les Radios Libres | RSS | `https://lesradioslibres.wordpress.com/feed/` | `data/raw/rss_latest.json` | Activée ; 10 entrées au dernier run ; statut 200. |
| `la_radio_du_futur` | La Radio du Futur | RSS | `https://radiodufutur.wordpress.com/feed/` | `data/raw/rss_latest.json` | Activée ; 10 entrées au dernier run ; statut 200. |
| `la_lettre_pro` | La Lettre Pro de la Radio | RSS | `https://www.lalettre.pro/xml/syndication.rss` | `data/raw/rss_latest.json` | Activée ; 20 entrées au dernier run ; statut 200. |
| `meccsa_radio_audio_studies` | MeCCSA Radio & Audio Studies | RSS | `https://radiostudiesnetworkreadinggroup.wordpress.com/feed/` | `data/raw/rss_latest.json` | Activée ; 10 entrées au dernier run ; statut 200 ; confirmé comme cible prioritaire déjà couverte, sans doublon. |
| `nieman_storyboard` | Nieman Storyboard | RSS | `https://niemanstoryboard.org/feed/` | `data/raw/rss_latest.json` | Activée ; 10 entrées au dernier run ; statut 200. |
| `journal_radio_audio_media` | Journal of Radio & Audio Media | RSS | `https://www.tandfonline.com/action/showFeed?type=etoc&feed=rss&jc=hjrs20` | `data/raw/rss_latest.json` | Activée ; 42 entrées au dernier run ; statut 200. |
| `sounding_out_blog` | Sounding Out! | RSS | `https://soundstudiesblog.com/feed/` | `data/raw/rss_latest.json` | Activée ; 50 entrées au dernier run ; statut 200. |
| `hal` | HAL radio studies search | API HAL | `https://api.archives-ouvertes.fr/search/` | `data/raw/hal_latest.json` | Activée ; 20 documents au dernier run ; `num_found` annoncé : 931. |
| `crossref` | Crossref radio journals | API Crossref | `https://api.crossref.org` | `data/raw/crossref_latest.json` | Activée durablement avec garde-fou : recette live OK, 20 notices pour Journal of Radio & Audio Media, `total_results=623`, `rows: 20`. |

## Derniers compteurs publics

- `data/raw/rss_latest.json` : 239 entrées RSS actives, 0 erreur au run final.
- `data/raw/hal_latest.json` : 20 documents, 0 erreur, `num_found=931`.
- `data/raw/crossref_latest.json` : 20 notices Crossref, 1 revue interrogée, 0 erreur, `total_results=623`.
- `data/normalized/db.json` : 289 items, dont `to_read=144`, `candidate=89`, `ignored=56`.
- `static/antenne-radio/index.json` : 233 items publics whitelisted après `make export-public`.
- Fusion DOI Crossref : les 20 notices Crossref ont été fusionnées avec les notices T&F/RSS existantes ; 0 doublon DOI observé dans `db.json`.
- Répartition publique actuelle : HAL 37, Journal of Radio & Audio Media / Taylor & Francis Online 33, La Lettre Pro 20, Radio Survivor 52, Sounding Out! 30, Radio Fañch 22, Radiomorphoses 9, Les Radios Libres 9, MeCCSA Radio and Audio Studies 9, Nieman Storyboard 8, La Radio du Futur 4.

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
| `transom` | Transom | RSS | `https://transom.org/feed/` | Juridiquement validé en métadonnées le 2026-05-20, mais techniquement reporté : le run contrôlé a retrouvé 0 entrée, statut 301 et warning feedparser. |
| `sounding_out_podcast` | Sounding Out! podcast | RSS | `https://feeds.feedburner.com/SoundingOutPodcast` | Flux valide, mais gardé désactivé pour éviter un doublon thématique avant décision sur les podcasts. |
| `example_disabled_journal` | Example journal feed to replace | Atom | `https://example.org/radio-studies.atom` | Exemple désactivé, à remplacer par une vraie source si utile. |

## Paramètres Crossref préparés

- État : activé durablement avec garde-fou (`crossref.enabled: true`) ; sans `CROSSREF_MAILTO`, le connecteur écrit `missing_mailto` et ne fait aucun appel réseau Crossref.
- Identification polie : variable locale `CROSSREF_MAILTO` ou `.env.local` ignoré par Git ; aucune adresse personnelle n'est inscrite dans le dépôt.
- Limite basse : `rows: 20`, requêtes séquentielles, `polite_delay_seconds: 1`.
- Revue active pour démarrage contrôlé : `Journal of Radio & Audio Media`, ISSN `1937-6529` et `1937-6537`.
- Revues désormais activées : `Radio Journal: International Studies in Broadcast & Audio Media` (`1476-4504`, `2040-1388`), `Sound Studies: An Interdisciplinary Journal` (`2055-1940`, `2055-1959`), `Resonance: The Journal of Sound and Culture` (`2688-867X`).
- Sortie brute prévue : `data/raw/crossref_latest.json`.
- Recette finale V3 du 2026-05-21 : `CROSSREF_MAILTO` fourni seulement en variable d'environnement locale pour la commande, 20 notices récupérées, 0 erreur, aucun secret exposé dans les artefacts publics ou les logs scannés. Ne pas élargir Crossref sans recette limitée par une seule revue et scan anti-fuite.

## Paramètres OpenAlex préparés

- État : déclaré et désigné actif (`openalex.enabled: true`) ; le pipeline l'appelle en live via `OPENALEX_MAILTO` local.
- Identification polie : `OPENALEX_MAILTO` doit rester local (`.env.local` ou variable d'environnement), jamais commité, jamais écrit dans les artefacts publics.
- Authentification API : la documentation OpenAlex actuelle indique une clé API gratuite pour l'usage courant ; si le connecteur la nécessite, utiliser `OPENALEX_API_KEY` local, jamais commité.
- Point d'accès : API Works `https://api.openalex.org/works`.
- Fenêtre et volume : 18 mois, `per_page: 20`, 1 page maximum par profil, délai poli de 1 seconde entre profils.
- Filtres initiaux : types `article`, `book`, `book-chapter`, `dissertation`, `review` ; langues `fr` et `en` ; exclusion des notices rétractées ou paratextuelles.
- Profils stricts :
  - `radio_studies` : `"radio studies"`, `radiophonic`, `"radio art"`, `"broadcasting history"`.
  - `radio_audio_media` : `"radio and audio media"`, `"audio media"`, `"broadcast media"`, `"Journal of Radio & Audio Media"`.
  - `sound_studies` : `"sound studies"`, `"sonic media"`, `"auditory culture"`, `"listening studies"`.
  - `podcast_studies` : `"podcast studies"`, `podcasting`, `"audio storytelling"`, `"serialized audio"`.
  - `community_free_radio` : `"community radio"`, `"free radio"`, `"pirate radio"`, `"radio libre"`, `"radios libres"`.
  - `journal_sonic_studies_venue` : profil de venue par filtre `primary_location.source.issn:2212-6252`, désormais activé.
- Exclusions de bruit obligatoires : `radio frequency`, `radiofrequency`, `radiotherapy`, `radioactive`, `radio telescope`, `radio astronomy`, `electromagnetic radiation`, `cognitive radio`, `spectrum sensing`, `beamforming`, `MIMO`, `5G`, `6G`.
- Champs privés autorisés au premier passage : identifiants OpenAlex/DOI, titre, date, type, langue, source primaire, signaux `topics`/`primary_topic`/`keywords`, et `relevance_score` OpenAlex uniquement pour tri privé.
- Champs interdits : `abstract_inverted_index`, abstract reconstruit, auteurs, affiliations, `locations`, PDF/fulltext, références, raw/logs/secrets en public. Le score de pertinence interne et `relevance_score` OpenAlex ne doivent jamais entrer dans `static/antenne-radio/index.json`.
- Recette d'activation V3 du 2026-05-21 : OpenAlex et Crossref (plusieurs revues) sont désormais actifs et intégrés dans la récolte live.

## Ressources explicitement non suivies en v0.1

- CiNii.
- NDL.
- J-STAGE.
- Zotero automatique.
- Pages HTML à scraper.
- Publication des exports privés hors whitelist.
- RadioDoc Review : ressource pertinente, mais aucun flux RSS/Atom clair vérifié pendant l'audit ; ne pas ajouter sans URL de flux stable.

## Procédure de mise à jour

1. Modifier `config/sources.yaml`.
2. Mettre à jour ce fichier.
3. Lancer `make test`.
4. Lancer `make run`.
5. Vérifier `data/logs/api.log`, `data/logs/pipeline.log` et les compteurs dans `data/raw/*.json`.

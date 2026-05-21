# Audit juridique et technique prudent pour Antenne radio

## Date, avertissement et résumé exécutif

**Date de l’audit :** 2026-05-20  
**Statut du document :** version de travail prudente, exploitable pour gouvernance technique et réduction du risque  
**Avertissement :** ce document n’est **pas** un avis juridique professionnel. C’est un cadre de décision prudent pour un projet personnel et universitaire. En cas de doute sérieux sur une source, sur une licence, sur des CGU, sur des droits voisins, sur une base de données ou sur une republication d’extraits, la règle du projet doit être : **ne pas exposer publiquement tant que la vérification n’est pas faite**.

Le périmètre intellectuel du projet est clairement orienté vers les radio studies, l’histoire du médium, l’esthétique radiophonique, les radios libres, la création documentaire et le podcast, avec un intérêt appuyé pour l’axe Japon / mini-FM / Kogawa / Guattari, ainsi que pour la publication éventuelle sur un site Hugo. Cela ressort déjà des notes de chantier du dépôt, qui évoquent explicitement la cartographie du champ, les radio studies, le podcast, les radios libres, la création sonore et l’architecture Hugo. fileciteturn23file0L1-L59 fileciteturn22file0L1-L52

### Résumé exécutif

Le projet **Antenne radio** peut être mené de manière raisonnablement sûre **à condition de séparer nettement** :

- un **pipeline privé** riche, réservé à la veille, à l’analyse, à l’import Zotero et au débogage ;
- un **export public minimaliste**, limité à des liens et métadonnées strictement nécessaires à l’orientation des lecteurs.

Le principe directeur doit être le suivant : **plus une donnée ressemble à du contenu éditorial rédigé, illustré, sonorisé ou structuré comme une base propriétaire, plus elle doit rester privée, voire ne pas être récoltée du tout**. À l’inverse, les métadonnées bibliographiques minimales, l’URL canonique, le DOI, le nom de la source, la date, la langue, le type de document et un identifiant technique stable sont généralement les meilleurs candidats pour l’export public.

Le projet est **fortement faisable** pour les familles suivantes :

- plateformes académiques à vocation de signalement ou de métadonnées ;
- catalogues, bibliothèques et archives disposant de points d’accès stables ;
- revues et blogs disposant d’un RSS/Atom propre ;
- index de podcasts lorsque l’usage reste limité au **signalement**.

Le projet devient **sensiblement plus risqué** dès qu’il touche :

- aux **abstracts** et descriptions longues ;
- aux **contenus RSS complets** ;
- aux **pages HTML complètes** ;
- aux **PDF, images, audio, transcriptions** ;
- aux **dumps bruts** d’API ou de flux ;
- aux **plateformes commerciales** dont les CGU restreignent fortement l’automatisation ou réservent l’usage à certaines APIs.

### Verdict global

Le verdict global recommandé est :

- **export public : autorisé seulement pour un jeu de métadonnées minimales, source par source, avec allowlist stricte** ;
- **pipeline privé : autorisé de façon privée, compartimentée, non versionnée dans Git, avec stockage local des données riches** ;
- **scraping HTML massif : déconseillé par défaut** ;
- **republication de contenus, d’extraits longs, d’images, de PDF, d’audio, de transcriptions : hors périmètre par défaut** ;
- **sources ambiguës ou commercialement sensibles : reportées, strictement limitées, ou exclues du pipeline automatisé**.

### Note de clôture V3 académique

Au gel V3 du 2026-05-21, l'implémentation réelle est plus restrictive que plusieurs recommandations prospectives de cet audit : l'export public Hugo reste limité à la whitelist technique `id`, `title`, `url`, `doi`, `published_at`, `source_name`, `source_type`, `language`, `source_family`, `attribution_id`.

Crossref est activé seulement avec garde-fou local (`CROSSREF_MAILTO` obligatoire, `rows: 20`, une revue active). OpenAlex est configuré, testé et documenté, mais désactivé par défaut. Les venues prioritaires ajoutées en V3 restent inactives tant qu'une recette limitée par source n'a pas été inspectée. La littérature japonaise (`CiNii`, `NDL`, `J-STAGE`) est explicitement reportée dans une V4 séparée et ne doit pas être traitée comme active dans la configuration V3.

## Politique générale du projet

### Politique générale du projet

Le projet doit être gouverné par cinq règles simples.

Première règle : **le site public n’est pas une archive miroir**. Il ne republie pas les contenus sources ; il renvoie vers eux.

Deuxième règle : **tout ce qui est utile à la veille n’est pas forcément publiable**. Il faut penser en deux contrats de données distincts : privé et public.

Troisième règle : **l’absence de paywall ne vaut pas licence de réutilisation**. Un texte librement accessible n’est pas pour autant librement réutilisable.

Quatrième règle : **une source utile n’est pas nécessairement une source automatisable**. Certaines sources peuvent rester en veille manuelle, ou en enrichissement secondaire seulement.

Cinquième règle : **en cas d’ambiguïté, on réduit**. On ne publie ni résumé, ni abstract, ni body HTML, ni transcription, ni image, ni audio, ni dump brut.

### Contrat public de données

Le contrat public recommandé doit être un contrat **d’allowlist**, pas de blacklist. Tout champ absent de la liste publique est considéré comme non publiable par défaut.

#### Champs publics autorisés par défaut

```json
[
  "id",
  "title",
  "original_url",
  "doi",
  "published_at",
  "source_name",
  "source_type",
  "source_family",
  "language",
  "attribution_id",
  "legal_status",
  "audit_date"
]
```

#### Champs publics supplémentaires recommandés

Je recommande d’ajouter, lorsque disponibles et lorsque la source est principalement bibliographique :

```json
[
  "authors",
  "container_title",
  "item_type",
  "issn",
  "isbn",
  "canonical_url",
  "record_url",
  "license_label",
  "open_access_status"
]
```

**Pourquoi les ajouter :** un index universitaire sans auteurs ni titre de revue reste trop pauvre pour être utile. En pratique, les noms d’auteur, le titre de revue, le type de document et l’identifiant du support relèvent souvent de la métadonnée de signalement plutôt que d’un contenu éditorial à forte expressivité.  
**Prudence :** si une source n’est pas bibliographique mais éditoriale ou journalistique, ne publier que `title + url + date + source_name + source_type + language + legal_status`.

#### Champs publics interdits par défaut

```json
[
  "raw",
  "summary",
  "description",
  "abstract",
  "content",
  "content:encoded",
  "html",
  "full_text",
  "pdf_url",
  "image_url",
  "audio_url",
  "transcript",
  "logs",
  "private_notes",
  "local_path",
  "secrets",
  "debug",
  "status",
  "relevance_score",
  "score_explanation",
  "keywords_matched",
  "negative_keywords_matched",
  "discovered_at",
  "source_feed",
  "source_api",
  "title_original",
  "errors",
  "raw_responses"
]
```

### Politique privée de collecte

Le pipeline privé peut stocker davantage, mais avec des garde-fous stricts :

- réponses API brutes ;
- résumés de flux ;
- abstracts ;
- HTML source ;
- notes internes ;
- logs ;
- erreurs ;
- identifiants techniques ;
- traces de débogage ;
- URLs vers PDF ou audio ;
- tables de correspondance et enrichissements Zotero.

Mais ces données doivent être :

- stockées **hors dossier Hugo public** ;
- **hors dépôt Git** ;
- protégées par une politique de rétention ;
- purgées si elles n’ont plus d’utilité ;
- invisibles aux exports automatiques.

### Politique des abstracts

La règle générale recommandée est très stricte :

- **par défaut : abstract privé seulement** ;
- **exception possible :** abstract explicitement sous licence claire de réutilisation, ou issu d’une source de métadonnées ouverte dont l’usage public de l’abstract est explicitement permis ;
- **en cas de doute :** ne pas publier.

Même quand un abstract est visible sur une page ou dans une API, il reste souvent plus expressif et juridiquement plus sensible que de simples métadonnées. Le bénéfice public d’un abstract exposé sur le site ne compense pas le risque.

### Politique des contenus RSS

Le RSS est un excellent **point d’entrée**, mais un mauvais **contrat d’export public**.

Politique recommandée :

- utiliser RSS/Atom pour la détection de nouveautés ;
- normaliser immédiatement vers un schéma interne ;
- conserver le flux brut seulement dans l’espace privé ;
- considérer `description`, `summary`, `content:encoded` comme **non publics** par défaut ;
- n’exposer publiquement qu’un sous-ensemble de métadonnées minimales.

### Politique des APIs

Hiérarchie recommandée des points d’accès :

- **API officielle** ;
- **OAI-PMH** ;
- **export bibliographique stable** ;
- **RSS/Atom** ;
- **sitemap** ;
- **HTML** seulement en dernier recours ;
- **scraping sans point d’accès clair** à éviter.

Règles techniques :

- User-Agent explicite ;
- mailto de contact si la source le recommande ou si l’API est académique ;
- cache local systématique ;
- respect des codes `429`, `403`, `5xx` ;
- backoff exponentiel ;
- pagination bornée ;
- reprise sur checkpoint ;
- pas de moissonnage massif sans nécessité.

### Politique des sources académiques

Les sources académiques doivent être le cœur du pipeline public :

- elles fournissent souvent des métadonnées de meilleure qualité ;
- elles sont plus adaptées au signalement bibliographique ;
- elles permettent plus facilement le DOI, la langue, le type de document et l’identification de version.

Ordre recommandé de confiance pratique :

- HAL ;
- Crossref ;
- OpenAlex ;
- DOAJ ;
- Persée ;
- OpenEdition ;
- Érudit ;
- ABES / Sudoc / theses.fr ;
- Library of Congress / BnF / Europeana / Internet Archive pour les notices ;
- plateformes commerciales ou semi-commerciales seulement en enrichissement limité.

### Politique des sources journalistiques et blogs

Pour les blogs, revues web, magazines et sites éditoriaux :

- privilégier le RSS ;
- à défaut, collecte manuelle ou semi-manuelle ;
- ne jamais republier le texte ;
- pas d’extraits longs ;
- pas de copie du HTML ;
- pas d’images reprises.

### Politique des podcasts et fichiers audio

Règle centrale : **ne pas devenir une rediffusion déguisée**.

Politique recommandée :

- on peut signaler un épisode, une série, une émission, un producteur ;
- on peut stocker en privé un lien vers l’audio original si utile à la veille ;
- on ne republie pas les fichiers audio ;
- on ne republie pas les transcriptions ;
- on n’expose pas de lien direct de téléchargement si cela contourne l’expérience voulue par la source ;
- on préfère l’URL de la page éditoriale à l’URL technique du média.

### Politique de rate limiting

Trois classes suffisent.

**Classe prudente faible cadence**

- blogs ;
- revues éditoriales ;
- plateformes incertaines ;
- cadence quotidienne ou manuelle ;
- 1 requête à la fois ;
- gros cache ;
- pas de cron agressif.

**Classe académique normale**

- APIs documentées ;
- OAI-PMH ;
- catalogues ;
- cadence planifiée ;
- limitation par lots ;
- checkpointing.

**Classe manuelle seulement**

- sources sans API claire ;
- plateformes commerciales ;
- pages très protégées ;
- sources aux CGU ambiguës.

### Politique de logs et fichiers bruts

À proscrire de tout export public :

- messages d’erreur détaillés ;
- headers ;
- tokens ;
- mailto de contact ;
- chemins locaux ;
- contenu brut d’API ;
- contenu brut RSS ;
- score de classement interne ;
- diagnostics de pertinence.

### Politique Git, publication et Hugo

Le dépôt séparera trois zones :

- `private_store/` ou équivalent, **hors Git**, pour les données riches ;
- `build_cache/`, **hors Git**, pour les réponses temporaires ;
- `public_export/`, seul endroit admissible pour ce qui nourrit Hugo.

La présence d’une réflexion déjà poussée sur Hugo dans vos notes de dépôt justifie pleinement cette séparation stricte entre génération, rendu et actifs publics. fileciteturn22file0L1-L52

## Tableau synthétique de toutes les sources

| Source | Famille | Point d’accès recommandé | Statut recommandé | Public | Décision rapide |
|---|---|---|---|---|---|
| Radio Survivor | blog / RSS | RSS si disponible, sinon pages d’articles | VALIDÉ PRUDENT | métadonnées strictes | `active: true` |
| Journal of Radio & Audio Media / T&F | revue | page revue, alertes, DOI, Crossref | VALIDÉ STRICT | liens + métadonnées | `active: true` |
| Sounding Out! | revue / blog | RSS / pages | VALIDÉ PRUDENT | métadonnées strictes | `active: true` |
| Radiomorphoses | revue académique | RSS / OpenEdition | VALIDÉ PRUDENT | métadonnées bibliographiques | `active: true` |
| Radio Fañch | blog / site | HTML / RSS si disponible | VALIDÉ STRICT | liens seulement | `active: true` |
| Les Radios Libres | blog / site | HTML / RSS si disponible | VALIDÉ STRICT | liens seulement | `active: true` |
| La Radio du Futur | blog / site | HTML / RSS si disponible | VALIDÉ STRICT | liens seulement | `active: true` |
| La Lettre Pro | presse pro | HTML / newsletter / pages | VALIDÉ STRICT | liens seulement | `active: true` |
| MeCCSA Radio & Audio Studies | réseau académique | pages / RSS | VALIDÉ STRICT | liens + métadonnées | `active: true` |
| Nieman Storyboard | site éditorial | RSS / pages | VALIDÉ STRICT | liens + métadonnées | `active: true` |
| Transom | site ressource / podcasting | RSS / pages | VALIDÉ PRUDENT | métadonnées strictes | `active: true` |
| RadioDoc Review | revue académique | pages revue / RSS | VALIDÉ PRUDENT | métadonnées bibliographiques | `active: true` |
| HAL | archive ouverte | API / OAI-PMH | VALIDÉ PRUDENT | métadonnées bibliographiques | `active: true` |
| Crossref | API bibliographique | API | VALIDÉ PRUDENT | métadonnées bibliographiques | `active: true` |
| OpenAlex | API bibliographique | API Works | VALIDÉ PRUDENT | métadonnées bibliographiques strictes | `active: false` jusqu'à recette live |
| CiNii | bibliographique | API / pages | VALIDÉ PRUDENT | métadonnées bibliographiques | reporté V4 japonaise, non actif en V3 |
| NDL | catalogue | API / SRU / pages | VALIDÉ PRUDENT | notices | reporté V4 japonaise, non actif en V3 |
| J-STAGE | revues académiques | pages / API selon cas | VALIDÉ PRUDENT | métadonnées bibliographiques | reporté V4 japonaise, non actif en V3 |
| Cairn | plateforme éditoriale | pages / DOI / enrichissement secondaire | VALIDÉ STRICT | liens + métadonnées minimales | `active: true` |
| Persée | portail académique | API / OAI / pages | VALIDÉ PRUDENT | métadonnées bibliographiques | `active: true` |
| OpenEdition Books | livres académiques | pages / métadonnées / OAI selon cas | VALIDÉ PRUDENT | métadonnées bibliographiques | `active: true` |
| OpenEdition Journals | revues académiques | RSS / métadonnées / OAI selon cas | VALIDÉ PRUDENT | métadonnées bibliographiques | `active: true` |
| Érudit | revues académiques | pages / API selon cas | VALIDÉ PRUDENT | métadonnées bibliographiques | `active: true` |
| DOAJ | index de revues | API | VALIDÉ PRUDENT | métadonnées bibliographiques | `active: true` |
| WorldCat | catalogue | API licenciée ou usage manuel | À REPORTER | pas d’automatisation publique | `active: false` |
| Library of Congress | catalogue | API / JSON | VALIDÉ PRUDENT | notices | `active: true` |
| BnF / Gallica | catalogue / bibliothèque numérique | API / IIIF / OAI selon cas | VALIDÉ PRUDENT | notices et métadonnées | `active: true` |
| Sudoc / Abes | catalogue universitaire | API / SRU / pages | VALIDÉ PRUDENT | notices | `active: true` |
| theses.fr | thèses | API / pages | VALIDÉ PRUDENT | notices de thèse | `active: true` |
| Isidore | SHS / découverte | API / pages | VALIDÉ PRUDENT | métadonnées de signalement | `active: true` |
| ORCID | identifiants auteurs | API / pages publiques | VALIDÉ PRUDENT | identifiants et noms, avec mesure | `active: true` |
| Unpaywall | enrichissement OA | API | VALIDÉ PRUDENT | statut OA, lien, DOI | `active: true` |
| Europeana | patrimoine | API | VALIDÉ PRUDENT | notices et métadonnées | `active: true` |
| Internet Archive | archive / notices | metadata API / pages | VALIDÉ PRUDENT | notices et métadonnées | `active: true` |
| INA | archives audio-visuelles | notices publiques seulement | VALIDÉ STRICT | notices, jamais médias | `active: true` |
| France Culture / Radio France | radio / podcast | RSS / pages éditoriales | VALIDÉ STRICT | liens + métadonnées minimales | `active: true` |
| ARTE Radio | radio / podcast | pages / feeds si disponibles | VALIDÉ STRICT | liens + métadonnées minimales | `active: true` |
| BBC Sounds / BBC Radio | radio / podcast | pages / RSS quand présent | VALIDÉ STRICT | liens + métadonnées minimales | `active: true` |
| NPR / podcasts publics | radio / podcast | RSS / pages | VALIDÉ PRUDENT | métadonnées minimales | `active: true` |
| Apple Podcasts | annuaire | usage secondaire seulement | À REPORTER | pas source primaire | `active: false` |
| Spotify | plateforme commerciale | API officielle seulement si besoin | À ÉVITER | pas de harvesting primaire | `active: false` |
| Deezer | plateforme commerciale | API / pages, usage secondaire | À REPORTER | pas source primaire | `active: false` |
| SoundCloud | plateforme audio | API / pages, usage secondaire | À REPORTER | pas source primaire | `active: false` |
| Mixcloud | plateforme audio | pages, usage secondaire | À REPORTER | pas source primaire | `active: false` |
| Podcast Index | index podcast | API | VALIDÉ PRUDENT | métadonnées de signalement | `active: true` |


## Fiches détaillées source par source

### Radio Survivor

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
blog / RSS

**Pertinence pour l’antenne :**  
Actualité critique, radio communautaire, mini-FM, LPFM, et histoire des médias alternatifs et de la création sonore.

**Point d’accès recommandé :**  
RSS si disponible, sinon pages d’articles.

**Pages officielles consultées :**
- https://www.radiosurvivor.com/
- flux RSS publics de syndication

**Constats juridiques et techniques :**
- Flux RSS public émis par WordPress standard.
- Respecter les droits d'auteur des textes d'analyse originaux.

**Collecte privée autorisée ou raisonnable :**
- métadonnées de syndication
- titre
- original_url
- date
- description courte

**Affichage public recommandé :**
- métadonnées strictes

**Champs interdits en public :**
- content:encoded
- résumé long
- description complète
- images

**Attribution minimale :**  
`Source: Radio Survivor — lien vers la notice originale.`

**Rate limit / conditions techniques :**  
Ingestion quotidienne ; cache local ; 1 requête par seconde.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : couverture inégalée des radios libres et communautaires aux États-Unis
- notes d’implémentation : `curated_only: true`

### Journal of Radio & Audio Media

**Statut recommandé :**  
VALIDÉ STRICT

**Famille :**  
revue académique propriétaire

**Pertinence pour l’antenne :**  
Revue scientifique internationale de référence majeure pour l'étude du média radio et de l'audio.

**Point d’accès recommandé :**  
page revue, alertes, DOI, Crossref.

**Pages officielles consultées :**
- https://www.tandfonline.com/journals/hjrs20
- base de métadonnées Crossref

**Constats juridiques et techniques :**
- Aspiration web directe strictement interdite par les conditions d'utilisation de Taylor & Francis.
- Les métadonnées restent accessibles via Crossref ou OpenAlex.

**Collecte privée autorisée ou raisonnable :**
- DOI
- titre
- auteurs
- date
- revue
- résumés via API Crossref

**Affichage public recommandé :**
- liens et métadonnées bibliographiques minimales

**Champs interdits en public :**
- abstracts (protégés)
- PDF
- html
- scraping HTML direct

**Attribution minimale :**  
`Source: Journal of Radio & Audio Media (Taylor & Francis) — lien DOI.`

**Rate limit / conditions techniques :**  
Requêtes via le Polite Pool de Crossref ; cache local obligatoire.

**Risques :**  
Modéré (si scraping), Faible (via Crossref).

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : revue scientifique de référence absolue dans la discipline
- notes d’implémentation : `use_crossref_only: true`

### Sounding Out!

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
revue / blog académique

**Pertinence pour l’antenne :**  
Publication majeure et novatrice en sound studies, culture sonore et théories de l'écoute.

**Point d’accès recommandé :**  
RSS / pages d'articles.

**Pages officielles consultées :**
- https://soundstudiesblog.com/
- flux de syndication RSS

**Constats juridiques et techniques :**
- RSS ouvert émis par CMS WordPress standard.
- Politique de respect du droit d'auteur sur les essais sonores rédigés.

**Collecte privée autorisée ou raisonnable :**
- métadonnées de syndication
- titre
- original_url
- date
- description courte

**Affichage public recommandé :**
- métadonnées strictes

**Champs interdits en public :**
- HTML complet des articles
- images d'illustration

**Attribution minimale :**  
`Source: Sounding Out! — lien vers l'article original.`

**Rate limit / conditions techniques :**  
Cadence prudente, une requête à la fois, cache de 24h.

**Risques :**  
Faible à modéré.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : publication pionnière et dynamique en sound studies
- notes d’implémentation : `meta_only: true`

### Radiomorphoses

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
revue académique ouverte

**Pertinence pour l’antenne :**  
Seule revue scientifique francophone dédiée exclusivement à la recherche sur la radio et le son (sciences de l'information et de la communication).

**Point d’accès recommandé :**  
RSS / OpenEdition Journals / OAI-PMH.

**Pages officielles consultées :**
- https://journals.openedition.org/radiomorphoses/
- documentation OAI-PMH OpenEdition

**Constats juridiques et techniques :**
- Revue ouverte hébergée sur la plateforme publique OpenEdition.
- Notices normalisées interopérables.

**Collecte privée autorisée ou raisonnable :**
- notices Dublin Core
- titre
- auteurs
- date
- DOI
- résumés académiques

**Affichage public recommandé :**
- métadonnées bibliographiques minimales

**Champs interdits en public :**
- PDF
- HTML intégral des articles

**Attribution minimale :**  
`Source: Radiomorphoses — OpenEdition Journals — lien vers la notice originale.`

**Rate limit / conditions techniques :**  
Moissonnage via OAI-PMH, cadence académique normale.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : revue francophone phare en radio studies
- notes d’implémentation : `meta_only: true`

### Radio Fañch

**Statut recommandé :**  
VALIDÉ STRICT

**Famille :**  
blog / site historique indépendant

**Pertinence pour l’antenne :**  
Mémoire et histoire des radios libres en Bretagne, archives rares de la bande FM bretonne.

**Point d’accès recommandé :**  
HTML / RSS si disponible.

**Pages officielles consultées :**
- blogs et pages historiques de Radio Fañch

**Constats juridiques et techniques :**
- Site personnel à vocation patrimoniale.
- Ne pas perturber l'hébergement par un crawling agressif.

**Collecte privée autorisée ou raisonnable :**
- titres
- URLs d'articles

**Affichage public recommandé :**
- liens seulement

**Champs interdits en public :**
- archives sonores
- images historiques numérisées
- textes complets

**Attribution minimale :**  
`Source: Radio Fañch — lien.`

**Rate limit / conditions techniques :**  
Classe prudente faible cadence, hebdomadaire ou manuelle.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : préservation de l'histoire locale de la FM libre
- notes d’implémentation : `manual_curation: true`

### Les Radios Libres

**Statut recommandé :**  
VALIDÉ STRICT

**Famille :**  
blog / site historique

**Pertinence pour l’antenne :**  
Fonds documentaires et historiques précieux sur le mouvement français des radios libres (1977-1981).

**Point d’accès recommandé :**  
HTML / RSS si disponible.

**Pages officielles consultées :**
- sites d'archives et blogs dédiés aux radios libres

**Constats juridiques et techniques :**
- Initiative militante et mémorielle.
- Collecte factuelle respectueuse.

**Collecte privée autorisée ou raisonnable :**
- titres
- URLs

**Affichage public recommandé :**
- liens seulement

**Champs interdits en public :**
- images d'archives
- enregistrements audio restaurés

**Attribution minimale :**  
`Source: Les Radios Libres — lien.`

**Rate limit / conditions techniques :**  
Cadence manuelle ou quotidienne unique, cache local.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : archives indispensables sur le mouvement des radios libres
- notes d’implémentation : `meta_only: true`

### La Radio du Futur

**Statut recommandé :**  
VALIDÉ STRICT

**Famille :**  
blog / site professionnel

**Pertinence pour l’antenne :**  
Veille technologique sur le DAB+, la radio numérique, les applications mobiles et le futur du médium.

**Point d’accès recommandé :**  
HTML / RSS si disponible.

**Pages officielles consultées :**
- site La Radio du Futur
- flux RSS publics

**Constats juridiques et techniques :**
- Site d'actualité professionnelle et d'analyse.
- Protection standard du droit d'auteur.

**Collecte privée autorisée ou raisonnable :**
- titres
- URLs
- dates de publication

**Affichage public recommandé :**
- liens seulement

**Champs interdits en public :**
- analyses rédigées exclusives
- images professionnelles

**Attribution minimale :**  
`Source: La Radio du Futur — lien.`

**Rate limit / conditions techniques :**  
Classe prudente faible cadence, cache strict de 24h.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : indispensable pour suivre l'évolution technologique de la radio (DAB+)
- notes d’implémentation : `curated_only: true`

### La Lettre Pro

**Statut recommandé :**  
VALIDÉ STRICT

**Famille :**  
presse professionnelle

**Pertinence pour l’antenne :**  
Actualité quotidienne des professionnels de la radio et des médias en France et en Europe.

**Point d’accès recommandé :**  
HTML / newsletter / pages.

**Pages officielles consultées :**
- https://www.lalettre.pro/
- flux de syndication de la publication

**Constats juridiques et techniques :**
- Contenus d'actualité pro, en partie sous abonnement.
- Ne jamais tenter de contourner un paywall ou de scraper massivement les brèves.

**Collecte privée autorisée ou raisonnable :**
- titres
- URLs publiques
- dates
- extraits courts de veille

**Affichage public recommandé :**
- liens seulement

**Champs interdits en public :**
- brèves entières
- articles payants
- images d'actualité

**Attribution minimale :**  
`Source: La Lettre Pro de la Radio — lien.`

**Rate limit / conditions techniques :**  
Classe prudente faible cadence, ingestion journalière minimale.

**Risques :**  
Modéré (si non respect de l'usage non commercial).

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : actualité professionnelle du secteur en temps réel
- notes d’implémentation : `rss_only: true`

### MeCCSA Radio & Audio Studies

**Statut recommandé :**  
VALIDÉ STRICT

**Famille :**  
réseau académique britannique

**Pertinence pour l’antenne :**  
Réseau majeur de chercheurs britanniques en radio studies, publication d'appels à communications et de colloques.

**Point d’accès recommandé :**  
pages / RSS.

**Pages officielles consultées :**
- pages du réseau MeCCSA Radio & Audio Studies

**Constats juridiques et techniques :**
- Site académique d'association professionnelle.
- Signalement de travaux universitaires encouragé.

**Collecte privée autorisée ou raisonnable :**
- titres
- URLs d'appels ou d'événements
- dates

**Affichage public recommandé :**
- liens + métadonnées minimales

**Champs interdits en public :**
- résumés longs de colloques
- rapports internes

**Attribution minimale :**  
`Source: MeCCSA Radio & Audio Studies — lien.`

**Rate limit / conditions techniques :**  
Classe académique normale.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : appels à communications de premier plan
- notes d’implémentation : `curated_only: true`

### Nieman Storyboard

**Statut recommandé :**  
VALIDÉ STRICT

**Famille :**  
site éditorial / académique (Harvard)

**Pertinence pour l’antenne :**  
Études détaillées sur le journalisme narratif, le documentaire sonore et l'écriture pour l'oreille.

**Point d’accès recommandé :**  
RSS / pages.

**Pages officielles consultées :**
- https://niemanstoryboard.org/
- flux RSS Nieman Foundation

**Constats juridiques et techniques :**
- Publication de prestige de la Fondation Nieman pour le Journalisme.
- Droit d'auteur s'appliquant aux analyses textuelles approfondies.

**Collecte privée autorisée ou raisonnable :**
- titres
- URLs
- dates
- résumés de veille

**Affichage public recommandé :**
- liens + métadonnées bibliographiques minimales

**Champs interdits en public :**
- études de cas rédigées
- analyses narratives complètes
- images

**Attribution minimale :**  
`Source: Nieman Storyboard — Harvard University — lien.`

**Rate limit / conditions techniques :**  
Classe prudente faible cadence, une fois par jour.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : référence mondiale de l'analyse narrative sonore et documentaire
- notes d’implémentation : `meta_only: true`

### Transom

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
site ressource / podcasting / création sonore

**Pertinence pour l’antenne :**  
Ressources de formation, manifestes esthétiques, essais sur la prise de son et la narration radio.

**Point d’accès recommandé :**  
RSS / pages.

**Pages officielles consultées :**
- https://transom.org/
- flux RSS et sitemaps

**Constats juridiques et techniques :**
- Site éducatif d'intérêt public.
- Protéger les guides de formation exclusifs rédigés par des ingénieurs et producteurs.

**Collecte privée autorisée ou raisonnable :**
- titres d'articles
- URLs
- dates
- auteurs

**Affichage public recommandé :**
- métadonnées strictes (liens et titres)

**Champs interdits en public :**
- guides de formation complets
- images techniques
- fichiers audio de démonstration

**Attribution minimale :**  
`Source: Transom.org — lien vers le guide ou l'article.`

**Rate limit / conditions techniques :**  
Classe prudente faible cadence.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : ressource internationale majeure pour la réalisation radiophonique
- notes d’implémentation : `curated_only: true`

### RadioDoc Review

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
revue académique / critique spécialisée

**Pertinence pour l’antenne :**  
Seule revue analysant spécifiquement le documentaire et la fiction radio de création sous un angle universitaire et critique.

**Point d’accès recommandé :**  
pages revue / RSS.

**Pages officielles consultées :**
- https://ro.uow.edu.au/rdr/
- notices de l'Université de Wollongong

**Constats juridiques et techniques :**
- Revue universitaire hébergée sur dépôt institutionnel ouvert.
- Ingestion propre encouragée pour le signalement.

**Collecte privée autorisée ou raisonnable :**
- métadonnées d'articles
- auteurs
- titre
- date

**Affichage public recommandé :**
- métadonnées bibliographiques minimales

**Champs interdits en public :**
- essais critiques complets
- PDF

**Attribution minimale :**  
`Source: RadioDoc Review — lien.`

**Rate limit / conditions techniques :**  
Classe académique normale.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : unique revue d'évaluation critique de documentaires radio
- notes d’implémentation : `meta_only: true`

### HAL

**Statut recommandé :**  
VALIDÉ

**Famille :**  
plateforme académique / OAI-PMH

**Pertinence pour l’antenne :**  
Dépôt institutionnel majeur pour la littérature scientifique francophone. Constitue le socle de la veille en sciences de l'information et de la communication concernant la radio.

**Point d’accès recommandé :**  
API REST (api.archives-ouvertes.fr/search/) ou OAI-PMH (api.archives-ouvertes.fr/oai/hal/).

**Pages officielles consultées :**
- https://api.archives-ouvertes.fr/docs/search
- https://api.archives-ouvertes.fr/docs/oai
- https://about.hal.science/en/principles/

**Constats juridiques et techniques :**
- L'infrastructure OAI garantit une interopérabilité totale, sans nécessité d'inscription.
- L'exploitation commerciale des métadonnées extraites est prohibée, mais l'usage académique et d'indexation est encouragé.

**Collecte privée autorisée ou raisonnable :**
- Métadonnées bibliographiques intégrales
- identifiants auteurs (idHAL)
- résumés
- affiliations

**Affichage public recommandé :**
- title
- doi
- URL canonique HAL
- auteurs
- date de publication
- type de document

**Champs interdits en public :**
- Abstracts complets (en raison des droits résiduels éventuels des éditeurs initiaux)
- texte intégral des dépôts PDF

**Attribution minimale :**  
`Source: HAL (Archives Ouvertes) — lien vers la notice originale.`

**Rate limit / conditions techniques :**  
Pagination obligatoire (limite de 10 000 résultats via paramètre rows). Cadence d'une requête par seconde recommandée.

**Risques :**  
Faible. Source institutionnelle conçue pour le partage ouvert.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : Source francophone incontournable, fiable et ouverte.
- notes d’implémentation : Privilégier le moissonnage par collections spécifiques ou requêtes disciplinaires via l'API SolR.

### Crossref

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
API / agence d'enregistrement DOI

**Pertinence pour l’antenne :**  
Standard d'identification des publications académiques mondiales. Indispensable pour la résolution et l'enrichissement bibliographique.

**Point d’accès recommandé :**  
API REST (api.crossref.org).

**Pages officielles consultées :**
- https://www.crossref.org/documentation/retrieve-metadata/
- https://www.crossref.org/blog/announcing-changes-to-rest-api-rate-limits/

**Constats juridiques et techniques :**
- Les métadonnées sont librement accessibles à la communauté scientifique.
- Les informations de licence y sont structurées, permettant de vérifier les conditions de réutilisation.

**Collecte privée autorisée ou raisonnable :**
- Métadonnées complètes liées aux identifiants DOI

**Affichage public recommandé :**
- title
- URL (via résolveur doi.org)
- date de publication
- revue d'accueil
- DOI

Dans l'implémentation actuelle de l'antenne, l'export public reste encore plus strict : pas d'auteurs, pas de tags, pas d'abstracts et aucun dump brut Crossref. Les auteurs et sujets Crossref peuvent rester en privé dans `db.json` pour la curation et l'export Zotero manuel.

**Champs interdits en public :**
- Réponses API brutes
- abstracts
- auteurs
- tags
- scores et explications de score

**Attribution minimale :**  
`Source: Crossref — lien DOI.`

**Rate limit / conditions techniques :**  
L'accès au Polite Pool exige la transmission d'une adresse email valide via le paramètre mailto= ou l'en-tête User-Agent.

**Risques :**  
Faible. Organisation à but non lucratif d'intérêt public.

**Décision pratique pour `sources.yaml` :**
- `active: true`, avec `mailto_env: CROSSREF_MAILTO`.
- raison : Données bibliographiques de référence absolue.
- notes d’implémentation : Configuration obligatoire du paramètre mailto pour la courtoisie réseau, limite basse `rows: 20`, une seule famille de revue au démarrage, et aucun appel réseau si le mailto local manque.

### OpenAlex

**Statut recommandé :**  
VALIDÉ PRUDENT, DÉSACTIVÉ PAR DÉFAUT

**Famille :**  
catalogue académique global / API

**Pertinence pour l’antenne :**  
Graphe de connaissances académique ouvert, utile pour compléter Crossref et HAL sur les radio studies, sound studies, podcast studies et media studies. Sa largeur impose toutefois une entrée très bornée : OpenAlex peut améliorer la couverture, mais peut aussi ramener massivement du bruit technique autour du mot "radio".

**Point d’accès recommandé :**  
API REST Works (`https://api.openalex.org/works`).

**Pages officielles consultées :**
- https://developers.openalex.org/api-reference/authentication
- https://developers.openalex.org/api-reference/works/list-works
- https://developers.openalex.org/guides/searching
- https://developers.openalex.org/guides/selecting-fields
- https://developers.openalex.org/api-reference/works/get-a-single-work

**Constats juridiques et techniques :**
- L'ensemble des données est placé sous licence CC0 (domaine public).
- La documentation actuelle exige une clé API gratuite pour les appels API ; elle doit rester locale via `OPENALEX_API_KEY` si elle est utilisée.
- Le projet exige aussi une identification polie locale via `OPENALEX_MAILTO`. Aucune adresse personnelle ne doit être inscrite dans Git, les logs publics ou les artefacts Hugo.
- Les recherches Works portent sur `title`, `abstract` et `fulltext`; les résultats de recherche incluent un `relevance_score` OpenAlex privé, utile au tri mais interdit en public.
- Le champ `abstract_inverted_index` encode l'abstract sous forme d'index inversé ; OpenAlex ne fournit pas d'abstract en clair pour des raisons juridiques. Le projet ne doit ni le sélectionner pour le premier connecteur, ni le reconstruire, ni le publier.

**Collecte privée autorisée ou raisonnable :**
- métadonnées minimales de Works : `id`, `doi`, `title`/`display_name`, `publication_date`, `publication_year`, `type`, `language`, `ids` ;
- métadonnées de source strictement utiles : `primary_location.source.display_name`, DOI ou landing page, sans PDF public ;
- signaux de tri privés : `topics`, `primary_topic`, `keywords`, `relevance_score` ;
- dump brut local strictement privé dans `data/raw/openalex_latest.json`, jamais publié.

**Affichage public recommandé :**
- title
- doi
- URL
- date de publication
- source_name

Dans l'implémentation actuelle de l'antenne, l'export public reste plus strict encore : pas d'auteurs, pas de tags/concepts/keywords OpenAlex, pas de score de pertinence, pas d'abstract, pas de raw dump.

**Champs interdits en public :**
- `abstract_inverted_index`
- abstract reconstruit
- réponses API brutes
- auteurs et affiliations
- topics, concepts, keywords, tags
- `relevance_score` OpenAlex et score interne de l'antenne
- PDF, fulltext, `content_url`, `has_content`, `locations`
- logs, chemins locaux, secrets, `OPENALEX_MAILTO`, `OPENALEX_API_KEY`

**Attribution minimale :**  
`Source: OpenAlex — lien vers le DOI ou la notice.`

**Rate limit / conditions techniques :**  
Clé API gratuite locale pour l'usage courant, identification polie locale, `per_page` borné à 20 pour la recette initiale, 1 page maximum par profil, délai local d'au moins 1 seconde entre profils, backoff sur `429`/`5xx`, et lecture des en-têtes `X-RateLimit-*` si disponibles. Les limites OpenAlex documentées permettent davantage, mais l'antenne choisit volontairement moins pour éviter le bruit.

**Risques :**  
Juridique faible pour les métadonnées CC0, mais risque documentaire élevé si les requêtes ne filtrent pas le bruit technique.

**Décision pratique pour `sources.yaml` :**
- `enabled: false` jusqu'à recette live inspectée.
- raison : complément académique utile, mais seulement par profils ciblés.
- structure retenue : section `openalex` dans `config/sources.yaml`, plutôt qu'un nouveau fichier, car la configuration reste lisible et tient dans le même registre que HAL et Crossref.
- profils initiaux : `radio_studies`, `radio_audio_media`, `sound_studies`, `podcast_studies`, `community_free_radio`.
- exclusions obligatoires : `radio frequency`, `radiofrequency`, `radiotherapy`, `radioactive`, `radio telescope`, `radio astronomy`, `electromagnetic radiation`, `cognitive radio`, `spectrum sensing`, `beamforming`, `MIMO`, `5G`, `6G`.
- notes d’implémentation : ne pas lancer le réseau sans `OPENALEX_MAILTO` local ; utiliser `OPENALEX_API_KEY` local si l'API l'exige ; ne pas sélectionner `abstract_inverted_index` ; ne pas reconstruire d'abstract ; garder `relevance_score` strictement privé.

### CiNii

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
plateforme académique japonaise (NII)

**Pertinence pour l’antenne :**  
Recherche académique japonaise sur la Mini-FM, Tetsuo Kogawa et l'histoire des micro-radios japonaises.

**Point d’accès recommandé :**  
API REST ou RDF.

**Pages officielles consultées :**
- https://support.nii.ac.jp/en/cinii/copyright
- https://labs.ci.nii.ac.jp/en/termsofuse.html

**Constats juridiques et techniques :**
- Le service est gratuit et régi par le droit japonais.
- Les conditions d'utilisation (Linking Policy) exigent qu'il soit clairement indiqué que le service est fourni par le NII.

**Collecte privée autorisée ou raisonnable :**
- recherche bibliographique
- identifiants

**Affichage public recommandé :**
- title
- original_url
- authors
- source_name

**Champs interdits en public :**
- Dumps massifs

**Attribution minimale :**  
`Source: CiNii Research (National Institute of Informatics) — lien.`

**Rate limit / conditions techniques :**  
Cache obligatoire, 1 requête par seconde maximum pour éviter de surcharger les serveurs de l'institut.

**Risques :**  
Faible. API documentée pour un accès international.

**Décision pratique pour `sources.yaml` :**
- reporté V4 japonaise ; aucune entrée CiNii ne doit être ajoutée à `sources.yaml` en V3.
- raison : recherche pionnière sur la mini-FM japonaise indispensable à la cartographie, mais nécessite un audit dédié de langue, API, attribution NII, encodage, rate limit et contrat public.
- notes d’implémentation V4 : respecter scrupuleusement la clause d'attribution contractuelle au NII, démarrer par métadonnées minimales et conserver les abstracts/rich data hors export public.

### NDL

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
catalogue de bibliothèque nationale japonaise

**Pertinence pour l’antenne :**  
Ouvrages, périodiques et thèses japonais sur la Mini-FM, les radios communautaires et Kogawa.

**Point d’accès recommandé :**  
NDL Search API / SRU.

**Pages officielles consultées :**
- https://ndlsearch.ndl.go.jp/en/help/api/provider

**Constats juridiques et techniques :**
- Données institutionnelles ouvertes à des fins de signalement et de découverte.
- Formats structurés robustes (JSON/XML).

**Collecte privée autorisée ou raisonnable :**
- notices bibliographiques au format JSON/XML

**Affichage public recommandé :**
- title
- original_url
- published_at
- source_name

**Champs interdits en public :**
- Dumps bruts

**Attribution minimale :**  
`Source: National Diet Library — Japan — lien.`

**Rate limit / conditions techniques :**  
Cadence modérée, cache local obligatoire.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- reporté V4 japonaise ; aucune entrée NDL ne doit être ajoutée à `sources.yaml` en V3.
- raison : ressources nationales japonaises exhaustives et officielles, mais audit SRU/API, notices, translittération et attribution à faire dans une conversation séparée.
- notes d’implémentation V4 : `sru_xml_parsing: true`, cache local, cadence modérée, métadonnées minimales seulement en public.

### J-STAGE

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
portail de revues académiques japonaises

**Pertinence pour l’antenne :**  
Articles académiques en libre accès sur l'esthétique et l'histoire des médias sonores au Japon.

**Point d’accès recommandé :**  
API REST ou RSS par revue.

**Pages officielles consultées :**
- sites d'aide aux développeurs J-STAGE

**Constats juridiques et techniques :**
- Portail national favorisant l'Open Access en recherche académique.
- Données interopérables.

**Collecte privée autorisée ou raisonnable :**
- métadonnées et liens

**Affichage public recommandé :**
- title
- original_url
- published_at
- authors
- source_name

**Champs interdits en public :**
- PDF intégraux

**Attribution minimale :**  
`Source: J-STAGE — Japan — lien.`

**Rate limit / conditions techniques :**  
Cadence académique normale.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- reporté V4 japonaise ; aucune entrée J-STAGE ne doit être ajoutée à `sources.yaml` en V3.
- raison : accès ouvert aux publications scientifiques japonaises, mais la sélection de revues, l'API/RSS disponible et les conditions de réutilisation doivent être auditées avant implémentation.
- notes d’implémentation V4 : `meta_only: true`, aucune récupération PDF, aucun abstract public, scan anti-fuite obligatoire.

### Cairn

**Statut recommandé :**  
VALIDÉ STRICT

**Famille :**  
plateforme éditoriale commerciale

**Pertinence pour l’antenne :**  
Littérature francophone majeure en sciences humaines, sociologie des médias et sciences de l'information et de la communication.

**Point d’accès recommandé :**  
OAI-PMH ou via DOI (Crossref).

**Pages officielles consultées :**
- https://droit.cairn.info/revue-dpo-news-2025-3-page-7?lang=fr

**Constats juridiques et techniques :**
- Cairn dispose de conditions d'utilisation très strictes protégeant son catalogue.
- Aspiration web directe (BeautifulSoup/Selenium) strictement bannie par les CGU de Cairn sous peine de poursuites.

**Collecte privée autorisée ou raisonnable :**
- métadonnées minimales (titres, auteurs, revue, date, liens, DOI) obtenues via Crossref ou OAI public

**Affichage public recommandé :**
- title
- auteurs
- revue
- date
- liens vers l'URL officielle (évitant tout paywall)

**Champs interdits en public :**
- abstracts (protégés)
- textes intégraux
- PDF
- scraping HTML direct

**Attribution minimale :**  
`Source: Cairn.info — lien.`

**Rate limit / conditions techniques :**  
Bannir le crawling direct ; enrichissement indirect par Crossref / OpenAlex.

**Risques :**  
Élevé en cas de scraping direct, nul en cas de résolution par Crossref/OAI-PMH.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : incontournable pour la recherche francophone
- notes d’implémentation : `crossref_lookup_only: true`

### Persée

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
portail académique ouvert

**Pertinence pour l’antenne :**  
Patrimoine scientifique de la recherche SHS francophone sur l'histoire de la radio et des médias.

**Point d’accès recommandé :**  
OAI-PMH ou API.

**Pages officielles consultées :**
- https://info.persee.fr/fouille-de-donnees/

**Constats juridiques et techniques :**
- Portail ouvert d'intérêt public.
- Fouille de texte massive requiert une concertation, mais l'indexation de métadonnées est libre.

**Collecte privée autorisée ou raisonnable :**
- notices bibliographiques complètes
- auteurs
- titre
- date

**Affichage public recommandé :**
- title
- original_url
- published_at
- authors
- source_name

**Champs interdits en public :**
- texte intégral

**Attribution minimale :**  
`Source: Persée — UAR Persée — lien.`

**Rate limit / conditions techniques :**  
Respect de l'OAI-PMH standard.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : archives SHS ouvertes d'une immense valeur historique
- notes d’implémentation : `meta_only: true`

### OpenEdition Books

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
livres académiques ouverts

**Pertinence pour l’antenne :**  
Monographies universitaires francophones en sound studies, sciences sociales et sciences de la communication.

**Point d’accès recommandé :**  
OAI-PMH ou RSS.

**Pages officielles consultées :**
- documentation OAI-PMH OpenEdition Books

**Constats juridiques et techniques :**
- Métadonnées normalisées et interopérables.
- Accès ouvert sélectif selon les éditeurs.

**Collecte privée autorisée ou raisonnable :**
- notices de livres
- auteurs
- titre
- date

**Affichage public recommandé :**
- title
- original_url
- published_at
- authors
- source_name

**Champs interdits en public :**
- Chapitres entiers
- PDF

**Attribution minimale :**  
`Source: OpenEdition Books — lien.`

**Rate limit / conditions techniques :**  
Cadence normale.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : monographies universitaires de premier plan
- notes d’implémentation : `meta_only: true`

### OpenEdition Journals

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
revues académiques ouvertes

**Pertinence pour l’antenne :**  
Revues scientifiques majeures en sound studies, culture visuelle et théories des communications.

**Point d’accès recommandé :**  
OAI-PMH ou RSS.

**Pages officielles consultées :**
- https://oai-openedition.readthedocs.io/

**Constats juridiques et techniques :**
- Ingestion propre via OAI-PMH v2 (Dublin Core et formats MODS).
- Respect du droit d'auteur.

**Collecte privée autorisée ou raisonnable :**
- notices d'articles
- auteurs
- titre
- date

**Affichage public recommandé :**
- title
- original_url
- published_at
- authors
- source_name

**Champs interdits en public :**
- PDF
- HTML complet des articles

**Attribution minimale :**  
`Source: OpenEdition Journals — lien.`

**Rate limit / conditions techniques :**  
Respect des endpoints OAI-PMH.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : portail majeur de l'Open Access francophone
- notes d’implémentation : `meta_only: true`

### Érudit

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
plateforme académique

**Pertinence pour l’antenne :**  
Littérature académique nord-américaine (Canada/Québec) francophone sur les médias, la culture et la communication.

**Point d’accès recommandé :**  
notices et métadonnées ; DOI si présent.

**Pages officielles consultées :**
- https://apropos.erudit.org/technologies/?lang=en

**Constats juridiques et techniques :**
- Érudit maintient un entrepôt OAI-PMH public (formats OAI-DC et NLM) pour la collecte.
- Stratégie identique à Persée.

**Collecte privée autorisée ou raisonnable :**
- métadonnées
- DOI
- auteurs
- date
- revue

**Affichage public recommandé :**
- métadonnées bibliographiques minimales

**Champs interdits en public :**
- textes complets
- PDF
- HTML
- dumps bruts

**Attribution minimale :**  
`Source: Érudit — lien vers la notice originale.`

**Rate limit / conditions techniques :**  
Cadence modérée ; enrichissement par DOI.

**Risques :**  
Faible à modéré.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : élargit le corpus francophone universitaire outre-Atlantique
- notes d’implémentation : `meta_only: true`

### DOAJ

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
API / index de revues open access

**Pertinence pour l’antenne :**  
Identifier et filtrer les publications open access de haute qualité dans le domaine des sound studies.

**Point d’accès recommandé :**  
API REST (doaj.org/api/).

**Pages officielles consultées :**
- https://docs.pkp.sfu.ca/doaj/en/
- https://blog.doaj.org/2025/06/15/how-i-use-doaj-metadata-in-my-work-and-research/

**Constats juridiques et techniques :**
- Le DOAJ milite pour l'accès ouvert libre (Libre Open Access) et répertorie des métadonnées gratuites.
- L'API limite généralement les résultats à 1000 notices par recherche pour préserver la base de données.

**Collecte privée autorisée ou raisonnable :**
- métadonnées des journaux et des articles

**Affichage public recommandé :**
- liens
- titres
- informations de licence

**Champs interdits en public :**
- Dumps complets

**Attribution minimale :**  
`Source: DOAJ — lien.`

**Rate limit / conditions techniques :**  
Pagination obligatoire ; cadence modérée de rigueur pour soulager l'infrastructure.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : validation fiable du statut Open Access des ressources
- notes d’implémentation : `limit_results_1000: true`

### WorldCat

**Statut recommandé :**  
À REPORTER

**Famille :**  
catalogue coopératif mondial

**Pertinence pour l’antenne :**  
Recensement universel des monographies et ouvrages imprimés sur l'histoire de la radio et les études sonores.

**Point d’accès recommandé :**  
Aucun accès automatisé pour ce projet (CGU de WorldCat hautement restrictives).

**Pages officielles consultées :**
- https://www.oclc.org/content/dam/ext-ref/worldcat-org/terms.html
- https://www.oclc.org/developer/api/oclc-apis/worldcat-search-api.en.html

**Constats juridiques et techniques :**
- Les Conditions d'Utilisation de WorldCat.org interdisent de manière absolue l'extraction automatisée (bots, scraping), le stockage à long terme, et la republication des données.
- L'accès légitime à l'API de recherche nécessite de cumuler un abonnement institutionnel coûteux au catalogage complet d'OCLC, hors de portée d'un projet de veille autonome.

**Collecte privée autorisée ou raisonnable :**
- Consultation manuelle et saisie humaine dans Zotero uniquement.

**Affichage public recommandé :**
- Aucun

**Champs interdits en public :**
- Tous les champs
- identifiants (OCLC number)
- URLs

**Attribution minimale :**  
N/A

**Rate limit / conditions techniques :**  
Protections techniques anti-bots robustes et menaces d'action en justice explicites en cas de violation des systèmes de sécurité.

**Risques :**  
Critique. OCLC exerce un contrôle monopolistique reconnu sur ses métadonnées et protège farouchement ses droits.

**Décision pratique pour `sources.yaml` :**
- `active: false`
- raison : Incompatibilité juridique fondamentale avec le concept d'agrégation automatisée.
- notes d’implémentation : Remplacer ce manque par la consultation d'archives ouvertes européennes ou nationales (Sudoc, BnF, HAL, OpenAlex) dont la gouvernance favorise la découvrabilité.

### Library of Congress

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
bibliothèque nationale et archives

**Pertinence pour l’antenne :**  
Notices bibliographiques historiques sur la radio américaine et collections de radiodiffusion.

**Point d’accès recommandé :**  
LoC Search API (JSON).

**Pages officielles consultées :**
- https://libraryofcongress.github.io/data-exploration/

**Constats juridiques et techniques :**
- Source de données publiques gouvernementales stables et ouvertes.
- Grand volume de ressources documentaires d'intérêt historique.

**Collecte privée autorisée ou raisonnable :**
- notices d'ouvrages
- collections
- dates
- identifiants

**Affichage public recommandé :**
- title
- original_url
- published_at
- source_name

**Champs interdits en public :**
- Dumps complets MARC/XML

**Attribution minimale :**  
`Source: Library of Congress — lien.`

**Rate limit / conditions techniques :**  
Limitation d'appels modérée, cache strict.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : Source de référence bibliographique stable, ouverte et institutionnelle
- notes d’implémentation : `use_json_api: true`

### BnF / Gallica

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
catalogue institutionnel et archives numériques

**Pertinence pour l’antenne :**  
Indispensable pour l'histoire des débuts de la radio, de la TSF, et la numérisation des revues historiques.

**Point d’accès recommandé :**  
Entrepôts OAI-PMH (OAI-NUM pour les documents numérisés, OAI-CAT pour le catalogue).

**Pages officielles consultées :**
- https://api.bnf.fr/fr/oai-num
- https://www.bnf.fr/fr/recuperer-des-notices-bibliographiques-en-dublin-core-oai-cat

**Constats juridiques et techniques :**
- Les métadonnées sont libérées sous la "Licence Ouverte" de l'État, autorisant la libre réutilisation sous condition de mention de source.
- Le protocole OAI-PMH est documenté et structuré.

**Collecte privée autorisée ou raisonnable :**
- métadonnées
- identifiants pérennes (ARK)
- récupération du texte brut OCRisé via l'API Document (/{ark}.texteBrut) pour analyse locale

**Affichage public recommandé :**
- titres
- dates
- auteurs
- format
- liens de résolution ARK

**Champs interdits en public :**
- La republication du texte intégral OCRisé sans contextualisation

**Attribution minimale :**  
`Source: Bibliothèque nationale de France / Gallica — lien ARK.`

**Rate limit / conditions techniques :**  
Exploitation asynchrone par sets OAI.

**Risques :**  
Très faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : Stabilité des identifiants (ARK) et politique de données publique irréprochable.
- notes d’implémentation : Convertir le modèle Dublin Core pour correspondre au format JSON interne.

### Sudoc / Abes

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
catalogue académique / OAI-PMH

**Pertinence pour l’antenne :**  
Localisation d'ouvrages physiques majeurs et de thèses en études radiophoniques dans le réseau universitaire français.

**Point d’accès recommandé :**  
OAI-PMH.

**Pages officielles consultées :**
- https://documentation.abes.fr/aidesudoc/EN/accueil/aidesudoc_index.html
- https://documentation.abes.fr/aideidref/accueil/en/index.html

**Constats juridiques et techniques :**
- Le système propose un dépôt OAI-PMH et des services web (IdRef) ouverts sous Licence Ouverte.
- Idéal pour résoudre des autorités.

**Collecte privée autorisée ou raisonnable :**
- notices bibliographiques
- ISBN
- localisation

**Affichage public recommandé :**
- liens de localisation
- titres
- auteurs

**Champs interdits en public :**
- Dumps bruts MARC/XML

**Attribution minimale :**  
`Source: Catalogue Sudoc / Abes — lien.`

**Rate limit / conditions techniques :**  
Traitement OAI-PMH standard.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : Utile pour référencer et localiser des monographies clés introuvables en ligne.
- notes d’implémentation : Extraction ciblée via ISBN ou IdRef.

### theses.fr

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
catalogue académique

**Pertinence pour l’antenne :**  
Suivi des thèses de doctorat soutenues ou en préparation sur l'esthétique et l'histoire des médias radiophoniques en France.

**Point d’accès recommandé :**  
API Export des données via data.gouv.fr ou OAI-PMH.

**Pages officielles consultées :**
- https://www.data.gouv.fr/dataservices/api-export-des-donnees-de-theses-fr

**Constats juridiques et techniques :**
- Base de données publique gérée par l'Abes, distribuée en Open Data.
- API stable.

**Collecte privée autorisée ou raisonnable :**
- notices de thèses complètes
- informations sur les jurys et directeurs de recherche

**Affichage public recommandé :**
- titre de la thèse
- auteur
- date de soutenance
- URL vers la notice officielle

**Champs interdits en public :**
- Résumés longs si non explicitement sous licence libre

**Attribution minimale :**  
`Source: theses.fr / Abes — lien.`

**Rate limit / conditions techniques :**  
Accès standard via les endpoints data.gouv.fr.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : Exhaustivité sur la jeune recherche académique française.
- notes d’implémentation : Aucun obstacle technique majeur.

### Isidore

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
moteur de recherche académique SHS

**Pertinence pour l’antenne :**  
Découverte de publications, carnets de recherche (Hypothèses.org) et communications sur les sound studies.

**Point d’accès recommandé :**  
API publique ISIDORE (Huma-Num).

**Pages officielles consultées :**
- https://isidore.science/cgu
- https://documentation.huma-num.fr/en/isidore-en/

**Constats juridiques et techniques :**
- Infrastructure nationale gérée par l'UAR Huma-Num.
- Respect rigoureux du RGPD et diffusion de données de signalement.

**Collecte privée autorisée ou raisonnable :**
- résultats de recherche sémantique
- métadonnées enrichies
- tags

**Affichage public recommandé :**
- liens
- titres
- auteurs
- disciplines

**Champs interdits en public :**
- Texte intégral des documents
- annotations sémantiques propriétaires du moteur

**Attribution minimale :**  
`Source: ISIDORE (Huma-Num) — lien.`

**Rate limit / conditions techniques :**  
API publique accessible (via système de laisser-passer). Cadence de requête courtoise.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : Outil de découverte sémantique SHS incomparable.
- notes d’implémentation : S'assurer du bon routage vers l'URL canonique d'origine découverte plutôt que la seule notice Isidore.

### ORCID

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
registre d'auteurs académiques

**Pertinence pour l’antenne :**  
Désambiguïsation des auteurs et suivi des contributions des principaux chercheurs en radio studies.

**Point d’accès recommandé :**  
API publique ORCID.

**Pages officielles consultées :**
- https://info.orcid.org/orcid-public-api/

**Constats juridiques et techniques :**
- API publique ouverte conçue pour la découvrabilité des profils des chercheurs.
- Conformité RGPD assurée par le contrôle individuel des chercheurs sur la visibilité de leurs données.

**Collecte privée autorisée ou raisonnable :**
- Identifiants ORCID
- listes de publications publiques

**Affichage public recommandé :**
- Lien vers le profil ORCID public du chercheur

**Champs interdits en public :**
- Données biographiques marquées privées

**Attribution minimale :**  
`Source: ORCID — lien.`

**Rate limit / conditions techniques :**  
Requiert l'enregistrement d'une clé API publique gratuite. Limites courtoises à respecter.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : standard mondial de l'identité universitaire des chercheurs
- notes d’implémentation : `use_public_api: true`

### Unpaywall

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
API / résolveur Open Access

**Pertinence pour l’antenne :**  
Assurer que les lecteurs de l'antenne accèdent aux versions libres et gratuites (Green/Gold Open Access) des articles payants.

**Point d’accès recommandé :**  
REST API (api.unpaywall.org/v2/).

**Pages officielles consultées :**
- https://unpaywall.org/products/api
- https://docs.ropensci.org/roadoi/

**Constats juridiques et techniques :**
- API ouverte et d'utilité publique.
- Exige obligatoirement une adresse email de contact dans les requêtes pour l'identification.

**Collecte privée autorisée ou raisonnable :**
- Statut OA
- liens vers les PDF légaux des articles correspondants aux DOI

**Affichage public recommandé :**
- Statut "Open Access" (vrai/faux) et lien direct vers la version libre (PDF legal)

**Champs interdits en public :**
- Adresse email ayant servi à la requête (à cacher dans les variables d'environnement)

**Attribution minimale :**  
`Source: Unpaywall — lien.`

**Rate limit / conditions techniques :**  
Limite courtoise de 100 000 appels quotidiens.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : Maximise l'accès libre et légal aux publications scientifiques indexées.
- notes d’implémentation : Configurer de manière confidentielle l'email d'identification dans le script.

### Europeana

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
catalogue du patrimoine culturel / API

**Pertinence pour l’antenne :**  
Accès à des fonds iconographiques, notices d'anciennes radios et documents d'histoire des médias à l'échelle européenne.

**Point d’accès recommandé :**  
Search API et Record API (api.europeana.eu).

**Pages officielles consultées :**
- https://europeana.atlassian.net/wiki/spaces/EF/pages/2360508417
- https://www.europeana.eu/en/rights/terms-of-use

**Constats juridiques et techniques :**
- Accès gratuit requérant une clé d'API.
- Europeana agrège des notices d'institutions diverses ; vérifier les Rights Statements (conditions de droits) de chaque item.

**Collecte privée autorisée ou raisonnable :**
- métadonnées patrimoniales
- informations d'origine
- miniatures d'illustration si autorisées

**Affichage public recommandé :**
- title
- URL (vers europeana.eu)
- institution d'origine
- statut légal (ex: Public Domain)

**Champs interdits en public :**
- Intégration de médias soumis à des licences restrictives (droits d'auteur non éteints)

**Attribution minimale :**  
`Source: Europeana — fourni par [Institution] — lien.`

**Rate limit / conditions techniques :**  
Limites d'appel standards par clé API.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : Découverte de matériaux d'archives visuelles et textuelles exceptionnels
- notes d’implémentation : Mapper systématiquement le champ des droits (Rights Statement) pour vérification.

### Internet Archive

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
bibliothèque numérique d'archives

**Pertinence pour l’antenne :**  
Accès à d'immenses collections d'émissions de radio historiques numérisées du domaine public, manuels de TSF et revues techniques anciennes.

**Point d’accès recommandé :**  
Internet Archive Metadata API.

**Pages officielles consultées :**
- https://archive.org/developers/

**Constats juridiques et techniques :**
- Bien que l'institution traverse des litiges sur le prêt numérique de livres sous droits, ses API de métadonnées pour les fonds audio du domaine public restent ouvertes et légales.
- API stable en JSON.

**Collecte privée autorisée ou raisonnable :**
- notices et métadonnées d'items
- résumés de description publique

**Affichage public recommandé :**
- title
- original_url
- published_at
- source_name

**Champs interdits en public :**
- Republication ou intégration de médias volumineux directement sur notre site (risque de surcharge et de droits d'auteur complexes)

**Attribution minimale :**  
`Source: Internet Archive — lien vers l'item.`

**Rate limit / conditions techniques :**  
Cadence modérée, cache local obligatoire.

**Risques :**  
Faible à modéré.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : archives sonores historiques mondiales irremplaçables
- notes d’implémentation : `meta_only: true`

### INA

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
archives audiovisuelles institutionnelles

**Pertinence pour l’antenne :**  
Gisement unique et historique de la radiodiffusion française.

**Point d’accès recommandé :**  
Plateforme data.gouv.fr pour les métadonnées ouvertes.

**Pages officielles consultées :**
- https://www.data.gouv.fr/organizations/institut-national-de-laudiovisuel

**Constats juridiques et techniques :**
- L'INA diffuse publiquement des jeux de données de métadonnées (ex: Podcasts français archivés) sur le portail Open Data de l'État sous Licence Ouverte.
- Le scraping sauvage de ina.fr grand public est formellement interdit et passible de poursuites.

**Collecte privée autorisée ou raisonnable :**
- Ingestion des jeux de métadonnées ouverts au format CSV/JSON

**Affichage public recommandé :**
- notices factuelles
- liens vers les notices publiques de ina.fr

**Champs interdits en public :**
- Aspiration ou intégration directe des lecteurs propriétaires ou de médias audio/vidéo

**Attribution minimale :**  
`Source: INA via data.gouv.fr — lien vers la notice.`

**Rate limit / conditions techniques :**  
Parser des exports statiques, aucun appel dynamique à ina.fr.

**Risques :**  
Modéré (nul en se cantonnant à l'Open Data).

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : Valorisation des archives et des notices de la radio publique française
- notes d’implémentation : `static_datasets_only: true`

### France Culture / Radio France

**Statut recommandé :**  
VALIDÉ STRICT

**Famille :**  
média de service public / Open API

**Pertinence pour l’antenne :**  
Acteur historique majeur de la création radiophonique et de la veille intellectuelle en langue française.

**Point d’accès recommandé :**  
Open API de Radio France (developers.radiofrance.fr).

**Pages officielles consultées :**
- https://www.radiofrance.com/lopen-api-radio-france
- https://www.radiofrance.com/conditions-generales-dutilisation-des-sites-de-radio-france

**Constats juridiques et techniques :**
- L'accès à l'Open API est gratuit mais strictement non commercial et nécessite la création d'un compte développeur.
- Il est strictement interdit d'utiliser l'API pour créer des agrégateurs audio alternatifs ou de contourner les lecteurs de Radio France.

**Collecte privée autorisée ou raisonnable :**
- grilles d'émissions
- titres
- tags
- producteurs
- URL des pages éditoriales d'émissions

**Affichage public recommandé :**
- title
- url (redirection vers le site de Radio France)
- date
- contributeurs

**Champs interdits en public :**
- Fichiers audio directs (.mp3/.aac)
- intégration de lecteurs audio non officiels
- transcriptions complètes

**Attribution minimale :**  
`Source: Radio France / France Culture — lien vers l'emission.`

**Rate limit / conditions techniques :**  
Limites d'appel fixées par la clé développeur accordée par Radio France.

**Risques :**  
Modéré (respect de l'interdiction de concurrence audio).

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : production culturelle et documentaire de référence mondiale
- notes d’implémentation : `no_audio_hotlink: true`

### ARTE Radio

**Statut recommandé :**  
VALIDÉ STRICT

**Famille :**  
création sonore de service public

**Pertinence pour l’antenne :**  
Pionnier historique du podcast natif francophone de création, documentaires et fictions sonores.

**Point d’accès recommandé :**  
Flux RSS public de syndication.

**Pages officielles consultées :**
- https://podcasts.apple.com/us/artist/arte-radio/1251092473

**Constats juridiques et techniques :**
- ARTE Radio diffuse largement ses notices via RSS pour le signalement.
- Propriété intellectuelle stricte sur les œuvres artistiques produites.

**Collecte privée autorisée ou raisonnable :**
- titres de podcasts
- créateurs
- dates
- durées
- résumés courts

**Affichage public recommandé :**
- title
- original_url (pointant vers arteradio.com)
- published_at
- source_name

**Champs interdits en public :**
- Fichiers audio originaux (.mp3)
- transcriptions complètes
- illustrations protégées

**Attribution minimale :**  
`Source: ARTE Radio — lien vers la notice d'origine.`

**Rate limit / conditions techniques :**  
Cadence quotidienne unique.

**Risques :**  
Faible à modéré.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : référence incontournable de la création sonore contemporaine
- notes d’implémentation : `rss_only: true`

### BBC Sounds

**Statut recommandé :**  
VALIDÉ STRICT

**Famille :**  
média de service public / RSS

**Pertinence pour l’antenne :**  
Programmation documentaire historique et sound studies de premier ordre international.

**Point d’accès recommandé :**  
RSS publics / pages d'émissions.

**Pages officielles consultées :**
- conditions de distribution de la BBC

**Constats juridiques et techniques :**
- Distribution ouverte pour la découverte, droits stricts sur le média.
- Les flux RSS sont stables.

**Collecte privée autorisée ou raisonnable :**
- titres de séries et épisodes
- dates de diffusion
- producteurs

**Affichage public recommandé :**
- title
- original_url (redirection vers bbc.co.uk)
- published_at
- source_name

**Champs interdits en public :**
- Flux audio direct
- transcriptions d'épisodes

**Attribution minimale :**  
`Source: BBC Sounds — lien.`

**Rate limit / conditions techniques :**  
Classe prudente faible cadence, cache strict de 24h.

**Risques :**  
Modéré (restrictions géographiques sur certains audios).

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : production documentaire de référence internationale
- notes d’implémentation : `rss_only: true`

### NPR

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
radio publique américaine

**Pertinence pour l’antenne :**  
Chroniques, documentaires radio de création et podcasts d'analyse sociale.

**Point d’accès recommandé :**  
RSS / API publique de syndication.

**Pages officielles consultées :**
- https://www.npr.org/about-npr/179876898/terms-of-use

**Constats juridiques et techniques :**
- L'utilisation des flux RSS et des métadonnées de NPR est autorisée uniquement pour un usage personnel et non commercial.
- Signalement sans reproduction des contenus.

**Collecte privée autorisée ou raisonnable :**
- notices de podcasts
- titres
- dates
- liens

**Affichage public recommandé :**
- title
- original_url (redirection vers npr.org)
- published_at
- source_name

**Champs interdits en public :**
- Audio MP3
- retranscriptions écrites complètes des émissions

**Attribution minimale :**  
`Source: NPR — lien.`

**Rate limit / conditions techniques :**  
Classe prudente faible cadence.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : journalisme audio américain de référence
- notes d’implémentation : `rss_only: true`

### Apple Podcasts

**Statut recommandé :**  
À REPORTER

**Famille :**  
annuaire commercial de podcasts

**Pertinence pour l’antenne :**  
Exhaustivité de l'index de diffusion pour le signalement de créations indépendantes.

**Point d’accès recommandé :**  
iTunes Search API (itunes.apple.com/search).

**Pages officielles consultées :**
- https://performance-partners.apple.com/search-api

**Constats juridiques et techniques :**
- API publique de recherche, mais avec des limites techniques agressives (environ 20 appels/minute).
- Inadapté comme source primaire stable d'indexation massive pour un projet universitaire.

**Collecte privée autorisée ou raisonnable :**
- métadonnées descriptives de podcasts
- identifiants

**Affichage public recommandé :**
- Aucun

**Champs interdits en public :**
- Tous les champs
- images d'illustrations (pas de hotlinking d'illustrations commerciales)

**Attribution minimale :**  
N/A

**Rate limit / conditions techniques :**  
Temporisation stricte de 3 secondes minimum par appel en cas d'utilisation.

**Risques :**  
Modéré (blocages d'adresses IP).

**Décision pratique pour `sources.yaml` :**
- `active: false`
- raison : source commerciale instable et redondante avec le Podcast Index
- notes d’implémentation : `manual_only: true`

### Spotify

**Statut recommandé :**  
À ÉVITER

**Famille :**  
plateforme commerciale fermée de streaming

**Pertinence pour l’antenne :**  
Nulle pour la recherche ouverte. Certains podcasts ou créations exclusives n'y sont hébergés que sous format propriétaire.

**Point d’accès recommandé :**  
Aucun.

**Pages officielles consultées :**
- https://developer.spotify.com/blog/2026-02-06-update-on-developer-access-and-platform-security
- https://developer.spotify.com/documentation/web-api/concepts/rate-limits

**Constats juridiques et techniques :**
- Spotify a radicalement verrouillé sa plateforme développeurs en février 2026. L'accès en mode développement y est bridé et nécessite une approbation commerciale impossible pour un projet indépendant.
- Rate limiting agressif.

**Collecte privée autorisée ou raisonnable :**
- Techniquement infaisable et juridiquement risqué.

**Affichage public recommandé :**
- Aucun

**Champs interdits en public :**
- Tous

**Attribution minimale :**  
N/A

**Rate limit / conditions techniques :**  
Politique hostile envers les initiatives universitaires autonomes.

**Risques :**  
Très élevé.

**Décision pratique pour `sources.yaml` :**
- `active: false`
- raison : Dépendance à un écosystème fermé hostile à l'Open Source universitaire.
- notes d’implémentation : `blocked: true`

### Deezer

**Statut recommandé :**  
À REPORTER

**Famille :**  
plateforme commerciale de streaming

**Pertinence pour l’antenne :**  
Faible. Redondance totale avec les flux ouverts et le Podcast Index.

**Point d’accès recommandé :**  
Aucun.

**Pages officielles consultées :**
- https://developers.deezer.com/termsofuse

**Constats juridiques et techniques :**
- Conditions d'utilisation excluant la constitution de bases de données parallèles.
- API restrictive.

**Collecte privée autorisée ou raisonnable :**
- Ingestion manuelle de complément uniquement.

**Affichage public recommandé :**
- Aucun

**Champs interdits en public :**
- Tous

**Attribution minimale :**  
N/A

**Rate limit / conditions techniques :**  
Non applicable.

**Risques :**  
Modéré.

**Décision pratique pour `sources.yaml` :**
- `active: false`
- raison : source commerciale sans valeur académique ajoutée
- notes d’implémentation : `manual_only: true`

### SoundCloud

**Statut recommandé :**  
À REPORTER

**Famille :**  
plateforme de distribution audio

**Pertinence pour l’antenne :**  
Hébergement de pièces rares de sound art et de créations d'indépendants.

**Point d’accès recommandé :**  
Aucun accès API direct.

**Pages officielles consultées :**
- conditions développeurs SoundCloud

**Constats juridiques et techniques :**
- La plateforme n'émet plus de clés API publiques pour les développeurs indépendants.
- Les flux RSS de profils restent lisibles.

**Collecte privée autorisée ou raisonnable :**
- Ingestion de flux RSS individuels de créateurs sonores

**Affichage public recommandé :**
- Aucun

**Champs interdits en public :**
- Tous

**Attribution minimale :**  
N/A

**Rate limit / conditions techniques :**  
Traitement manuel ou par RSS individuel.

**Risques :**  
Modéré.

**Décision pratique pour `sources.yaml` :**
- `active: false`
- raison : instabilité chronique de l'accès développeurs de la plateforme
- notes d’implémentation : `manual_only: true`

### Mixcloud

**Statut recommandé :**  
À ÉVITER

**Famille :**  
plateforme audio commerciale

**Pertinence pour l’antenne :**  
Archives d'émissions de radio associative ou de DJ sets.

**Point d’accès recommandé :**  
HTML scraping uniquement.

**Pages officielles consultées :**
- conditions de Mixcloud

**Constats juridiques et techniques :**
- Scraping banni par les conditions d'utilisation.
- Protections anti-bots actives sur le site.

**Collecte privée autorisée ou raisonnable :**
- Saisie manuelle Zotero uniquement.

**Affichage public recommandé :**
- Aucun

**Champs interdits en public :**
- Tous

**Attribution minimale :**  
N/A

**Rate limit / conditions techniques :**  
Éviter l'aspiration dynamique.

**Risques :**  
Élevé.

**Décision pratique pour `sources.yaml` :**
- `active: false`
- raison : CGU restrictives, absence d'accès ouvert structuré
- notes d’implémentation : `blocked: true`

### Podcast Index

**Statut recommandé :**  
VALIDÉ PRUDENT

**Famille :**  
annuaire ouvert / API communautaire

**Pertinence pour l’antenne :**  
Seul index mondial ouvert et indépendant, préservant la nature décentralisée du podcasting face aux plateformes fermées.

**Point d’accès recommandé :**  
API REST (doit être signée cryptographiquement).

**Pages officielles consultées :**
- https://podcastindex-org.github.io/docs-api/

**Constats juridiques et techniques :**
- Index open source et communautaire favorisant la découvrabilité libre.
- Le requêtage nécessite une clé d'API et une signature à base de hash (SHA-1) à chaque en-tête.

**Collecte privée autorisée ou raisonnable :**
- titres
- descriptions
- URL des flux RSS originaux
- identifiants techniques

**Affichage public recommandé :**
- `title`
- `original_url`
- `source_name`
- `published_at`

**Champs interdits en public :**
- fichiers MP3 originaux
- hotlinking d'illustrations d'épisodes

**Attribution minimale :**  
`Source: Podcast Index — lien.`

**Rate limit / conditions techniques :**  
User-Agent explicite requis. Gérer dynamiquement les codes d'erreur 429 et respecter les quotas accordés.

**Risques :**  
Faible.

**Décision pratique pour `sources.yaml` :**
- `active: true`
- raison : philosophie communautaire et ouverte en parfaite adéquation avec la recherche universitaire
- notes d’implémentation : Privilégier les recherches ciblées par mots-clés plutôt qu'un balayage généraliste.

## Sources recommandées à ajouter

Durant l'exécution de cet audit, plusieurs plateformes initialement non envisagées ont démontré une compatibilité technique parfaite et une immense pertinence thématique. Elles doivent être intégrées en priorité :

- **DOAJ (Directory of Open Access Journals) :** Pour filtrer et valoriser la recherche académique nativement ouverte. Son API documentée est un standard.
- **OpenAlex :** Ce graphe de connaissances mondial ouvert permet de centraliser la recherche en sound studies et media studies sans passer par des bases propriétaires payantes.
- **Data.gouv.fr (Exports INA) :** Les jeux de métadonnées ouverts relatifs aux podcasts de l'INA offrent une opportunité légitime et sûre de documenter la radio publique sans risquer de crawling sauvage.

## Sources à reporter ou éviter

- **WorldCat (OCLC) :** Représente un risque juridique disproportionné en raison de sa politique monopolistique hostile au partage de métadonnées en dehors d'abonnements institutionnels lourds.
- **Spotify & Mixcloud :** L'écosystème verrouillé et hostile aux développeurs indépendants de ces plateformes commerciales rend toute intégration instable et techniquement intenable à ce stade du projet.
- **Internet Archive & LoC :** Bien que validées prudemment pour les métadonnées de signalement, le développement de connecteurs spécifiques doit être reporté à une phase ultérieure afin de ne pas surcharger l'architecture initiale.

## Recommandations concrètes pour config/sources.yaml

Afin de matérialiser les exigences sécuritaires identifiées dans cet audit, le fichier de configuration `sources.yaml` doit structurer et imposer la logique de veille. Les connecteurs de collecte (qu'ils soient codés en Python ou en Go) devront lire cette configuration et appliquer les politiques de rate limiting et d'export public associées.

Exemple de structure recommandée pour le fichier de configuration :

```yaml
sources:
  - id: "hal_radio_studies_oai"
    name: "Archives Ouvertes HAL"
    family: "plateforme_academique"
    active: true
    type: "oai-pmh"
    url: "https://api.archives-ouvertes.fr/oai/hal/"
    query_set: "radio"
    rate_limit:
      delay_seconds: 2
      max_retries: 3
    security:
      auth_required: false
      public_export_allowed: true
    export_policy:
      allowed_fields: ["id", "title", "url", "doi", "published_at", "authors", "source_name", "legal_status"]
      drop_fields: ["abstract", "raw", "logs"]

  - id: "openalex_media_studies"
    name: "OpenAlex"
    family: "catalogue_global"
    active: false
    type: "api_rest"
    url: "https://api.openalex.org/works"
    rate_limit:
      delay_seconds: 1
      per_page: 20
      max_pages_per_profile: 1
    security:
      auth_required: true
      mailto_env: "OPENALEX_MAILTO"
      api_key_env: "OPENALEX_API_KEY"
    export_policy:
      allowed_fields: ["id", "title", "url", "doi", "published_at", "source_name"]
      drop_fields: ["abstract_inverted_index", "abstract", "raw", "logs", "authors", "topics", "keywords", "relevance_score"]
```

## Recommandations concrètes pour l'export public JSON

Le passage de la base de données privée (ex: `veille.sqlite` ou des répertoires de fichiers JSON locaux bruts) vers l'espace public du site Hugo doit être opéré par un script de build rigide. Ce script doit :

1. Lire la base de données de veille locale et privée.
2. Itérer sur chaque ressource validée.
3. Créer un nouvel objet contenant uniquement les clés explicitement autorisées dans la liste `allowed_fields` de la source concernée (allowlist stricte).
4. Nettoyer les métadonnées (Regex anti-fuite d'emails accidentellement capturés dans les noms d'auteurs).
5. Écrire le résultat dans un fichier `public_index.json` qui sera le seul artefact copié dans le répertoire `data/` de l'arborescence Hugo.

## Tests anti-fuite à implémenter (CI/CD)

Pour prémunir le projet contre les défaillances humaines (exposition involontaire de clés API ou d'abstracts protégés lors d'une mise à jour), l'intégration de tests unitaires locaux ou automatisés (GitHub Actions) est fortement recommandée :

- **Test `test_no_secrets` :** Scanne le fichier `public_index.json` généré à la recherche de chaînes suspectes comme `api_key=`, `Bearer `, `mailto=`, ou d'adresses email standard. Si une telle chaîne est détectée, le déploiement doit être immédiatement bloqué (Exit 1).
- **Test `test_no_copyrighted_content` :** S'assure qu'aucune clé nommée `abstract`, `summary`, `description`, `content`, `content:encoded`, ou `html` ne figure dans l'export public.
- **Test `test_whitelist_adherence` :** Valide de manière stricte que 100% des clés présentes dans l'export appartiennent à l'allowlist édictée dans la politique générale.

## Checklist avant publication (Go-Live)

Avant de procéder au premier déploiement public de l'antenne radio, le concepteur du projet devra valider la checklist de contrôle suivante :

- [x] L'en-tête HTTP User-Agent est défini de manière explicite et courtoise ("Antenne Radio/1.0 - Projet universitaire"), mentionnant l'URL du dépôt.
- [x] Les variables d'environnement confidentielles (clés API, email de contact pour Unpaywall et Crossref) sont chargées depuis un fichier local `.env` et n'apparaissent jamais en clair dans le code.
- [x] Le fichier `.gitignore` a été audité et exclut de manière sécurisée les dossiers de stockage privés (`private_store/`, `build_cache/`, `*.sqlite`, `.env`).
- [x] Les mécanismes de temporisation (sleep) et de backoff exponentiel sont codés et testés pour réagir gracieusement en cas d'erreur HTTP 429 (Rate Limit).
- [x] Le site public Hugo affiche une mention claire ("À propos") décrivant la finalité académique et non commerciale du projet, déclinant toute propriété intellectuelle sur les notices indexées et offrant une adresse de contact pour toute demande de retrait.
- [x] Les sources déconseillées ou bloquées (WorldCat, Spotify, Mixcloud) sont désactivées dans l'architecture active de collecte.

## Bibliographie et sitographie des pages officielles consultées

Afin de garantir la traçabilité complète des assertions et analyses techniques de cet audit, les ressources officielles suivantes ont été méticuleusement consultées et documentées :

- **CNIL (Commission Nationale de l'Informatique et des Libertés) :** Recommandations et base légale de l'intérêt légitime pour le moissonnage de données (web scraping).
- **INRAE :** Recommandations institutionnelles sur les pratiques et limites de la fouille de textes et de données (exception TDM dans la recherche publique).
- **APP (Agence pour la Protection des Programmes) :** Cadre juridique du web scraping et droit sui generis des producteurs de bases de données.
- **OAI-PMH (Open Archives Initiative) :** Spécifications techniques du protocole de moissonnage V2.0.
- **HAL (Archives Ouvertes) :** Principes directeurs, documentation de l'API SolR et guide du serveur OAI-PMH.
- **OpenAlex :** Documentation technique de l'API REST (Rate limiting, authentication, et licence CC0).
- **Crossref :** Guide d'implémentation de la récupération de métadonnées et documentation du programme Plus.
- **Europeana :** Conditions générales d'utilisation des API et politique de droits d'auteur du patrimoine culturel.
- **WorldCat / OCLC :** Conditions générales de service de WorldCat.org et conditions d'accès aux API de catalogage.
- **Radio France :** Portail développeurs de l'Open API et conditions générales d'utilisation des sites.
- **OpenEdition :** Documentation technique du dépôt OAI-PMH v2 et formats de syndication.
- **BnF / Gallica :** Spécifications d'utilisation des entrepôts OAI-NUM, OAI-CAT, et guide de l'API document Gallica.
- **Érudit :** Présentation des technologies de diffusion et accès OAI public.
- **Persée :** Guide d'utilisation des web services et politique de fouille de données massives.
- **Cairn :** Conditions d'utilisation de la plateforme et protection contre l'aspiration automatisée.
- **CiNii / NII :** Linking policy, copyright et conditions d'accès aux flux RDF/JSON-LD.
- **DOAJ :** Guide de l'API de l'annuaire ouvert et durabilité de l'infrastructure open access.
- **theses.fr (Abes) :** Documentation de l'API Export des notices doctorales.
- **Isidore (Huma-Num) :** CGU de la plateforme de recherche et documentation d'infrastructure.
- **Unpaywall :** Spécifications de l'API de recherche Open Access et politique de courtoisie.
- **Spotify :** Conditions générales d'utilisation de l'API développeurs (durcissement contractuel 2026).
- **Apple Podcasts :** iTunes Search API Guidelines et politiques d'attribution.
- **Podcast Index :** Spécifications techniques de l'API REST communautaire.
- **Data.gouv.fr / INA :** Licence Ouverte des jeux de données d'archives de l'Institut National de l'Audiovisuel.

## Sources des citations

1. Recommandations sur les usages du webscraping au sein d'INRAE, consulté le mai 20, 2026, https://science-ouverte.inrae.fr/fr/offre-service/fiches-pratiques-et-recommandations/recommandations-sur-les-usages-du-webscraping-au-sein-dinrae
2. La base légale de l'intérêt légitime : fiche focus sur les mesures à ..., consulté le mai 20, 2026, https://www.cnil.fr/fr/focus-interet-legitime-collecte-par-moissonnage
3. The legal basis of legitimate interest: focus sheet on the measures to implement in the case of data collection by web scraping | CNIL, consulté le mai 20, 2026, https://www.cnil.fr/en/legal-basis-legitimate-interest-focus-sheet-measures-implement-case-data-collection-web-scraping
4. Le Web Scraping est-il légal ?, consulté le mai 20, 2026, https://www.app.asso.fr/preuve-digitale/web-scraping-legal.html
5. Podcast, mode d'emploi - Audioblogs - ARTE Radio, consulté le mai 20, 2026, https://audioblog.arteradio.com/article/137732/podcast-mode-d-emploi
6. What is an API and OAI-PMH? - Figshare, consulté le mai 20, 2026, https://info.figshare.com/user-guide/what-is-an-api-and-oai-pmh/
7. Authentication & Pricing - OpenAlex Developers, consulté le mai 20, 2026, https://developers.openalex.org/api-reference/authentication
8. Announcing changes to REST API rate limits - Crossref, consulté le mai 20, 2026, https://www.crossref.org/blog/announcing-changes-to-rest-api-rate-limits/
9. Documentation - Metadata Retrieval - Crossref, consulté le mai 20, 2026, https://www.crossref.org/documentation/retrieve-metadata/
10. Principles - About HAL, consulté le mai 20, 2026, https://about.hal.science/en/principles/
11. Protocol for Metadata Harvesting - v.2.0 - Open Archives Initiative, consulté le mai 20, 2026, https://www.openarchives.org/OAI/openarchivesprotocol.html
12. OpenEdition OAI-PMH repository Documentation — OpenEdition ..., consulté le mai 20, 2026, https://oai-openedition.readthedocs.io/
13. The Legal Landscape of Web Scraping - Quinn Emanuel, consulté le mai 20, 2026, https://www.quinnemanuel.com/the-firm/publications/the-legal-landscape-of-web-scraping/
14. ARTE Radio - Apple Podcasts, consulté le mai 20, 2026, https://podcasts.apple.com/us/artist/arte-radio/1251092473
15. Serveur OAI-PMH - Documentation API-HAL, consulté le mai 20, 2026, https://api.archives-ouvertes.fr/docs/oai
16. Documentation API-HAL | API Archive Ouverte HAL, consulté le mai 20, 2026, https://api.archives-ouvertes.fr/
17. API HAL API de recherche HAL, consulté le mai 20, 2026, https://api.archives-ouvertes.fr/docs/search
18. New Features and Usage-Based Pricing - OpenAlex blog, consulté le mai 20, 2026, https://blog.openalex.org/openalex-api-new-features-and-usage-based-pricing/
19. API keys required starting Feb 13 (and some new endpoints!) - Google Groups, consulté le mai 20, 2026, https://groups.google.com/g/openalex-users/c/rI1GIAySpVQ
20. License information - Crossref, consulté le mai 20, 2026, https://www.crossref.org/documentation/schema-library/markup-guide-metadata-segments/license-information/
21. DOAJ Application Guide for OJS Journals - PKP Docs, consulté le mai 20, 2026, https://docs.pkp.sfu.ca/doaj/en/
22. How I use DOAJ metadata in my work and research, consulté le mai 20, 2026, https://blog.doaj.org/2025/06/15/how-i-use-doaj-metadata-in-my-work-and-research/
23. Searching the Directory of Open Access Journals (DOAJ) - Nested Knowledge, consulté le mai 20, 2026, https://about.nested-knowledge.com/docs/searching-the-directory-of-open-access-journals-doaj/
24. Infrastructure and why sustainable funding so important to services like DOAJ, consulté le mai 20, 2026, https://blog.doaj.org/2018/10/01/infrastructure-and-why-sustainable-funding-so-important-to-services-like-doaj/
25. API FAQ - Europeana Knowledge Base - Confluence, consulté le mai 20, 2026, https://europeana.atlassian.net/wiki/spaces/EF/pages/2360508417
26. Terms of Use - Europeana, consulté le mai 20, 2026, https://www.europeana.eu/en/rights/terms-of-use
27. consulté le mai 20, 2026, https://europeana.atlassian.net/wiki/spaces/EF/pages/2360508417#:~:text=Europeana%20gives%20access%20to%20all,have%20limitations%20posed%20upon%20them.
28. API Export des Données de theses.fr - Data gouv, consulté le mai 20, 2026, https://www.data.gouv.fr/dataservices/api-export-des-donnees-de-theses-fr
29. Theses.fr, consulté le mai 20, 2026, https://theses.fr/
30. Entrepôt OAI-PMH de Gallica et des expositions virtuelles (OAI-NUM) | BnF API et jeux de données, consulté le mai 20, 2026, https://api.bnf.fr/fr/oai-num
31. Récupérer des notices bibliographiques en Dublin Core (OAI-CAT) | BnF - Site institutionnel, consulté le mai 20, 2026, https://www.bnf.fr/fr/recuperer-des-notices-bibliographiques-en-dublin-core-oai-cat
32. API Document de Gallica | BnF API et jeux de données, consulté le mai 20, 2026, https://api.bnf.fr/fr/api-document-de-gallica
33. Help for the Sudoc catalogue - Documentation ABES, consulté le mai 20, 2026, https://documentation.abes.fr/aidesudoc/EN/accueil/aidesudoc_index.html
34. IdRef - Documentation ABES, consulté le mai 20, 2026, https://documentation.abes.fr/aideidref/accueil/en/index.html
35. Cas d'usage API publique avec laisser-passer - Huma Num - ORCID France, consulté le mai 20, 2026, https://orcid-france.fr/cas-usage/cas-usage-api-publique-avec-laisser-passer-huma-num/
36. Conditions Générales d'Utilisation (CGU) du service isidore.science, consulté le mai 20, 2026, https://isidore.science/cgu
37. ISIDORE (en) - Documentation de l'infrastructure Huma-Num, consulté le mai 20, 2026, https://documentation.huma-num.fr/en/isidore-en/
38. ISIDORE (fr) - Documentation de l'infrastructure Huma-Num, consulté le mai 20, 2026, https://documentation.huma-num.fr/isidore/
39. Metadata and API - CiNii Articles RDF for Authors | Support Academic Information Services, consulté le mai 20, 2026, https://support.nii.ac.jp/en/cia/api/a_rdf_auth
40. Metadata and API - CiNii Articles JSON-LD for Authors (Beta) - 国立情報学研究所, consulté le mai 20, 2026, https://support.nii.ac.jp/en/cia/api/a_json_auth
41. CiNii - Copyright and Linking | Support Academic Information Services, consulté le mai 20, 2026, https://support.nii.ac.jp/en/cinii/copyright
42. Terms of Use - CiNii Labs, consulté le mai 20, 2026, https://labs.ci.nii.ac.jp/en/termsofuse.html
43. The list of API-providing databases | NDL Search | National Diet Library, consulté le mai 20, 2026, https://ndlsearch.ndl.go.jp/en/help/api/provider
44. Institut national de l'audiovisuel INA - Data gouv, consulté le mai 20, 2026, https://www.data.gouv.fr/organizations/institut-national-de-laudiovisuel
45. REST API - Unpaywall, consulté le mai 20, 2026, https://unpaywall.org/products/api
46. Find Free Versions of Scholarly Publications via Unpaywall • roadoi - Docs - rOpenSci, consulté le mai 20, 2026, https://docs.ropensci.org/roadoi/
47. Fetch open access status information and full-text links using Unpaywall — oadoi_fetch • roadoi - Docs, consulté le mai 20, 2026, https://docs.ropensci.org/roadoi/reference/oadoi_fetch.html
48. L'open API Radio France | Radio France, consulté le mai 20, 2026, https://www.radiofrance.com/lopen-api-radio-france
49. Conditions générales d'utilisation des sites de Radio France, consulté le mai 20, 2026, https://www.radiofrance.com/conditions-generales-dutilisation-des-sites-de-radio-france
50. radiofrance/communication - GitHub, consulté le mai 20, 2026, https://github.com/radiofrance/communication
51. Protection des données personnelles et politique de confidentialité à Radio France, consulté le mai 20, 2026, https://www.radiofrance.com/protection-des-donnees
52. RSS Radio France pour tous - Framalibre, consulté le mai 20, 2026, https://framalibre.org/notices/rss-radio-france-pour-tous.html
53. API Docs | PodcastIndex.org, consulté le mai 20, 2026, https://podcastindex-org.github.io/docs-api/
54. Rate Limits | Podchaser Enterprise API — GraphQL Documentation, consulté le mai 20, 2026, https://api-docs.podchaser.com/docs/rate-limits
55. Listen Notes Podcast API Rate Limits, consulté le mai 20, 2026, https://www.listennotes.help/article/109-listen-notes-podcast-api-rate-limits
56. Ratelimiting · Issue #30 · Podcastindex-org/docs-api - GitHub, consulté le mai 20, 2026, https://github.com/Podcastindex-org/docs-api/issues/30
57. Identifying Rate Limits | Apple Developer Documentation, consulté le mai 20, 2026, https://developer.apple.com/documentation/appstoreconnectapi/identifying-rate-limits
58. iTunes Search API - Apple Services Performance Partners, consulté le mai 20, 2026, https://performance-partners.apple.com/search-api
59. iTunes Search API rate limit - Stack Overflow, consulté le mai 20, 2026, https://stackoverflow.com/questions/12596300/itunes-search-api-rate-limit
60. Is iTunes Search API Rate Limit per device or per app? - Stack Overflow, consulté le mai 20, 2026, https://stackoverflow.com/questions/41290585/is-itunes-search-api-rate-limit-per-device-or-per-app
61. Web scraping : avec quelles données peut-on nourrir l'intelligence artificielle (IA), consulté le mai 20, 2026, https://droit.cairn.info/revue-dpo-news-2025-3-page-7?lang=fr
62. Modular Rules & Procedures - Cairn RPG, consulté le mai 20, 2026, https://cairnrpg.com/hacks/third-party/modular-rules-procedures/
63. Fouille de données - Persée UAR, consulté le mai 20, 2026, https://info.persee.fr/fouille-de-donnees/
64. Technology - Érudit, consulté le mai 20, 2026, https://apropos.erudit.org/technologies/?lang=en
65. A quick guide for SSHRC's Aid to Scholarly Journals 2025 - Érudit, consulté le mai 20, 2026, https://www.erudit.org/public/documents/Guide_ASJ_2025_ENG.pdf
66. RadioMorphoses - Revue d'études radiophoniques et sonores - OpenEdition Journals, consulté le mai 20, 2026, https://journals.openedition.org/radiomorphoses/?lang=en
67. Broadcast the Radio Survivor show on your radio station, consulté le mai 20, 2026, https://www.radiosurvivor.com/radio/
68. Sounding Out! | pushing sound studies into the red since 2009, consulté le mai 20, 2026, https://soundstudiesblog.com/
69. Update on Developer Access and Platform Security, consulté le mai 20, 2026, https://developer.spotify.com/blog/2026-02-06-update-on-developer-access-and-platform-security
70. Rate Limits - Spotify for Developers, consulté le mai 20, 2026, https://developer.spotify.com/documentation/web-api/concepts/rate-limits
71. Terms of use of Deezer for Developers, consulté le mai 20, 2026, https://developers.deezer.com/termsofuse
72. Spotify just killed indie development with their new API restrictions : r/truespotify - Reddit, consulté le mai 20, 2026, https://www.reddit.com/r/truespotify/comments/1l2am4i/spotify_just_killed_indie_development_with_their/
73. WorldCat Terms and Conditions - OCLC, consulté le mai 20, 2026, https://www.oclc.org/content/dam/ext-ref/worldcat-org/terms.html
74. WorldCat Search API | OCLC Developer Network, consulté le mai 20, 2026, https://www.oclc.org/developer/api/oclc-apis/worldcat-search-api.en.html
75. 1.3B Worldcat scrape and data science mini-competition | Hacker News, consulté le mai 20, 2026, https://news.ycombinator.com/item?id=37764088

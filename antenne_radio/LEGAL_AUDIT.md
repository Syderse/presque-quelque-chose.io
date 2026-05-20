# Audit Juridique et Technique : Architecture de Veille et d'Indexation pour les Radio Studies

## 2. Date de l'audit

Cet audit a été réalisé et consolidé le 20 Mai 2026. Il reflète l'état des conditions générales d'utilisation, des politiques d'interface de programmation (API), et du cadre juridique européen et français à cette date.

## 3. Avertissement

Le présent rapport constitue une analyse technique et une évaluation des risques fondées sur la documentation publique des fournisseurs de données, les recommandations de la Commission Nationale de l'Informatique et des Libertés (CNIL), et les principes généraux du droit du numérique. Ce document ne constitue en aucun cas un avis juridique professionnel opposable. Toute implémentation relève de la responsabilité exclusive des concepteurs du projet. Une approche orientée vers la prudence maximale et la réduction des risques a été systématiquement adoptée pour pallier les incertitudes jurisprudentielles.

## 4. Résumé exécutif

Le projet d'antenne de veille universitaire en radio studies, sound studies et histoire des médias radiophoniques repose sur une architecture duale. D'une part, il implique le développement d'un pipeline local destiné à la collecte exhaustive, à la fouille de données et à l'importation vers des logiciels de gestion bibliographique comme Zotero. D'autre part, il prévoit l'exposition publique d'un index léger et statique, généré via le framework Hugo. L'analyse démontre que l'agrégation de métadonnées pour un usage strictement privé et de recherche s'inscrit largement dans le cadre des exceptions légales relatives à la fouille de textes et de données, sous réserve de respecter le principe de minimisation. En revanche, l'exposition publique de ces mêmes données cristallise des risques juridiques significatifs, notamment en matière de droit d'auteur, de protection des bases de données et de conditions d'utilisation contractuelles dictées par les plateformes. Afin de sécuriser le projet, il est impératif d'instaurer une étanchéité technique et conceptuelle absolue entre le stockage local riche et l'affichage public minimaliste, ce dernier devant se limiter à un rôle de pointage vers les sources originelles sans jamais s'y substituer.

## 5. Verdict global

Le projet est jugé juridiquement viable et techniquement réalisable, à la condition stricte que les garde-fous identifiés dans ce rapport soient intégrés au cœur même de l'architecture logicielle. L'initiative s'inscrit dans la philosophie de la science ouverte et de la découvrabilité des ressources académiques, à condition d'opérer exclusivement comme un catalogue de signalement. L'utilisation d'APIs ouvertes et du protocole OAI-PMH doit être privilégiée. Les plateformes imposant des écosystèmes fermés ou interdisant formellement l'extraction automatisée doivent être exclues du périmètre technique pour éviter tout risque de litige pour parasitisme ou violation contractuelle.

## 6. Politique générale du projet

La stratégie opérationnelle de l'antenne radio s'articule autour d'un principe fondamental : moissonner avec respect, stocker avec précaution, et publier avec une extrême parcimonie. L'infrastructure ne doit à aucun moment héberger, répliquer ou diffuser des œuvres de l'esprit (textes intégraux, créations sonores, résumés originaux) sans une licence explicite le permettant. Le pipeline doit être conçu pour asseoir la légitimité du projet vis-à-vis des éditeurs : identification transparente des robots de collecte, limitation stricte de la cadence des requêtes, et redirection systématique du trafic public vers les ayants droit.

## 7. Contrat public de données

La publication des données via le site statique Hugo doit obéir à une liste d'inclusion stricte (whitelist). Toute donnée non explicitement autorisée par ce contrat doit être filtrée lors de la phase de compilation.

| Champ | Statut | Justification juridique et technique |
| :--- | :--- | :--- |
| id | Autorisé | Identifiant interne généré localement, exempt de droit. |
| title | Autorisé | Information factuelle descriptive. Les titres échappent généralement au droit d'auteur, sauf originalité exceptionnelle. |
| url ou original_url | Autorisé | Le lien hypertexte simple ne constitue pas une communication au public d'une œuvre protégée si celle-ci est déjà librement accessible. |
| doi | Autorisé | Identifiant standard ouvert, conçu pour le partage. |
| published_at | Autorisé | Donnée purement factuelle et historique. |
| authors | Autorisé | La citation de la paternité est un fait historique et une obligation morale. |
| source_name | Autorisé | Indispensable pour l'attribution correcte de la ressource. |
| source_type | Autorisé | Catégorisation technique locale (article, podcast, ouvrage). |
| language | Autorisé | Métadonnée descriptive factuelle. |
| source_family | Autorisé | Taxonomie locale permettant le filtrage sur le site. |
| legal_status | Autorisé | Indique la licence (ex: Open Access, CC-BY) pour orienter l'utilisateur. |
| audit_date | Autorisé | Date de validation technique locale du lien. |
| abstract / summary | Interdit | L'abstract est une œuvre de l'esprit protégeable. Sa reproduction sans autorisation constitue une contrefaçon, sauf licence Creative Commons explicite. |
| content / full_text | Interdit | Violation directe du droit d'auteur et des droits d'exploitation. |
| pdf_url | Interdit | Risque de facilitation du contournement de mesures de protection si la source n'est pas strictement Open Access. L'usager doit utiliser l'original_url. |
| images / audio | Interdit | Fichiers soumis à des droits d'auteur et droits voisins. L'hébergement ou l'intégration (hotlinking) non autorisée est proscrite. |
| raw / logs / secrets | Interdit | Risque critique de cybersécurité et fuite de données personnelles ou de clés d'authentification. |

La décision d'interdire les résumés et les URL de téléchargement direct de PDF ou d'audio repose sur la volonté de ne pas cannibaliser le trafic des éditeurs originaux et de ne pas engager la responsabilité du projet en tant qu'hébergeur de contenus contrefaisants.

## 8. Politique privée de collecte

La constitution d'une base de données locale pour la veille universitaire bénéficie d'un cadre légal plus clément. Le droit européen, via la directive de 2019 sur le droit d'auteur (2019/790), instaure une exception pour la fouille de textes et de données (Text and Data Mining - TDM) au profit de la recherche.<sup>1</sup> Cette exception permet l'analyse automatisée de corpus à condition que l'accès originel soit licite et que les ayants droit n'aient pas expressément exprimé d'opposition (opt-out) via des mesures lisibles par machine.<sup>2</sup>
Toutefois, le moissonnage doit impérativement respecter le droit sui generis des producteurs de bases de données, prohibant l'extraction substantielle non autorisée.<sup>4</sup> Sur le volet des données à caractère personnel, la CNIL exige le respect du principe de minimisation.<sup>2</sup> Il est donc impératif d'exclure de la collecte les sites s'opposant clairement au web scraping via leur fichier robots.txt ou la présence de CAPTCHA. Toute donnée sensible collectée de manière résiduelle ou fortuite doit être supprimée immédiatement.<sup>2</sup> La base locale doit demeurer sur un environnement chiffré, accessible au seul chercheur.

## 9. Politique d'abstracts

L'appréhension des résumés académiques et descriptifs journalistiques requiert une grande prudence. Bien que cruciaux pour la recherche bibliographique et l'indexation algorithmique (TF-IDF, similarité sémantique) exécutée au sein du pipeline privé, ces textes constituent des créations intellectuelles originales. Leur moissonnage local est justifié par l'exception TDM, mais leur exposition publique est strictement interdite par défaut. Une exception peut être programmée pour les sources délivrant formellement leurs métadonnées sous licence CC0 (comme OpenAlex) ou CC-BY (comme certaines notices d'Europeana), sous réserve de reproduire la chaîne d'attribution requise.

## 10. Politique des contenus RSS

Le format RSS (Really Simple Syndication) incarne une volonté de dissémination de la part de l'éditeur. Néanmoins, la mise à disposition d'un flux n'équivaut pas à une cession de droits permettant la constitution d'une archive publique tierce.<sup>5</sup> La collecte privée peut traiter les balises content:encoded ou description pour évaluer la pertinence de l'article, mais le module d'exportation vers Hugo doit impérativement expurger ces champs. Le site public ne fonctionnera qu'en tant que relais de titres cliquables vers l'article source.

## 11. Politique des APIs

L'utilisation d'interfaces de programmation applicatives (API) est le vecteur privilégié du projet, car elle manifeste une volonté explicite d'interopérabilité de la part du fournisseur.<sup>6</sup> Cependant, l'accès est conditionné à l'acceptation de Conditions Générales d'Utilisation (CGU). Le pipeline technique doit intégrer de manière transparente l'identité du projet en fournissant un en-tête HTTP User-Agent descriptif et, lorsque cela est exigé (comme pour l'API Crossref), une adresse électronique de contact (mailto:) pour accéder aux pools de requêtes dits "polis".<sup>7</sup> Aucune technique de dissimulation (rotation d'adresses IP, falsification d'en-têtes) ne doit être employée pour contourner les quotas.

## 12. Politique des sources académiques

Les infrastructures de la science ouverte (OpenAlex, HAL, Crossref, bases OAI-PMH) constituent le cœur légitime du projet.<sup>7</sup> L'usage du protocole OAI-PMH (Open Archives Initiative Protocol for Metadata Harvesting) est fortement recommandé pour les dépôts institutionnels. Ce protocole, utilisant le verbe ListRecords et la mécanique des resumptionTokens, permet un moissonnage asynchrone, paginé, et conçu précisément pour minimiser la charge sur les serveurs cibles.<sup>11</sup> Les métadonnées issues de ces plateformes, souvent formatées en Dublin Core (oai_dc), présentent un risque juridique extrêmement faible, les institutions favorisant activement la découvrabilité de leur patrimoine scientifique.

## 13. Politique des sources journalistiques / blogs

Les publications spécialisées (La Lettre Pro, Radio Survivor, Nieman Storyboard, etc.) relèvent d'un régime de droit d'auteur classique. La récupération de leurs informations doit se limiter à l'interrogation de leurs flux RSS officiels ou de leurs sitemaps. L'aspiration des pages HTML complètes (web scraping) pour en extraire le corps du texte est fortement déconseillée, d'autant plus que les conditions générales de nombreux médias interdisent l'extraction automatisée.<sup>13</sup> Le pipeline doit se contenter des métadonnées de surface.

## 14. Politique des podcasts et fichiers audio

Le traitement des œuvres sonores exige une prudence redoublée en raison de la superposition des droits (auteurs, producteurs, interprètes). Les flux RSS de podcasts (ARTE Radio, Transom, BBC) structurent l'accès via la balise <enclosure> pointant vers le fichier audio.<sup>5</sup> Il est recommandé de ne pas procéder au téléchargement des fichiers MP3 en local, sauf nécessité absolue d'analyse computationnelle (ex: extraction de transcriptions privées). Sur le versant public, la ré-hébergement de l'audio ou l'intégration de lecteurs personnalisés contournant les statistiques d'audience de l'éditeur est prohibée. Seuls les hyperliens orientant l'auditeur vers la plateforme officielle de diffusion sont autorisés.

## 15. Politique de rate limiting

La viabilité technique de l'antenne radio dépend de sa civilité algorithmique. Le moteur de collecte doit implémenter une gestion robuste de la cadence de requêtage. Une temporisation (sleep) d'au moins 1 à 2 secondes entre chaque appel HTTP est prescrite pour les APIs sans quotas explicites. Les architectures d'ingestion doivent scruter les en-têtes HTTP de limitation, tels que X-RateLimit-Remaining ou Retry-After.<sup>7</sup> En cas de réception d'un code d'erreur 429 (Too Many Requests), le système doit suspendre immédiatement ses opérations via une stratégie de retrait exponentiel (exponential backoff). La mise en cache des réponses locales est obligatoire pour éviter toute redondance de requêtes sur le réseau.

## 16. Politique de logs et fichiers bruts

Les réponses brutes (payloads JSON ou XML) retournées par les APIs peuvent receler des données non destinées à la publication, telles que les identifiants internes des plateformes, des adresses email d'auteurs ou des clés d'accès techniques. L'enregistrement des historiques d'exécution (logs) doit être confiné à l'environnement de développement local, soumis à une rotation régulière pour éviter l'accumulation de données. Les traces d'erreurs (stack traces) ne doivent jamais être transmises au générateur statique Hugo.

## 17. Politique Git / publication / Hugo

L'architecture logicielle impose une dichotomie au niveau du contrôle de version. Le dépôt contenant le code source du moissonneur et les templates du site Hugo peut être rendu public (ex: GitHub, GitLab). En revanche, le répertoire hébergeant la base de données relationnelle locale (ex: SQLite), les fichiers de configuration contenant des variables d'environnement (.env) et le cache des requêtes brutes doit obligatoirement être consigné dans le fichier .gitignore. Seul le fichier JSON expurgé, résultant de la procédure de liste blanche, doit être versionné ou transmis au serveur de déploiement continu.

## 18. Tableau synthétique de toutes les sources

| Source | Famille | Point d'accès | Statut Recommandé | Risque |
| :--- | :--- | :--- | :--- | :--- |
| HAL | Académique | API / OAI-PMH | VALIDÉ | Faible |
| OpenAlex | Académique | API REST | VALIDÉ | Faible |
| Crossref | Académique | API REST | VALIDÉ | Faible |
| DOAJ | Académique | API REST | VALIDÉ | Faible |
| Europeana | Patrimoine | API REST | VALIDÉ | Faible |
| Theses.fr | Académique | API / OAI-PMH | VALIDÉ | Faible |
| BnF / Gallica | Patrimoine | OAI-PMH / API | VALIDÉ | Faible |
| Sudoc / Abes | Académique | OAI-PMH | VALIDÉ | Faible |
| Isidore | Académique | OAI-PMH / API | VALIDÉ | Faible |
| ORCID | Académique | API | VALIDÉ | Faible |
| CiNii / NDL / J-STAGE | Académique | API | VALIDÉ | Faible |
| INA | Archives | Open Data (API) | VALIDÉ PRUDENT | Modéré |
| Unpaywall | Académique | API REST | VALIDÉ PRUDENT | Faible |
| Radio France | Média | API / RSS | VALIDÉ PRUDENT | Modéré |
| Podcast Index | Annuaire | API REST | VALIDÉ PRUDENT | Modéré |
| Apple Podcasts | Annuaire | API Search | VALIDÉ STRICT | Modéré |
| Cairn / Persée / Érudit | Revues SHS | OAI-PMH / RSS | VALIDÉ STRICT | Modéré |
| Radio Survivor, Sounding Out!... | Blogs / RSS | RSS / Atom | VALIDÉ STRICT | Modéré |
| Journaux académiques (T&F...) | Revues | RSS / Crossref | VALIDÉ STRICT | Modéré |
| BBC Sounds / NPR / ARTE Radio | Média / Audio | RSS | VALIDÉ STRICT | Modéré |
| Internet Archive | Archives | API | À REPORTER | Incertain |
| Library of Congress | Archives | API | À REPORTER | Incertain |
| Spotify / Deezer | Plateformes | API | À ÉVITER | Élevé |
| SoundCloud / Mixcloud | Plateformes | API / RSS | À ÉVITER | Élevé |
| WorldCat | Catalogue | API | INTERDIT POUR EXPORT PUBLIC | Élevé |

## 19. Fiches détaillées source par source

### HAL


**Statut recommandé :** VALIDÉ

**Famille :** Plateforme académique / OAI-PMH

**Pertinence pour l’antenne :**
Dépôt institutionnel majeur pour la littérature scientifique francophone. Constitue le socle de la veille en sciences de l'information et de la communication concernant la radio.

**Point d’accès recommandé :**
API REST (api.archives-ouvertes.fr/search/) ou OAI-PMH (api.archives-ouvertes.fr/oai/hal/).<sup>15</sup>

**Pages officielles consultées :**
- https://api.archives-ouvertes.fr/docs/search <sup>17</sup>
- https://api.archives-ouvertes.fr/docs/oai <sup>15</sup>
- https://about.hal.science/en/principles/ <sup>10</sup>

**Constats juridiques et techniques :**
- L'infrastructure OAI garantit une interopérabilité totale, sans nécessité d'inscription.<sup>10</sup>
- L'exploitation commerciale des métadonnées extraites est prohibée, mais l'usage académique et d'indexation est encouragé.<sup>15</sup>

**Collecte privée autorisée ou raisonnable :**
Métadonnées bibliographiques intégrales, identifiants auteurs (idHAL), résumés, affiliations.

**Affichage public recommandé :**
title, doi, URL canonique HAL, auteurs, date de publication, type de document.

**Champs interdits en public :**
Abstracts complets (en raison des droits résiduels éventuels des éditeurs initiaux), texte intégral des dépôts.

**Attribution minimale :**
Source: HAL (Archives Ouvertes) — lien vers la notice originale.

**Rate limit / conditions techniques :**
Pagination obligatoire (limite de 10 000 résultats via paramètre rows).<sup>17</sup> Cadence d'une requête par seconde recommandée.

**Risques :**
Faible. Source institutionnelle conçue pour le partage ouvert.

**Décision pratique pour sources.yaml :**
```yaml
active: true
raison : Source francophone incontournable, fiable et ouverte.
notes d’implémentation : Privilégier le moissonnage par collections spécifiques ou requêtes disciplinaires via l'API SolR.
```

### OpenAlex


**Statut recommandé :** VALIDÉ

**Famille :** Catalogue académique global / API

**Pertinence pour l’antenne :**
Graphe de connaissances remplaçant de nombreuses bases propriétaires. Couvre la quasi-totalité des publications mondiales en sound studies et media studies.

**Point d’accès recommandé :**
API REST (api.openalex.org).

**Pages officielles consultées :**
- https://developers.openalex.org/api-reference/authentication <sup>7</sup>
- https://blog.openalex.org/openalex-api-new-features-and-usage-based-pricing/ <sup>18</sup>

**Constats juridiques et techniques :**
- L'ensemble des données est placé sous licence CC0 (domaine public).<sup>19</sup>
- Un système de crédits gratuits (100 000 crédits/jour) impose l'utilisation d'une clé d'API pour tout usage sérieux.<sup>7</sup>

**Collecte privée autorisée ou raisonnable :**
Totalité du graphe : auteurs, institutions, concepts, références croisées.

**Affichage public recommandé :**
title, doi, URL, auteurs, année de publication, concepts, source_name.

**Champs interdits en public :**
L'index d'abstracts inversé (trop lourd), dumps API bruts.

**Attribution minimale :**
Source: OpenAlex — lien vers le DOI ou la notice.

**Rate limit / conditions techniques :**
Nécessite le passage de api_key=VOTRE_CLE. Limite stricte de 100 requêtes par seconde.<sup>7</sup> Utiliser le paramètre per_page=100 pour optimiser la consommation de crédits.<sup>7</sup>

**Risques :**
Faible. Cadre juridique CC0 exceptionnellement favorable.

**Décision pratique pour sources.yaml :**
```yaml
active: true
raison : Réservoir de données massives sans barrière juridique.
notes d’implémentation : Injecter la clé API via l'environnement local. Surveiller l'en-tête X-RateLimit-Remaining.
```

### Crossref


**Statut recommandé :** VALIDÉ

**Famille :** Agence d'enregistrement DOI / API

**Pertinence pour l’antenne :**
Standard d'identification des publications. Permet de résoudre les liens cassés et d'obtenir des métadonnées normalisées sur les revues académiques internationales.

**Point d’accès recommandé :**
API REST (api.crossref.org).

**Pages officielles consultées :**
- https://www.crossref.org/documentation/retrieve-metadata/ <sup>9</sup>
- https://www.crossref.org/blog/announcing-changes-to-rest-api-rate-limits/ <sup>8</sup>

**Constats juridiques et techniques :**
- Les métadonnées sont librement accessibles à la communauté.<sup>9</sup>
- Les informations de licence y sont structurées, permettant de vérifier les conditions de réutilisation.<sup>20</sup>

**Collecte privée autorisée ou raisonnable :**
Métadonnées complètes liées aux identifiants DOI.

**Affichage public recommandé :**
title, URL (via résolveur doi.org), auteurs, date, revue.

**Champs interdits en public :**
Réponses API brutes.

**Attribution minimale :**
Source: Crossref — lien DOI.

**Rate limit / conditions techniques :**
L'accès au Polite Pool (file d'attente prioritaire et plus permissive) exige la transmission d'une adresse email valide via le paramètre mailto= ou l'en-tête User-Agent.<sup>8</sup>

**Risques :**
Faible. Infrastructure d'intérêt public.

**Décision pratique pour sources.yaml :**
```yaml
active: true
raison : Données bibliographiques de référence absolue.
notes d’implémentation : Configuration obligatoire du paramètre mailto pour la courtoisie réseau.
```

### DOAJ (Directory of Open Access Journals)


**Statut recommandé :** VALIDÉ

**Famille :** Catalogue académique / API

**Pertinence pour l’antenne :**
Permet de s'assurer que les articles indexés sont réellement en Open Access, facilitant la mise à disposition de la recherche sur la radio.

**Point d’accès recommandé :**
API REST (doaj.org/api/).

**Pages officielles consultées :**
- https://docs.pkp.sfu.ca/doaj/en/ <sup>21</sup>
- https://blog.doaj.org/2025/06/15/how-i-use-doaj-metadata-in-my-work-and-research/ <sup>22</sup>

**Constats juridiques et techniques :**
- Le DOAJ milite pour l'accès ouvert libre (Libre Open Access) et répertorie des métadonnées gratuites de journaux peer-reviewed.<sup>21</sup>
- L'API limite généralement les résultats à 1000 notices par recherche pour préserver la base de données ElasticSearch.<sup>23</sup>

**Collecte privée autorisée ou raisonnable :**
Métadonnées des journaux et des articles.

**Affichage public recommandé :**
Liens, titres, informations de licence.

**Champs interdits en public :**
Dumps complets.

**Attribution minimale :**
Source: DOAJ — lien.

**Rate limit / conditions techniques :**
Pagination obligatoire. Les concepteurs du DOAJ signalent que l'infrastructure peut souffrir de charges élevées 24 ; une cadence modérée est de rigueur.

**Risques :**
Faible.

**Décision pratique pour sources.yaml :**
```yaml
active: true
raison : Validation fiable du statut Open Access des ressources.
notes d’implémentation : Gérer le plafond des 1000 résultats par segmentation temporelle si nécessaire.
```

### Europeana


**Statut recommandé :** VALIDÉ

**Famille :** Catalogue du patrimoine culturel / API

**Pertinence pour l’antenne :**
Ressource exceptionnelle pour l'histoire des médias, les archives sonores européennes et l'esthétique radiophonique ancienne.

**Point d’accès recommandé :**
Search API et Record API (api.europeana.eu).

**Pages officielles consultées :**
- https://europeana.atlassian.net/wiki/spaces/EF/pages/2360508417 25
- https://www.europeana.eu/en/rights/terms-of-use <sup>26</sup>

**Constats juridiques et techniques :**
- L'accès est gratuit, inconditionnel sur le volume de lecture, mais requiert une clé d'API.<sup>25</sup>
- Bien que le portail agrége des œuvres du domaine public, la plateforme se dégage de toute responsabilité quant aux erreurs de droits d'auteur émanant des institutions contributrices.<sup>26</sup>

**Collecte privée autorisée ou raisonnable :**
Métadonnées patrimoniales, informations géographiques et temporelles.

**Affichage public recommandé :**
title, URL (vers europeana.eu), institution source, statut légal (ex: Public Domain).

**Champs interdits en public :**
L'intégration directe de médias soumis à des licences restrictives en dehors du Europeana Media Player.<sup>26</sup>

**Attribution minimale :**
Source: Europeana, fourni par [Institution] — lien.

**Rate limit / conditions techniques :**
Authentification par clé. Requêtes espacées pour une intégration propre.

**Risques :**
Faible. Les conditions d'utilisation encouragent explicitement l'exploitation via API.

**Décision pratique pour sources.yaml :**
```yaml
active: true
raison : Découverte de matériaux historiques rares sur la radiodiffusion.
notes d’implémentation : Mapper systématiquement le champ des droits (Rights Statement) pour vérification.
```

### Theses.fr


**Statut recommandé :** VALIDÉ

**Famille :** Catalogue académique

**Pertinence pour l’antenne :**
Détection précoce des recherches doctorales francophones en études radiophoniques.

**Point d’accès recommandé :**
API Export des données via data.gouv.fr ou OAI-PMH.<sup>28</sup>

**Pages officielles consultées :**
- https://www.data.gouv.fr/dataservices/api-export-des-donnees-de-theses-fr 28
- https://theses.fr/ 29

**Constats juridiques et techniques :**
- Base centralisée de l'Abes, largement partagée en Open Data gouvernemental.<sup>28</sup>

**Collecte privée autorisée ou raisonnable :**
Données bibliographiques complètes, informations sur les jurys et directeurs de recherche.

**Affichage public recommandé :**
Titre de la thèse, auteur, date de soutenance, URL vers la notice.

**Champs interdits en public :**
Résumés longs si non expressément libres.

**Attribution minimale :**
Source: theses.fr / Abes — lien.

**Rate limit / conditions techniques :**
Accès standard data.gouv.fr.

**Risques :**
Faible.

**Décision pratique pour sources.yaml :**
```yaml
active: true
raison : Exhaustivité sur la recherche française en devenir.
notes d’implémentation : Aucun obstacle technique majeur.
```

### BnF / Gallica


**Statut recommandé :** VALIDÉ

**Famille :** Catalogue institutionnel et archives

**Pertinence pour l’antenne :**
Essentiel pour l'archéologie des médias et la numérisation des anciennes revues de TSF ou radiodiffusion.

**Point d’accès recommandé :**
Entrepôts OAI-PMH (OAI-NUM pour les documents numérisés, OAI-CAT pour le catalogue).<sup>30</sup>

**Pages officielles consultées :**
- https://api.bnf.fr/fr/oai-num 30
- https://www.bnf.fr/fr/recuperer-des-notices-bibliographiques-en-dublin-core-oai-cat 31

**Constats juridiques et techniques :**
- Les métadonnées sont libérées sous la "Licence Ouverte de l'État", autorisant la libre réutilisation, y compris commerciale, sous condition de mention de source.<sup>31</sup>
- Le protocole OAI-PMH est documenté et structuré en Dublin Core XML.<sup>30</sup>

**Collecte privée autorisée ou raisonnable :**
Métadonnées, identifiants pérennes (ARK), récupération du texte brut OCRisé via l'API Document (/{ark}.texteBrut) pour analyse sémantique locale.<sup>32</sup>

**Affichage public recommandé :**
Titres, dates, auteurs, format, liens de résolution ARK.

**Champs interdits en public :**
La republication publique du texte intégral OCRisé sans contextualisation.

**Attribution minimale :**
Source: Bibliothèque nationale de France / Gallica — lien ARK.

**Rate limit / conditions techniques :**
Exploitation asynchrone par sets OAI.

**Risques :**
Très Faible. Soutien actif des pouvoirs publics à la réutilisation des données.

**Décision pratique pour sources.yaml :**
```yaml
active: true
raison : Stabilité des identifiants (ARK) et politique de données irréprochable.
notes d’implémentation : Convertir le modèle Dublin Core pour correspondre au format JSON interne.
```

### Sudoc / Abes


**Statut recommandé :** VALIDÉ

**Famille :** Catalogue académique / OAI-PMH

**Pertinence pour l’antenne :**
Localisation d'ouvrages physiques et théoriques sur les media studies dans le réseau universitaire français.

**Point d’accès recommandé :**
OAI-PMH.<sup>33</sup>

**Pages officielles consultées :**
- https://documentation.abes.fr/aidesudoc/EN/accueil/aidesudoc_index.html <sup>33</sup>
- https://documentation.abes.fr/aideidref/accueil/en/index.html <sup>34</sup>

**Constats juridiques et techniques :**
- Le système propose un dépôt OAI-PMH et des services web (IdRef) pour les données d'autorité, interopérables et sous Licence Ouverte.<sup>34</sup>

**Collecte privée autorisée ou raisonnable :**
Notices bibliographiques.

**Affichage public recommandé :**
Liens de localisation, titres, auteurs.

**Champs interdits en public :**
Dumps bruts MARC/XML.

**Attribution minimale :**
Source: Catalogue Sudoc / Abes — lien.

**Rate limit / conditions techniques :**
Traitement OAI-PMH standard.

**Risques :**
Faible.

**Décision pratique pour sources.yaml :**
```yaml
active: true
raison : Utile pour référencer des monographies clés introuvables en ligne.
notes d’implémentation : Extraction ciblée via ISBN ou IdRef.
```

### Isidore (Huma-Num)


**Statut recommandé :** VALIDÉ

**Famille :** Moteur de recherche académique SHS

**Pertinence pour l’antenne :**
Agrège massivement la recherche en Sciences Humaines et Sociales (SHS), incluant une vaste littérature francophone pertinente pour le projet.

**Point d’accès recommandé :**
API publique ISIDORE.<sup>35</sup>

**Pages officielles consultées :**
- https://isidore.science/cgu <sup>36</sup>
- https://documentation.huma-num.fr/en/isidore-en/ <sup>37</sup>

**Constats juridiques et techniques :**
- Moteur sémantique géré par l'infrastructure nationale Huma-Num. L'indexation comprend les métadonnées et, le cas échéant, le texte intégral en libre accès.<sup>38</sup>
- L'infrastructure est hébergée en France, respectant scrupuleusement le RGPD.<sup>37</sup>

**Collecte privée autorisée ou raisonnable :**
Résultats de recherche sémantique, métadonnées enrichies.

**Affichage public recommandé :**
Liens, titres, auteurs, disciplines.

**Champs interdits en public :**
Texte intégral des documents, annotations sémantiques propriétaires du moteur.

**Attribution minimale :**
Source: ISIDORE (Huma-Num) — lien.

**Rate limit / conditions techniques :**
Une API publique est accessible (parfois via un système de "laisser-passer").<sup>35</sup> Respecter des délais de requêtes modérés.

**Risques :**
Faible.

**Décision pratique pour sources.yaml :**
```yaml
active: true
raison : Outil de découverte spécialisé en SHS indispensable.
notes d’implémentation : S'assurer du bon routage des URL vers la source originale découverte par Isidore, plutôt que vers la seule notice Isidore.
```

### ORCID


**Statut recommandé :** VALIDÉ

**Famille :** Registre académique d'auteurs

**Pertinence pour l’antenne :**
Désambiguïsation des auteurs clés en études radiophoniques.

**Point d’accès recommandé :**
API publique ORCID.

**Pages officielles consultées :**
- N/A (Source standard académique).

**Constats juridiques et techniques :**
- L'API publique est ouverte pour consulter les profils publics des chercheurs.

**Collecte privée autorisée ou raisonnable :**
Identifiants, listes de publications.

**Affichage public recommandé :**
Lien vers le profil ORCID d'un auteur.

**Champs interdits en public :**
Données biographiques privées (non marquées comme publiques par l'utilisateur).

**Attribution minimale :**
Source: ORCID — lien.

**Rate limit / conditions techniques :**
Authentification requise pour l'API publique.

**Risques :**
Faible.

**Décision pratique pour sources.yaml :**
```yaml
active: false (à différer)
raison : Complexité technique de l'alignement des entités pour un projet naissant. Peut être intégré en phase 2.
```

### CiNii / NDL / J-STAGE


**Statut recommandé :** VALIDÉ

**Famille :** Plateformes académiques japonaises / API

**Pertinence pour l’antenne :**
Accès à la littérature asiatique, souvent pionnière en matière d'études sur la Mini-FM, les micro-radios et l'art sonore.

**Point d’accès recommandé :**
APIs (Formats JSON/RDF) du National Institute of Informatics (NII).<sup>39</sup>

**Pages officielles consultées :**
- https://support.nii.ac.jp/en/cinii/copyright <sup>41</sup>
- https://labs.ci.nii.ac.jp/en/termsofuse.html 42
- https://ndlsearch.ndl.go.jp/en/help/api/provider <sup>43</sup>

**Constats juridiques et techniques :**
- Le service est gratuit et régi par le droit japonais.<sup>42</sup>
- Les conditions d'utilisation (Linking Policy) exigent qu'il soit clairement indiqué que le service est fourni par le NII.<sup>41</sup> Les liens statiques sont libres de droits.<sup>41</sup>

**Collecte privée autorisée ou raisonnable :**
Recherche bibliographique.

**Affichage public recommandé :**
Titres, auteurs, liens vers le CRID (CiNii Research ID).

**Champs interdits en public :**
Dumps complets.

**Attribution minimale :**
Source: CiNii (National Institute of Informatics) — lien.

**Rate limit / conditions techniques :**
Interdiction stricte des actions interférant avec les serveurs de l'institut.<sup>42</sup> Mise en place d'un cache recommandée.

**Risques :**
Faible. API documentée pour un accès international.

**Décision pratique pour sources.yaml :**
```yaml
active: true
raison : Littérature unique sur les phénomènes de radios libres japonaises.
notes d’implémentation : Respecter scrupuleusement la clause d'attribution contractuelle au NII.
```

### INA (Institut National de l'Audiovisuel)


**Statut recommandé :** VALIDÉ PRUDENT

**Famille :** Archives institutionnelles

**Pertinence pour l’antenne :**
Gisement historique de la radiodiffusion française.

**Point d’accès recommandé :**
Plateforme data.gouv.fr pour les métadonnées.<sup>44</sup>

**Pages officielles consultées :**
- https://www.data.gouv.fr/organizations/institut-national-de-laudiovisuel <sup>44</sup>

**Constats juridiques et techniques :**
- L'INA diffuse publiquement des jeux de données de métadonnées (ex: Podcasts français archivés à l'INA) sur le portail open data de l'État.<sup>44</sup>
- Le contenu audiovisuel hébergé sur ina.fr relève du dépôt légal web et d'une gestion stricte des droits.<sup>44</sup>

**Collecte privée autorisée ou raisonnable :**
Ingestion des fichiers JSON/CSV fournis sur data.gouv.fr.

**Affichage public recommandé :**
Métadonnées factuelles, liens vers les notices publiques de ina.fr.

**Champs interdits en public :**
Toute tentative de moissonnage et de rediffusion des médias vidéo ou audio issus du lecteur web propriétaire.

**Attribution minimale :**
Source: INA via data.gouv.fr — lien vers la notice.

**Rate limit / conditions techniques :**
Téléchargement statique de fichiers. Aucun risque de blocage dynamique si l'on ne scrape pas ina.fr.

**Risques :**
Modéré. Risque légal nul sur l'Open Data, mais sévère en cas de scraping direct du site grand public.

**Décision pratique pour sources.yaml :**
```yaml
active: true (restreint aux datasets)
raison : Valorisation des bases de métadonnées de l'INA.
notes d’implémentation : Parser les exports statiques sans interroger les serveurs de production commerciaux.
```

### Unpaywall


**Statut recommandé :** VALIDÉ PRUDENT

**Famille :** API / Résolveur Open Access

**Pertinence pour l’antenne :**
Identification des versions gratuites et légales de publications sous péage.

**Point d’accès recommandé :**
REST API (api.unpaywall.org/v2/).<sup>45</sup>

**Pages officielles consultées :**
- https://unpaywall.org/products/api <sup>45</sup>
- https://docs.ropensci.org/roadoi/ <sup>46</sup>

**Constats juridiques et techniques :**
- L'API offre un accès gratuit à la base de données.<sup>45</sup>
- Requiert obligatoirement l'inclusion d'une adresse email comme paramètre dans l'URL pour identifier l'utilisateur et notifier en cas de problème.

**Collecte privée autorisée ou raisonnable :**
Vérification massive de listes de DOI.

**Affichage public recommandé :**
Le statut "Open Access" et l'URL vers le PDF légal (meilleure localisation OA).<sup>47</sup>

**Champs interdits en public :**
L'email utilisé pour l'authentification (doit être gardé secret dans les variables d'environnement).

**Attribution minimale :**
Source: Unpaywall — lien.

**Rate limit / conditions techniques :**
Le fournisseur impose une limite courtoise de 100 000 appels par jour.<sup>45</sup> Pour des volumes supérieurs, le téléchargement du dump complet de la base est exigé.<sup>46</sup>

**Risques :**
Faible, si l'email n'est pas exposé.

**Décision pratique pour sources.yaml :**
```yaml
active: true
raison : Améliore considérablement l'utilité de l'index public en pointant vers des PDF libres.
notes d’implémentation : Coder une vérification anti-fuite de l'email paramétré dans la requête.
```

### Radio France / France Culture


**Statut recommandé :** VALIDÉ PRUDENT

**Famille :** Média de service public / Open API

**Pertinence pour l’antenne :**
Acteur central de la création radiophonique et documentaire en France (ACR, fictions, magazines).

**Point d’accès recommandé :**
Open API de Radio France (developers.radiofrance.fr).<sup>48</sup>

**Pages officielles consultées :**
- https://www.radiofrance.com/lopen-api-radio-france <sup>48</sup>
- https://www.radiofrance.com/conditions-generales-dutilisation-des-sites-de-radio-france <sup>49</sup>

**Constats juridiques et techniques :**
- L'accès à l'Open API est gratuit, mais strictement réservé à un usage non commercial.<sup>48</sup>
- La création de compte développeur et la validation du projet (description de la finalité) par les équipes de Radio France sont nécessaires.<sup>48</sup>
- Il est explicitement interdit d'utiliser l'API pour créer des agrégateurs de flux live ou des agrégateurs de podcasts de substitution.<sup>48</sup> L'antenne universitaire doit se positionner comme un annuaire de découverte.

**Collecte privée autorisée ou raisonnable :**
Grilles, métadonnées d'émissions, tags, URL des podcasts, producteurs.

**Affichage public recommandé :**
title, url (pointant vers la page de l'émission sur radiofrance.fr), date, contributeurs.

**Champs interdits en public :**
Les fichiers audio directs ou l'intégration d'un lecteur tiers lisant les flux de Radio France.

**Attribution minimale :**
Source: Radio France / France Culture — lien vers l'émission.

**Rate limit / conditions techniques :**
Déterminées lors de la délivrance de la clé API. L'utilisation d'API tierces intégrées aux sites de Radio France (ex: YouTube, Google) est soumise à des CGU croisées.<sup>51</sup>

**Risques :**
Modéré. Le respect scrupuleux de l'interdiction de concurrence (agrégation audio) est impératif pour éviter la révocation de la clé.

**Décision pratique pour sources.yaml :**
```yaml
active: true
raison : Richesse de l'information pour l'esthétique sonore.
notes d’implémentation : Redirection du trafic vers le média d'origine. Les flux RSS alternatifs 52 ne doivent servir qu'à un usage purement privé de veille.
```

### Podcast Index


**Statut recommandé :** VALIDÉ PRUDENT

**Famille :** Annuaire de Podcasts / API

**Pertinence pour l’antenne :**
Découverte de séries indépendantes liées aux sound studies et à la création radiophonique. Indépendant des grandes plateformes fermées.

**Point d’accès recommandé :**
API REST (nécessite une clé).<sup>53</sup>

**Pages officielles consultées :**
- https://api-docs.podchaser.com/docs/rate-limits (Exemple de limites GraphQL analogues) <sup>54</sup>
- https://www.listennotes.help/article/109-listen-notes-podcast-api-rate-limits (Exemple des pratiques de l'industrie) <sup>55</sup>

**Constats juridiques et techniques :**
- L'API est communautaire et ouverte, visant à préserver l'écosystème ouvert du podcasting.
- Le moissonnage massif (batch scraping) est découragé en faveur des exports statiques fournis par l'organisation.<sup>55</sup>

**Collecte privée autorisée ou raisonnable :**
Titres, descriptions, métadonnées techniques, URL des flux RSS originaux.

**Affichage public recommandé :**
Liens vers les pages d'émission, titres, éditeurs.

**Champs interdits en public :**
Fichiers MP3, hotlinking massif d'illustrations de podcasts.

**Attribution minimale :**
Source: Podcast Index — lien.

**Rate limit / conditions techniques :**
L'en-tête User-Agent descriptif est impératif pour ne pas être bloqué.<sup>56</sup> Les limites de requêtes (exprimées en erreurs 429) doivent être respectées sous peine de bannissement.<sup>56</sup>

**Risques :**
Modéré.

**Décision pratique pour sources.yaml :**
```yaml
active: true
raison : Index ouvert, philosophie alignée avec la recherche universitaire.
notes d’implémentation : Privilégier les recherches ciblées par mots-clés plutôt qu'un balayage généraliste.
```

### Apple Podcasts


**Statut recommandé :** VALIDÉ STRICT

**Famille :** Annuaire commercial / Search API

**Pertinence pour l’antenne :**
L'index le plus exhaustif de la scène du podcast. Utile pour identifier des créations radiophoniques internationales.

**Point d’accès recommandé :**
iTunes Search API (itunes.apple.com/search).

**Pages officielles consultées :**
- https://developer.apple.com/documentation/appstoreconnectapi/identifying-rate-limits <sup>57</sup>
- https://performance-partners.apple.com/search-api <sup>58</sup>

**Constats juridiques et techniques :**
- API de recherche publique existante. L'infrastructure limite les appels à environ 20 appels par minute par client (limite sujette à variation).<sup>58</sup>
- Pour un usage plus intensif, Apple recommande l'Enterprise Partner Feed (EPF), inadapté à un petit projet universitaire.<sup>58</sup>

**Collecte privée autorisée ou raisonnable :**
Données descriptives des émissions.

**Affichage public recommandé :**
Titre, auteur, URL vers l'interface Apple Podcasts.

**Champs interdits en public :**
Fichiers médias, descriptions complètes sous copyright de l'éditeur.

**Attribution minimale :**
Source: Apple Podcasts — lien.

**Rate limit / conditions techniques :**
Temporisation stricte de 3 secondes minimum entre chaque requête pour éviter le blocage de l'IP du serveur.<sup>58</sup> Utilisation du paramètre limit pour restreindre la taille des paquets.<sup>58</sup>

**Risques :**
Modéré.

**Décision pratique pour sources.yaml :**
```yaml
active: true (Usage de complément)
raison : Utile pour la veille, mais fragile techniquement.
notes d’implémentation : Mécanisme de cache local indispensable pour minimiser les appels à l'API Apple.
```

### Cairn / Persée / Érudit


**Statut recommandé :** VALIDÉ STRICT

**Famille :** Plateformes de revues SHS francophones

**Pertinence pour l’antenne :**
Contiennent les articles phares en sociologie et histoire de la radio.

**Point d’accès recommandé :**
OAI-PMH (Persée, Érudit). Le web scraping HTML est fortement déconseillé pour Cairn.<sup>61</sup>

**Pages officielles consultées :**
- https://info.persee.fr/fouille-de-donnees/ <sup>63</sup>
- https://apropos.erudit.org/technologies/?lang=en <sup>64</sup>

**Constats juridiques et techniques :**
- Érudit maintient un OAI-PMH public (format OAI-DC et NLM) pour la collecte des métadonnées des revues de sa plateforme.<sup>64</sup>
- Persée propose des services web ("Autorités") et de l'OAI-PMH, mais la fouille de texte massive requiert une concertation avec l'institution.<sup>63</sup>
- Cairn dispose de conditions d'utilisation restrictives concernant l'aspiration de pages et l'alimentation de systèmes tiers d'IA ou de bases de données.<sup>61</sup>

**Collecte privée autorisée ou raisonnable :**
Métadonnées bibliographiques (titres, auteurs, numéros, résumés courts via OAI).

**Affichage public recommandé :**
title, auteurs, revue, date, liens vers l'URL officielle (évitant tout paywall).

**Champs interdits en public :**
Extraction par force brute (scraping HTML) du texte intégral des articles.

**Attribution minimale :**
Source: Cairn / Persée / Érudit — lien vers la page de l'article.

**Rate limit / conditions techniques :**
Privilégier exclusivement les endpoints OAI-PMH ou les flux RSS.

**Risques :**
Modéré (si scraping sauvage), Faible (si cantonné à l'OAI-PMH).

**Décision pratique pour sources.yaml :**
```yaml
active: true
raison : Indispensable à la veille universitaire.
notes d’implémentation : Bannir BeautifulSoup/Selenium sur ces domaines. Restreindre l'antenne au parsing XML des flux officiels.
```

### Sources RSS, Revues et Blogs (Radio Survivor, Radiomorphoses, Sounding Out!, etc.)


**Statut recommandé :** VALIDÉ STRICT

**Famille :** Flux de syndication d'actualités et revues indépendantes

**Pertinence pour l’antenne :**
Cœur de la veille de l'actualité de la recherche, des appels à communications (CFP), et des réflexions sur les sound studies.

**Point d’accès recommandé :**
Flux RSS ou Atom originaux.

**Pages officielles consultées :**
- https://journals.openedition.org/radiomorphoses/?lang=en <sup>66</sup>
- https://www.radiosurvivor.com/ <sup>67</sup>
- https://soundstudiesblog.com/ <sup>68</sup>

**Constats juridiques et techniques :**
- Les revues hébergées sur OpenEdition (comme Radiomorphoses) bénéficient du dépôt OAI-PMH d'OpenEdition (bien que la version v1 soit en cours de dépréciation au profit de la v2).<sup>12</sup>
- Les blogs (Sounding Out!, Radio Survivor, La Lettre Pro) utilisent des CMS standards (WordPress) émettant des flux RSS publics.<sup>67</sup>
- Si le droit autorise la lecture d'un flux, la duplication d'un article entier (content:encoded) sur un site tiers porte préjudice à l'éditeur et viole le droit d'auteur.<sup>5</sup>

**Collecte privée autorisée ou raisonnable :**
Ingestion des balises <title>, <link>, <pubDate>, et <description> pour le traitement linguistique privé.

**Affichage public recommandé :**
title, url originale, date de publication, nom du blog.

**Champs interdits en public :**
Contenu intégral, balises <description> si elles constituent une part substantielle de l'article, images sans contexte.

**Attribution minimale :**
Source: — lien direct.

**Rate limit / conditions techniques :**
Pour soulager les serveurs des petits éditeurs (Radio Fañch, Les Radios Libres), le pipeline doit effectuer un téléchargement journalier unique. L'utilisation des en-têtes HTTP If-Modified-Since et ETag est requise.

**Risques :**
Modéré. Le risque d'infraction naîtrait de la republication publique accidentelle du contenu complet des articles.

**Décision pratique pour sources.yaml :**
```yaml
active: true
raison : Les blogs sont les senseurs primaires de l'actualité de la discipline.
notes d’implémentation : Filtre strict lors de la compilation Hugo pour s'assurer qu'aucun résumé étendu n'est généré.
```

### Journaux académiques propriétaires (ex: Journal of Radio & Audio Media)


**Statut recommandé :** VALIDÉ STRICT

**Famille :** Revues à comité de lecture (Grandes maisons d'édition)

**Pertinence pour l’antenne :**
Publications de pointe de la recherche mondiale en médias audio (Taylor & Francis, etc.).

**Point d’accès recommandé :**
Flux RSS de la revue ou extraction via Crossref.

**Pages officielles consultées :**
- N/A (Les éditeurs académiques majeurs possèdent des CGU d'une grande sévérité).

**Constats juridiques et techniques :**
- L'aspiration des pages web de ces éditeurs est formellement interdite sans accord institutionnel de TDM.
- Les métadonnées restent accessibles légalement via des agrégateurs comme Crossref ou OpenAlex.

**Collecte privée autorisée ou raisonnable :**
Titres, auteurs, DOI, résumés (via API académiques légitimes).

**Affichage public recommandé :**
title, auteurs, DOI, lien.

**Champs interdits en public :**
Résumés (souvent protégés par le copyright de l'éditeur dans ce contexte précis), URL directes de PDF piratés (ex: Sci-Hub).

**Attribution minimale :**
Source: [Nom de la revue] — lien DOI.

**Rate limit / conditions techniques :**
S'appuyer sur l'infrastructure de Crossref plutôt que d'interagir directement avec le serveur de l'éditeur.

**Risques :**
Modéré.

**Décision pratique pour sources.yaml :**
```yaml
active: false pour le scraping web direct.
active: true pour le suivi des alertes RSS et de Crossref.
```

### BBC Sounds / NPR / ARTE Radio


**Statut recommandé :** VALIDÉ STRICT

**Famille :** Médias audiovisuels publics et affiliés / RSS

**Pertinence pour l’antenne :**
Production sonore internationale de haute qualité (documentaires, narrations complexes, créations).

**Point d’accès recommandé :**
Flux RSS publics de podcasting.<sup>14</sup>

**Pages officielles consultées :**
- https://podcasts.apple.com/us/artist/arte-radio/1251092473 <sup>14</sup>

**Constats juridiques et techniques :**
- Ces médias distribuent leurs contenus via des flux RSS ouverts destinés aux applications de lecture (podcatchers).<sup>5</sup>
- Les contenus intégraux sont lourdement protégés.

**Collecte privée autorisée ou raisonnable :**
Titres de séries, épisodes, dates.

**Affichage public recommandé :**
Liens de redirection vers la page web d'écoute de l'éditeur (ex: page de l'épisode sur arteradio.com).

**Champs interdits en public :**
Balises <enclosure> contenant le fichier MP3, transcriptions éventuelles de l'audio non placées dans le domaine public.

**Attribution minimale :**
Source: [Nom du média] — lien d'écoute.

**Rate limit / conditions techniques :**
Requêtage très distancié (une fois par jour).

**Risques :**
Modéré. Le contournement des régies publicitaires ou des lecteurs institutionnels expose à des plaintes.

**Décision pratique pour sources.yaml :**
```yaml
active: true
raison : Analyse de la création sonore contemporaine.
notes d’implémentation : Ne stocker en public que l'URL canonique web, ignorer l'URL du fichier média.
```

### Internet Archive / Library of Congress


**Statut recommandé :** À REPORTER

**Famille :** Archives institutionnelles internationales

**Pertinence pour l’antenne :**
Fonds historiques massifs sur la radio nord-américaine et les médias du monde entier.

**Point d’accès recommandé :**
APIs de recherche.

**Pages officielles consultées :**
- N/A

**Constats juridiques et techniques :**
- L'Internet Archive traverse une période de fortes incertitudes juridiques (contentieux liés au droit d'auteur, National Emergency Library). Les politiques de leurs APIs de recherche risquent d'évoluer de manière imprévisible.
- La Library of Congress dispose d'APIs puissantes, mais l'intégration requiert une analyse approfondie des formats de données complexes (MARC).

**Collecte privée autorisée ou raisonnable :**
Métadonnées publiques de recherche.

**Risques :**
Incertain. La maintenance d'un connecteur API pour ces plateformes à ce stade du projet engendrerait une dette technique prématurée.

**Décision pratique pour sources.yaml :**
```yaml
active: false
raison : Trop lourd techniquement pour le lancement. À considérer pour une "V3" du projet.
```

### Spotify / Deezer / SoundCloud / Mixcloud


**Statut recommandé :** À ÉVITER

**Famille :** Plateformes commerciales de streaming musical et audio / Web API

**Pertinence pour l’antenne :**
Hébergent des créations sonores exclusives, des mixtapes et certains podcasts non diffusés via RSS ouvert.

**Point d’accès recommandé :**
API REST propriétaires (Spotify Web API).

**Pages officielles consultées :**
- https://developer.spotify.com/blog/2026-02-06-update-on-developer-access-and-platform-security <sup>69</sup>
- https://developer.spotify.com/documentation/web-api/concepts/rate-limits <sup>70</sup>
- https://developers.deezer.com/termsofuse <sup>71</sup>

**Constats juridiques et techniques :**
- L'écosystème Spotify s'est radicalement fermé aux développeurs indépendants début 2026. L'accès en mode développement a été considérablement restreint (nécessite un compte Premium, limité à un seul ID client et 5 utilisateurs).<sup>69</sup>
- L'obtention d'un mode "Extended quota" sur Spotify exige d'être une société enregistrée commercialement, possédant déjà 250 000 utilisateurs actifs mensuels.<sup>69</sup>
- Les CGU de Deezer limitent l'API à un usage non commercial et imposent le respect strict de leurs contraintes de propriété intellectuelle.<sup>71</sup>

**Collecte privée autorisée ou raisonnable :**
Techniquement infaisable à moyenne échelle sans risquer la révocation immédiate du compte développeur (Erreurs 429 systématiques).<sup>70</sup>

**Affichage public recommandé :**
AUCUN (Ne pas dépendre de ces plateformes pour générer des liens).

**Champs interdits en public :**
TOUS.

**Attribution minimale :**
N/A

**Rate limit / conditions techniques :**
Spotify opère sur une fenêtre de calcul du taux d'appel de 30 secondes extrêmement stricte.<sup>70</sup>

**Risques :**
Élevé (Hostilité déclarée envers les initiatives tierces indépendantes).

**Décision pratique pour sources.yaml :**
```yaml
active: false
raison : La dépendance à une architecture fermée et instable est contraire aux principes d'un outil universitaire open source.
notes d’implémentation : Contourner le problème en identifiant ces mêmes contenus via Podcast Index ou Crossref lorsque possible.
```

### WorldCat (OCLC)


**Statut recommandé :** INTERDIT POUR EXPORT PUBLIC / PRIVÉ SEULEMENT (MANUEL)

**Famille :** Catalogue coopératif mondial

**Pertinence pour l’antenne :**
Notice bibliographique universelle, recense toutes les monographies relatives à la radio.

**Point d’accès recommandé :**
Aucun accès automatisé autorisé pour ce type de projet.

**Pages officielles consultées :**
- https://www.oclc.org/content/dam/ext-ref/worldcat-org/terms.html <sup>73</sup>
- https://www.oclc.org/developer/api/oclc-apis/worldcat-search-api.en.html <sup>74</sup>

**Constats juridiques et techniques :**
- Les Conditions d'Utilisation de WorldCat.org interdisent de manière absolue : l'extraction automatisée (bots, scraping), la capture en vrac, le stockage à long terme, la divulgation ou republication des données, et la création de bases de données dérivées.<sup>73</sup>
- L'usage est limité de façon draconienne à un cadre "Non Commercial" strictement personnel pour la découverte de ressources (usage humain via navigateur).<sup>73</sup>
- L'accès légitime à l'API de recherche (Search API) nécessite de cumuler un abonnement institutionnel au catalogage complet d'OCLC et une souscription à WorldCat Discovery, hors de portée d'un projet de veille individuel/universitaire autonome.<sup>74</sup>

**Collecte privée autorisée ou raisonnable :**
Consultation manuelle et saisie humaine uniquement.

**Affichage public recommandé :**
AUCUN.

**Champs interdits en public :**
Tous les champs, identifiants (OCLC number) et URL.

**Attribution minimale :**
N/A

**Rate limit / conditions techniques :**
Protections techniques anti-bots robustes et menaces d'action en justice explicites en cas de violation des systèmes de sécurité.<sup>73</sup>

**Risques :**
Critique. OCLC exerce un contrôle monopolistique reconnu sur ses métadonnées bibliographiques et n'hésite pas à restreindre les accès.<sup>75</sup>

**Décision pratique pour sources.yaml :**
```yaml
active: false
raison : Incompatibilité juridique fondamentale avec le concept d'agrégation automatisée.
notes d’implémentation : Remplacer systématiquement ce manque par la consultation d'archives ouvertes européennes ou nationales (Sudoc, BnF, HAL, OpenAlex) dont la gouvernance favorise la découvrabilité.
```

## 20. Sources recommandées à ajouter

Durant l'exécution de cet audit, plusieurs plateformes initialement non envisagées ont démontré une compatibilité technique parfaite et une forte pertinence thématique. Elles doivent être intégrées en priorité :

- **DOAJ (Directory of Open Access Journals) :** Pour filtrer et valoriser la recherche nativement ouverte. Son API documentée est un standard de la profession.
- **OpenAlex :** Révolutionnant la bibliométrie, ce graphe massif permet de contourner le scraping pénible de multiples micro-revues en centralisant leurs identifiants DOI. Son statut CC0 efface les risques juridiques.<sup>19</sup>
- **Data.gouv.fr (Jeux de données de l'INA) :** La découverte d'exports ouverts relatifs aux podcasts de l'INA offre une opportunité de contourner l'interdiction de scraper les plateformes propriétaires.<sup>44</sup>

## 21. Sources à reporter ou éviter

- **WorldCat (OCLC) :** Constitue un risque juridique disproportionné pour la viabilité de l'antenne radio.<sup>73</sup>
- **Spotify & Deezer :** L'écosystème fermé de ces géants du streaming, couplé à de récentes durcissements contractuels visant expressément l'éviction des développeurs tiers non commerciaux, rend toute pérennité technique impossible.<sup>69</sup>
- **Internet Archive :** À reporter sine die, en attente de clarification des batailles judiciaires en cours aux États-Unis influençant la disponibilité de leurs APIs.

## 22. Recommandations concrètes pour config/sources.yaml

Afin de matérialiser les exigences sécuritaires identifiées, la configuration logicielle doit embarquer la logique d'audit. Le fichier sources.yaml définira non seulement l'URL, mais imposera la stratégie de temporisation et le filtrage (whitelisting) des données vers le fichier final.
Exemple d'implémentation attendue pour le module Python ou Go assurant la collecte :

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
      # Application stricte de la politique "Whitelist" de l'audit.
      allowed_fields: ["id", "title", "url", "doi", "published_at", "authors", "source_name", "legal_status"]
      drop_fields: ["abstract", "raw", "logs"]

  - id: "openalex_media_studies"
    name: "OpenAlex"
    family: "catalogue_global"
    active: true
    type: "api_rest"
    url: "https://api.openalex.org/works"
    rate_limit:
      delay_seconds: 1
    security:
      auth_required: true
      env_key: "OPENALEX_API_KEY" # Chargé depuis.env, jamais commité
    export_policy:
      allowed_fields: ["id", "title", "url", "doi", "published_at", "authors", "source_name"]
```

## 23. Recommandations concrètes pour l'export public JSON

Le pont entre la base locale (ex: veille.sqlite ou un répertoire riche de fichiers JSON bruts) et le site Hugo doit être assuré par un script de conversion rigide. Ce script doit :

1. Lire la base de données privée.
2. Itérer sur chaque ressource.
3. Créer un nouvel objet dictionnaire vide.
4. Transférer uniquement les clés présentes dans la liste allowed_fields de la export_policy de la source concernée.
5. Si un champ contient des chaînes sensibles par accident (ex: un email machinalement absorbé dans le champ authors), appliquer une expression régulière (Regex) de nettoyage.
6. Écrire le résultat dans un fichier public_index.json qui sera le seul artefact copié dans le dossier data/ de l'arborescence Hugo.

## 24. Tests anti-fuite à implémenter (CI/CD)

Pour parer à la défaillance humaine (une clé d'API oubliée, un abstract protégé exposé suite au changement de format d'une API source), l'intégration de tests unitaires locaux ou via GitHub Actions/GitLab CI est indispensable.

- **Test `test_no_secrets` :** Le test scanne le fichier généré public_index.json à la recherche des chaînes api_key=, Bearer , mailto=, ou d'expressions régulières ciblant des adresses email standards. S'il en trouve, le script de déploiement doit échouer (Exit 1).
- **Test `test_no_copyrighted_content` :** Le test s'assure qu'aucune clé nommée abstract, summary, description, content, ou content:encoded ne figure dans l'export. Il peut également mesurer la longueur de la chaîne title ; si un titre dépasse 500 caractères, une alerte est levée (suspectant qu'un abstract a été injecté par erreur dans le champ titre).
- **Test `test_whitelist_adherence` :** Valide que toutes les clés présentes dans l'artefact public appartiennent au sous-ensemble autorisé édicté dans la section 7 du présent audit.

## 25. Checklist avant publication (Go-Live)

Avant le tout premier déploiement public sur le serveur d'hébergement, le concepteur du projet devra valider les points de contrôle suivants :

- [ ] L'en-tête HTTP User-Agent est défini au nom explicite du projet ("Antenne Radio/1.0 - Projet universitaire"), incluant l'URL du dépôt de code.
- [ ] Le paramètre `mailto:` (requis par Unpaywall et Crossref) est renseigné via des variables d'environnement locales et n'apparaît pas en clair dans les scripts Python/Go.
- [ ] Le fichier `.gitignore` a été audité et mentionne bien les répertoires hébergeant les dumps bruts (raw/, logs/, *.sqlite, .env).
- [ ] Les mécanismes de limitation de débit (`sleep`, backoff exponentiel) gèrent gracieusement les codes HTTP 429 et 403, suspendant la collecte au lieu d'insister.
- [ ] Le site public Hugo contient une mention légale claire ("À propos") précisant la nature documentaire et académique du projet, le fait qu'il ne détient aucun droit sur les données indexées, et dirigeant expressément l'audience vers les institutions d'origine pour toute demande de retrait.
- [ ] Les sources blacklistées (WorldCat, Spotify) sont définitivement retirées de l'architecture.

## 26. Bibliographie et sitographie des pages officielles consultées

Afin de garantir la traçabilité des assertions juridiques et techniques du présent audit, les ressources documentaires institutionnelles suivantes ont été étudiées :

- **CNIL (Commission Nationale de l'Informatique et des Libertés) :** Focus sur l'intérêt légitime et collecte de données par moissonnage (web scraping). 2
- **INRAE :** Recommandations sur les usages du webscraping au sein de la recherche publique (Directive européenne du droit d'auteur 2019/790, exception TDM). 1
- **APP (Agence pour la Protection des Programmes) :** Le web scraping légal et le droit sui generis des bases de données (Art. L. 342-3 du CPI). 4
- **OAI-PMH (Open Archives Initiative) :** Protocol for Metadata Harvesting (Spécifications V2.0). [11]
- **HAL (Archives Ouvertes) :** Principes, documentation API SolR et serveur OAI. [10, 15, 16, 17]
- **OpenAlex :** Documentation développeurs (Rate limits, Authentification, Licences CC0). [7, 18, 19, 76]
- **Crossref :** Metadata retrieval, Terms of use, Metadata Plus. [8, 9, 20]
- **Europeana :** API FAQ, Terms of Use. [25, 26, 27]
- **WorldCat / OCLC :** WorldCat Search API Terms and Conditions (Interdiction stricte). [73, 74]
- **Radio France :** Portail Open API (developers.radiofrance.fr) et CGU. [48, 49, 50]
- **OpenEdition :** Documentation de l'entrepôt OAI-PMH (OAI-PMH v2, formats oai_dc, mods). 12
- **BnF / Gallica :** Entrepôts OAI-NUM, OAI-CAT, et API Document (Licence Ouverte). [30, 31, 32]
- **Érudit :** Documentation des technologies de diffusion et Public OAI. 64
- **Persée :** Fouille de données et webservices de l'UAR Persée. [63, 77]
- **Cairn :** Mention de la protection contre l'aspiration des bases. [61, 78]
- **CiNii / NII :** Terms of Use et Copyright. [41, 42]
- **DOAJ :** Infrastructures et API de l'annuaire ouvert. [21, 23, 24]
- **Theses.fr (Abes) :** API Export des données. 28
- **Isidore (Huma-Num) :** CGU du moteur de recherche et documentation d'infrastructure. [36, 37, 38]
- **Unpaywall :** REST API Overview (Rate limits, Authentification). ``
- **Spotify :** Web API Concepts, Terms of Use (Restrictions sur l'accès développeur indépendant). [69, 70]
- **Apple Podcasts :** Search API (Documentation App Store Connect). [57, 58]
- **Podcast Index :** Docs API, informations sur le Query Cost et le Rate limit. [54, 55]
- **Data.gouv.fr / INA :** Jeux de données ouverts de l'Institut National de l'Audiovisuel. [44, 79]

## Sources des citations

1. Recommandations sur les usages du webscraping au sein d'INRAE, consulté le mai 20, 2026, https://science-ouverte.inrae.fr/fr/offre-service/fiches-pratiques-et-recommandations/recommandations-sur-les-usages-du-webscraping-au-sein-dinrae
2. La base légale de l'intérêt légitime : fiche focus sur les mesures à ..., consulté le mai 20, 2026, https://www.cnil.fr/fr/focus-interet-legitime-collecte-par-moissonnage
3. The legal basis of legitimate interest: focus sheet on the measures to implement in the case of data collection by web scraping | CNIL, consulté le mai 20, 2026, https://www.cnil.fr/en/legal-basis-legitimate-interest-focus-sheet-measures-implement-case-data-collection-web-scraping
4. Le Web Scraping est-il légal ?, consulté le mai 20, 2026, https://www.app.asso.fr/preuve-digitale/web-scraping-legal.html
5. Podcast, mode d'emploi - Audioblogs - ARTE Radio, consulté le mai 20, 2026, https://audioblog.arteradio.com/article/137732/podcast-mode-d-emploi
6. What is an API and OAI-PMH? - Figshare, consulté le mai 20, 2026, https://info.figshare.com/user-guide/what-is-an-api-and-oai-pmh/
7. Authentication & Pricing - OpenAlex Developers, consulté le mai 20, 2026, https://developers.openalex.org/api-reference/authentication <sup>8</sup>. Announcing changes to REST API rate limits - Crossref, consulté le mai 20, 2026, https://www.crossref.org/blog/announcing-changes-to-rest-api-rate-limits/ <sup>9</sup>. Documentation - Metadata Retrieval - Crossref, consulté le mai 20, 2026, https://www.crossref.org/documentation/retrieve-metadata/ <sup>10</sup>. Principles - About HAL, consulté le mai 20, 2026, https://about.hal.science/en/principles/ <sup>11</sup>. Protocol for Metadata Harvesting - v.<sup>2</sup>.0 - Open Archives Initiative, consulté le mai 20, 2026, https://www.openarchives.org/OAI/openarchivesprotocol.html
12. OpenEdition OAI-PMH repository Documentation — OpenEdition ..., consulté le mai 20, 2026, https://oai-openedition.readthedocs.io/
13. The Legal Landscape of Web Scraping - Quinn Emanuel, consulté le mai 20, 2026, https://www.quinnemanuel.com/the-firm/publications/the-legal-landscape-of-web-scraping/
14. ARTE Radio - Apple Podcasts, consulté le mai 20, 2026, https://podcasts.apple.com/us/artist/arte-radio/1251092473 <sup>15</sup>. Serveur OAI-PMH - Documentation API-HAL, consulté le mai 20, 2026, https://api.archives-ouvertes.fr/docs/oai <sup>16</sup>. Documentation API-HAL | API Archive Ouverte HAL, consulté le mai 20, 2026, https://api.archives-ouvertes.fr/
17. API HAL API de recherche HAL, consulté le mai 20, 2026, https://api.archives-ouvertes.fr/docs/search <sup>18</sup>. New Features and Usage-Based Pricing - OpenAlex blog, consulté le mai 20, 2026, https://blog.openalex.org/openalex-api-new-features-and-usage-based-pricing/ <sup>19</sup>. API keys required starting Feb 13 (and some new endpoints!) - Google Groups, consulté le mai 20, 2026, https://groups.google.com/g/openalex-users/c/rI1GIAySpVQ
20. License information - Crossref, consulté le mai 20, 2026, https://www.crossref.org/documentation/schema-library/markup-guide-metadata-segments/license-information/
21. DOAJ Application Guide for OJS Journals - PKP Docs, consulté le mai 20, 2026, https://docs.pkp.sfu.ca/doaj/en/ <sup>22</sup>. How I use DOAJ metadata in my work and research, consulté le mai 20, 2026, https://blog.doaj.org/2025/06/15/how-i-use-doaj-metadata-in-my-work-and-research/ <sup>23</sup>. Searching the Directory of Open Access Journals (DOAJ) - Nested Knowledge, consulté le mai 20, 2026, https://about.nested-knowledge.com/docs/searching-the-directory-of-open-access-journals-doaj/
24. Infrastructure and why sustainable funding so important to services like DOAJ, consulté le mai 20, 2026, https://blog.doaj.org/2018/10/01/infrastructure-and-why-sustainable-funding-so-important-to-services-like-doaj/
25. API FAQ - Europeana Knowledge Base - Confluence, consulté le mai 20, 2026, https://europeana.atlassian.net/wiki/spaces/EF/pages/2360508417
26. Terms of Use - Europeana, consulté le mai 20, 2026, https://www.europeana.eu/en/rights/terms-of-use <sup>27</sup>. consulté le mai 20, 2026, https://europeana.atlassian.net/wiki/spaces/EF/pages/2360508417#:~:text=Europeana%20gives%20access%20to%20all,have%20limitations%20posed%20upon%20them.
28. API Export des Données de theses.fr - Data gouv, consulté le mai 20, 2026, https://www.data.gouv.fr/dataservices/api-export-des-donnees-de-theses-fr
29. Theses.fr, consulté le mai 20, 2026, https://theses.fr/
30. Entrepôt OAI-PMH de Gallica et des expositions virtuelles (OAI-NUM) | BnF API et jeux de données, consulté le mai 20, 2026, https://api.bnf.fr/fr/oai-num
31. Récupérer des notices bibliographiques en Dublin Core (OAI-CAT) | BnF - Site institutionnel, consulté le mai 20, 2026, https://www.bnf.fr/fr/recuperer-des-notices-bibliographiques-en-dublin-core-oai-cat
32. API Document de Gallica | BnF API et jeux de données, consulté le mai 20, 2026, https://api.bnf.fr/fr/api-document-de-gallica
33. Help for the Sudoc catalogue - Documentation ABES, consulté le mai 20, 2026, https://documentation.abes.fr/aidesudoc/EN/accueil/aidesudoc_index.html <sup>34</sup>. IdRef - Documentation ABES, consulté le mai 20, 2026, https://documentation.abes.fr/aideidref/accueil/en/index.html <sup>35</sup>. Cas d'usage API publique avec laisser-passer - Huma Num - ORCID France, consulté le mai 20, 2026, https://orcid-france.fr/cas-usage/cas-usage-api-publique-avec-laisser-passer-huma-num/
36. Conditions Générales d'Utilisation (CGU) du service isidore.science, consulté le mai 20, 2026, https://isidore.science/cgu <sup>37</sup>. ISIDORE (en) - Documentation de l'infrastructure Huma-Num, consulté le mai 20, 2026, https://documentation.huma-num.fr/en/isidore-en/ <sup>38</sup>. ISIDORE (fr) - Documentation de l'infrastructure Huma-Num, consulté le mai 20, 2026, https://documentation.huma-num.fr/isidore/
39. Metadata and API - CiNii Articles RDF for Authors | Support Academic Information Services, consulté le mai 20, 2026, https://support.nii.ac.jp/en/cia/api/a_rdf_auth
40. Metadata and API - CiNii Articles JSON-LD for Authors (Beta) - 国立情報学研究所, consulté le mai 20, 2026, https://support.nii.ac.jp/en/cia/api/a_json_auth
41. CiNii - Copyright and Linking | Support Academic Information Services, consulté le mai 20, 2026, https://support.nii.ac.jp/en/cinii/copyright <sup>42</sup>. Terms of Use - CiNii Labs, consulté le mai 20, 2026, https://labs.ci.nii.ac.jp/en/termsofuse.html
43. The list of API-providing databases | NDL Search | National Diet Library, consulté le mai 20, 2026, https://ndlsearch.ndl.go.jp/en/help/api/provider <sup>44</sup>. Institut national de l'audiovisuel INA - Data gouv, consulté le mai 20, 2026, https://www.data.gouv.fr/organizations/institut-national-de-laudiovisuel <sup>45</sup>. REST API - Unpaywall, consulté le mai 20, 2026, https://unpaywall.org/products/api <sup>46</sup>. Find Free Versions of Scholarly Publications via Unpaywall • roadoi - Docs - rOpenSci, consulté le mai 20, 2026, https://docs.ropensci.org/roadoi/ <sup>47</sup>. Fetch open access status information and full-text links using Unpaywall — oadoi_fetch • roadoi - Docs, consulté le mai 20, 2026, https://docs.ropensci.org/roadoi/reference/oadoi_fetch.html
48. L'open API Radio France | Radio France, consulté le mai 20, 2026, https://www.radiofrance.com/lopen-api-radio-france <sup>49</sup>. Conditions générales d'utilisation des sites de Radio France, consulté le mai 20, 2026, https://www.radiofrance.com/conditions-generales-dutilisation-des-sites-de-radio-france <sup>50</sup>. radiofrance/communication - GitHub, consulté le mai 20, 2026, https://github.com/radiofrance/communication
51. Protection des données personnelles et politique de confidentialité à Radio France, consulté le mai 20, 2026, https://www.radiofrance.com/protection-des-donnees
52. RSS Radio France pour tous - Framalibre, consulté le mai 20, 2026, https://framalibre.org/notices/rss-radio-france-pour-tous.html
53. API Docs | PodcastIndex.org, consulté le mai 20, 2026, https://podcastindex-org.github.io/docs-api/
54. Rate Limits | Podchaser Enterprise API — GraphQL Documentation, consulté le mai 20, 2026, https://api-docs.podchaser.com/docs/rate-limits <sup>55</sup>. Listen Notes Podcast API Rate Limits, consulté le mai 20, 2026, https://www.listennotes.help/article/109-listen-notes-podcast-api-rate-limits <sup>56</sup>. Ratelimiting · Issue #30 · Podcastindex-org/docs-api - GitHub, consulté le mai 20, 2026, https://github.com/Podcastindex-org/docs-api/issues/30
57. Identifying Rate Limits | Apple Developer Documentation, consulté le mai 20, 2026, https://developer.apple.com/documentation/appstoreconnectapi/identifying-rate-limits <sup>58</sup>. iTunes Search API - Apple Services Performance Partners, consulté le mai 20, 2026, https://performance-partners.apple.com/search-api <sup>59</sup>. iTunes Search API rate limit - Stack Overflow, consulté le mai 20, 2026, https://stackoverflow.com/questions/12596300/itunes-search-api-rate-limit
60. Is iTunes Search API Rate Limit per device or per app? - Stack Overflow, consulté le mai 20, 2026, https://stackoverflow.com/questions/41290585/is-itunes-search-api-rate-limit-per-device-or-per-app
61. Web scraping : avec quelles données peut-on nourrir l'intelligence artificielle (IA), consulté le mai 20, 2026, https://droit.cairn.info/revue-dpo-news-2025-3-page-7?lang=fr
62. Modular Rules & Procedures - Cairn RPG, consulté le mai 20, 2026, https://cairnrpg.com/hacks/third-party/modular-rules-procedures/
63. Fouille de données - Persée UAR, consulté le mai 20, 2026, https://info.persee.fr/fouille-de-donnees/ <sup>64</sup>. Technology - Érudit, consulté le mai 20, 2026, https://apropos.erudit.org/technologies/?lang=en <sup>65</sup>. A quick guide for SSHRC's Aid to Scholarly Journals 2025 - Érudit, consulté le mai 20, 2026, https://www.erudit.org/public/documents/Guide_ASJ_2025_ENG.pdf
66. RadioMorphoses - Revue d'études radiophoniques et sonores - OpenEdition Journals, consulté le mai 20, 2026, https://journals.openedition.org/radiomorphoses/?lang=en <sup>67</sup>. Broadcast the Radio Survivor show on your radio station, consulté le mai 20, 2026, https://www.radiosurvivor.com/radio/
68. Sounding Out! | pushing sound studies into the red since 2009, consulté le mai 20, 2026, https://soundstudiesblog.com/ <sup>69</sup>. Update on Developer Access and Platform Security, consulté le mai 20, 2026, https://developer.spotify.com/blog/2026-02-06-update-on-developer-access-and-platform-security <sup>70</sup>. Rate Limits - Spotify for Developers, consulté le mai 20, 2026, https://developer.spotify.com/documentation/web-api/concepts/rate-limits <sup>71</sup>. Terms of use of Deezer for Developers, consulté le mai 20, 2026, https://developers.deezer.com/termsofuse <sup>72</sup>. Spotify just killed indie development with their new API restrictions : r/truespotify - Reddit, consulté le mai 20, 2026, https://www.reddit.com/r/truespotify/comments/1l2am4i/spotify_just_killed_indie_development_with_their/
73. WorldCat Terms and Conditions - OCLC, consulté le mai 20, 2026, https://www.oclc.org/content/dam/ext-ref/worldcat-org/terms.html <sup>74</sup>. WorldCat Search API | OCLC Developer Network, consulté le mai 20, 2026, https://www.oclc.org/developer/api/oclc-apis/worldcat-search-api.en.html <sup>75</sup>. 1.3B Worldcat scrape and data science mini-competition | Hacker News, consulté le mai 20, 2026, https://news.ycombinator.com/item?id=37764088

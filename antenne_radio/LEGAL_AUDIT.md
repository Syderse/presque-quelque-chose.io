# Legal audit - antenne radio

Date: 2026-05-19
Statut: audit minimal avant publication publique

Ce document n'est pas un avis juridique. Il fixe une politique prudente pour
eviter qu'un futur export public expose des donnees privees, des contenus sous
droits ou des donnees dont la reutilisation n'est pas claire.

## Decision courte

Verdict global: publiable partiellement seulement.

Un futur JSON public peut etre envisage uniquement comme index de liens et de
metadonnees minimales, sans `raw`, sans logs, sans notes privees, sans chemins
locaux, sans secrets, sans champs de debug et sans abstracts.

Les exports actuels `data/exports/veille-YYYY-WW.md` et
`data/exports/zotero-veille-YYYY-WW.csl.json` restent des exports prives.
Ils ne doivent pas etre deplaces vers Hugo tels quels.

## Rappel du Prompt 15

Whitelist publique stricte proposee:

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

Champs interdits en public:

- `raw`
- `abstract`
- logs
- notes privees
- chemins locaux
- secrets
- champs de debug
- `status`
- `relevance_score`
- `score_explanation`
- `keywords_matched`
- `negative_keywords_matched`
- `discovered_at`
- `source_feed`
- `source_api` brut
- `title_original`
- `errors`
- `raw_responses`
- tout champ douteux

## Sources officielles consultees

### Radio Survivor

- https://www.radiosurvivor.com/about-2/
- https://www.radiosurvivor.com/contact-us/
- https://www.radiosurvivor.com/feed/

Constats:

- Le site propose explicitement un flux RSS.
- La page About indique que le contenu du site est sous copyright et demande de
  contacter Radio Survivor avant reproduction de leurs histoires ou photos.

Verdict: publiable partiellement.

Autorise pour un futur export public:

- titre;
- URL canonique;
- date de publication si presente dans le flux;
- nom de source `Radio Survivor`;
- attribution avec lien vers l'article original.

Interdit ou a reporter:

- abstract, resume RSS, extrait, contenu HTML, photo, media embarque;
- republication de texte de l'article;
- stockage public de dump RSS brut;
- scraping HTML.

Attribution minimale:

`Source: Radio Survivor - lien vers l'article original.`

Risque:

- fort si le resume RSS est repris publiquement, car il peut etre considere
  comme reproduction d'une partie de l'histoire.

### Journal of Radio & Audio Media / Taylor & Francis Online

- https://www.tandfonline.com/terms-and-conditions
- https://www.tandfonline.com/action/showFeed?type=etoc&feed=rss&jc=hjrs20

Constats:

- Le flux RSS public existe pour la table des matieres.
- Les conditions Taylor & Francis distinguent contenus gratuits, premium et
  open access.
- Les usages de contenus et d'articles dependent de leur licence propre.
- Les conditions consultables indiquent aussi des restrictions sur le
  telechargement et le stockage systematique de contenus complets.

Verdict: publiable partiellement, avec prudence accrue.

Autorise pour un futur export public:

- titre;
- URL vers la page Taylor & Francis;
- date si fournie par le flux;
- nom de source `Journal of Radio & Audio Media`;
- eventuel DOI seulement s'il vient d'une source metadonnees claire comme
  Crossref ou de la page publique sans copier de contenu protege.

Interdit ou a reporter:

- abstract;
- extrait;
- resume RSS;
- contenu d'article;
- image;
- metadonnees enrichies issues d'une page payante;
- stockage public d'un numero ou d'un volume complet;
- scraping HTML.

Attribution minimale:

`Source: Journal of Radio & Audio Media / Taylor & Francis Online - lien vers la
notice originale.`

Risque:

- eleve pour tout champ textuel descriptif au-dela du titre, surtout les
  abstracts. Preferer Crossref pour les metadonnees bibliographiques quand le
  connecteur Crossref sera active et verifie.

### Sounding Out!

- https://soundstudiesblog.com/sound-studies-blog/
- https://soundstudiesblog.com/editorial-statemen/
- https://soundstudiesblog.com/feed/
- https://soundstudiesblog.com/2012/09/17/easy-listening-spreading-and-the-role-of-the-ear-in-debating/

Constats:

- Le site propose un flux WordPress.
- Les pages officielles presentent Sounding Out! comme publication en ligne
  citable et editoriale.
- Aucune licence globale claire de reutilisation des textes n'a ete trouvee
  dans les pages consultees.
- Au moins certains elements ou images portent des mentions de droits reservees
  ou de licences tierces.

Verdict: publiable partiellement.

Autorise pour un futur export public:

- titre;
- URL de l'article;
- date si presente dans le flux;
- nom de source `Sounding Out!`;
- attribution avec lien vers l'article original.

Interdit ou a reporter:

- abstract;
- extrait;
- contenu HTML;
- images;
- biographies d'auteur issues du flux;
- commentaires;
- media;
- stockage public du dump RSS brut;
- scraping HTML.

Attribution minimale:

`Source: Sounding Out! - lien vers l'article original.`

Risque:

- moyen a eleve, car le flux peut contenir des contenus longs ou du HTML riche.
  L'export public doit se limiter a un index de liens.

### HAL

- https://api.archives-ouvertes.fr/
- https://api.hal.science/docs/oai
- https://doc.hal.science/aspects-juridiques/conditions-de-reutilisation/

Constats:

- HAL expose des APIs et un serveur OAI-PMH pour consultation machine.
- Les conditions OAI indiquent que les metadonnees peuvent etre consultees par
  moissonnage, dans le respect du code de la propriete intellectuelle, et sans
  utilisation commerciale des donnees extraites.
- La documentation HAL 2026 indique que la licence CC0 s'applique aux
  metadonnees des depots, mais que les fichiers et documents ont leurs propres
  conditions de reutilisation.

Verdict: publiable avec attribution, mais seulement pour metadonnees strictes
et usage non commercial.

Autorise pour un futur export public:

- titre;
- URL HAL;
- DOI si present;
- date;
- langue;
- type de document;
- nom de source `HAL`;
- eventuels auteurs seulement si le projet decide d'elargir la whitelist apres
  QA et mention de provenance.

Interdit ou a reporter:

- abstract par defaut;
- texte integral;
- fichier depose;
- licence de fichier non verifiee;
- dump API brut;
- usage commercial;
- moissonnage massif non borne;
- scraping HTML.

Attribution minimale:

`Source: HAL open archive - lien vers la notice HAL.`

Risque:

- modere. Les metadonnees sont mieux encadrees que les RSS, mais la tension
  entre CC0 metadonnees et condition "pas d'utilisation commerciale" impose de
  garder l'export public non commercial et clairement attribue.

### Crossref

- https://www.crossref.org/documentation/retrieve-metadata/
- https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication/
- https://api.crossref.org/

Constats:

- Crossref documente une API REST publique sans inscription obligatoire.
- Crossref indique que la majorite des metadonnees bibliographiques sont des
  faits non soumis au copyright et reutilisables, tandis que les abstracts
  restent soumis au copyright des editeurs ou auteurs.
- Crossref recommande l'identification polie avec `mailto` ou un header agent.
- Les limites documentees au 2026-05-19 sont: pool public 5 requetes, 1
  concurrence; pool polite 10 requetes, 3 concurrences; depassement possible en
  429, blocage possible en 403.

Verdict: publiable avec attribution pour les metadonnees bibliographiques,
mais source a reporter tant que `CROSSREF_MAILTO` n'est pas configure et qu'un
run live limite n'a pas ete verifie.

Autorise pour un futur export public, apres activation controlee:

- titre;
- DOI;
- URL;
- date;
- source/journal;
- type bibliographique;
- langue si disponible;
- auteurs si le projet accepte de les mettre dans une whitelist v1.1.

Interdit:

- abstract;
- raw Crossref;
- `raw_responses`;
- erreurs HTTP detaillees;
- mailto personnel ou valeur de `CROSSREF_MAILTO`;
- dumps avec parametres de debug.

Attribution minimale:

`Metadata: Crossref - DOI/lien vers la notice ou l'editeur original.`

Contraintes d'usage:

- garder `rows` bas;
- requetes sequentielles;
- respecter `polite_delay_seconds`;
- utiliser une vraie adresse de contact locale, jamais inscrite dans le depot;
- backoff sur 429 et 403;
- cache local, pas de requetes repetees inutiles.

Risque:

- faible pour metadonnees bibliographiques hors abstracts;
- eleve si abstracts, raw responses ou email de contact fuitent.

## Sources inactives ou reportees

### Transom

Verdict: a reporter.

Raison:

- Source RSS desactivee dans la configuration locale apres erreurs 301 et 0
  entree stable. Aucun export public ne doit contenir de donnees Transom tant
  que le flux n'est pas revalide et audite.

### Sounding Out! podcast

Verdict: a reporter.

Raison:

- Source declaree mais inactive pour eviter doublon thematique. Ne pas publier
  ses metadonnees avant activation, test et audit dedie.

### OpenAlex, CiNii, NDL, J-STAGE, RadioDoc Review

Verdict: a reporter.

Raison:

- Non suivis dans l'etat actuel. Aucune publication publique et aucun contrat
  de reutilisation ne doivent etre supposes.

## Politique d'abstracts

Verdict: prive seulement.

Regle:

- Aucun abstract public par defaut.
- Un abstract ne pourra devenir public que si une decision explicite future
  verifie la source, la licence de l'item et le besoin editorial.
- Cette regle vaut pour RSS, HAL et Crossref.

## Politique de rate limit et collecte

- RSS: pas de scraping HTML, seulement flux declares, cadence manuelle ou basse,
  cache local, pas de moissonnage agressif.
- HAL: requetes bornees (`limit: 20` actuellement), pas d'usage commercial,
  cache local.
- Crossref: source desactivee par defaut, activation seulement avec
  `CROSSREF_MAILTO`, `User-Agent` explicite, delai poli et backoff.
- Aucun cron public, aucun auto-commit, aucune publication automatique tant que
  l'export public n'est pas implemente et teste.

## Contrat public provisoire

Un futur export public doit:

1. etre genere par whitelist stricte;
2. exclure tous les champs interdits du Prompt 15;
3. ne pas inclure les items `ignored`;
4. ne jamais contenir de `raw`;
5. ne jamais contenir de logs;
6. ne jamais contenir d'abstract par defaut;
7. contenir une attribution par item;
8. contenir une section de provenance des sources;
9. etre inspecte par tests anti-fuite avant toute integration Hugo.

## Verdict final du Prompt 16

- RSS Radio Survivor: publiable partiellement.
- RSS Journal of Radio & Audio Media / Taylor & Francis: publiable
  partiellement, prudence accrue.
- RSS Sounding Out!: publiable partiellement.
- HAL: publiable avec attribution pour metadonnees strictes, non commercial,
  sans abstracts.
- Crossref: publiable avec attribution pour metadonnees bibliographiques, mais
  a reporter jusqu'a activation controlee avec `CROSSREF_MAILTO`.
- Sources inactives ou non suivies: a reporter.

Prochain chantier recommande: Prompt 17, QA du contrat public et mise a jour de
la memoire materielle. Ne pas commencer l'export public ni l'integration Hugo
avant cette QA.

# Legal audit — Antenne radio

Dernier audit : 2026-05-20  
Objet : sources RSS faciles pour agrégateur public léger sur le site.

## Règle générale retenue

Pour toutes les sources ci-dessous, l’antenne radio ne stocke et n’affiche que :

- `source_name`
- `title`
- `published_at`
- `original_url`
- `fetched_at`
- `legal_status`
- `audit_date`

Champs à ne pas stocker / republier par défaut :

- `summary`
- `description`
- `abstract`
- `content`
- `content:encoded`
- extraits longs
- images reprises depuis la source
- audio repris depuis la source

Raison : l’objectif est un index de liens, non une republication éditoriale.

## Sources auditées

| Source | Statut | Usage autorisé retenu | Attribution | Résumés / abstracts | URLs consultées | Date |
|---|---|---|---|---|---|---|
| Radiomorphoses | VALIDÉ — métadonnées ; contenu sous conditions CC | Titre, date, URL originale. Contenus potentiellement réutilisables sous CC BY-NC-SA 4.0, mais non repris dans l’antenne. | Mentionner Radiomorphoses, auteur si disponible, OpenEdition, URL/DOI. | Ne pas stocker par homogénéité, sauf traitement CC explicite futur. | https://journals.openedition.org/radiomorphoses/?lang=en&page=informations ; https://www.openedition.org/33667?lang=en | 2026-05-20 |
| Radio Fañch | VALIDÉ PRUDENT — métadonnées uniquement | Titre, date, URL originale. | Mentionner Radio Fañch + lien vers le billet. | Ne pas stocker / republier. Aucune licence ouverte identifiée. | https://radiofanch.blogspot.com/ ; http://radiofanch.blogspot.com/feeds/posts/default?alt=rss ; https://radio5312.rssing.com/chan-34736084/all_p1.html | 2026-05-20 |
| Les Radios Libres | VALIDÉ PRUDENT — métadonnées uniquement | Titre, date, URL originale. | Mentionner Les Radios Libres + lien vers le billet. | Ne pas stocker / republier. Aucune licence ouverte identifiée. | https://lesradioslibres.wordpress.com/ ; https://lesradioslibres.wordpress.com/about/ ; https://lesradioslibres.wordpress.com/contact/ | 2026-05-20 |
| La Radio du Futur | VALIDÉ PRUDENT — métadonnées uniquement | Titre, date, URL originale. | Mentionner La Radio du Futur + lien vers le billet. | Ne pas stocker / republier. Aucune licence ouverte identifiée. | https://radiodufutur.wordpress.com/ ; https://radiodufutur.wordpress.com/about/ ; https://radiodufutur.wordpress.com/author/sebastienpoulain/ | 2026-05-20 |
| La Lettre Pro de la Radio | VALIDÉ STRICT — liens uniquement | Titre, date, URL originale. Le site propose explicitement la syndication sous forme de liste de liens récents. | Mentionner La Lettre Pro de la Radio & du Podcast + lien vers l’article. | Ne pas stocker / republier. Les mentions légales interdisent la reproduction partielle ou totale sur support électronique. | https://www.lalettre.pro/feeds/ ; https://www.lalettre.pro/rgpd/ | 2026-05-20 |
| MeCCSA Radio & Audio Studies | VALIDÉ PRUDENT — métadonnées uniquement | Titre, date, URL originale. | Mentionner MeCCSA Radio and Audio Studies + lien vers le billet. | Ne pas stocker / republier. Aucune licence ouverte identifiée. | https://www.meccsa.org.uk/networks/radio-studies-section/ ; https://radiostudiesnetworkreadinggroup.wordpress.com/ | 2026-05-20 |
| Nieman Storyboard | VALIDÉ PRUDENT — métadonnées uniquement | Titre, date, URL originale. | Mentionner Nieman Storyboard + lien vers l’article. | Ne pas stocker / republier. Pas de licence générale ; certains contenus sont sous droits réservés ou reproduits par permission. | https://niemanstoryboard.org/about/ ; https://niemanstoryboard.org/about/subscribe-to-nieman-storyboard/ ; https://niemanstoryboard.org/2016/05/06/turbulent-times/ | 2026-05-20 |
| Transom | VALIDÉ PRUDENT — métadonnées uniquement | Titre, date, URL originale. Flux retesté : endpoint repéré. | Mentionner Transom + lien vers l’article ; attribution requise en cas de réutilisation. | Ne pas stocker / republier. Les auteurs conservent leurs droits. | https://transom.org/about/about-transom/ ; https://transom.org/about/submit-your-work/ ; https://transom.org/faq/ ; https://transom.org/feed/ | 2026-05-20 |

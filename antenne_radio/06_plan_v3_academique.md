# Antenne Radio v3 - Plan academique sobre et priorise

```text
Note d'execution :
- La V2 est consideree comme stable : pipeline local, exports prives, export public whitelist, section Hugo et filtres UX.
- La V3 ne reconstruit pas l'antenne. Elle etend prudemment la base reelle.
- Le transfert entre conversations repose sur antenne_radio/codex_memoire_materielle.md.
- A la fin de chaque prompt, ajouter un handoff clair dans ce fichier pour qu'une conversation fraiche puisse reprendre sans contexte implicite.
- Tous les chemins de l'antenne sont a resoudre depuis le dossier reel antenne_radio/.
- Ne jamais creer de doublon a la racine si un fichier equivalent existe deja dans antenne_radio/.
```

## Objectif de la V3

La V3 ajoute une couche academique robuste autour de trois gestes, chacun traite comme une conversation autonome :

1. **Activer Crossref proprement** : `mailto` obligatoire, limites basses, dedoublonnage DOI robuste, aucun abstract public.
2. **Ajouter OpenAlex** : requetes ciblees radio/audio/sound studies, score de pertinence explicable, API polie et bornee.
3. **Ajouter les venues et reseaux prioritaires** : Radio Journal, Sound Studies, JSS, Resonance, IAMCR MAR, ECREA Radio & Sound, MeCCSA.

Cette V3 reste une antenne locale de veille, pas une archive exhaustive ni un service automatique.

## Hors perimetre explicite

Sont reportes hors V3 :

- litterature japonaise, CiNii, NDL, J-STAGE : **V4 separee** ;
- moissonnage generaliste DOAJ, Persee, CAIRN, OpenEdition OPML ;
- scraping HTML de pages sans flux stable ou API documentee ;
- cron, auto-commit, publication automatique, resume LLM ;
- ajout de champs publics au JSON Hugo sans audit legal dedie.

Le JSON public conserve strictement le schema `antenne-radio-public-v0` :

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

Tout le reste reste prive : `raw`, `abstract`, auteurs, tags, scores, explications de score, statuts, logs, chemins locaux, secrets.

## Principes directeurs

- **Local d'abord** : tout passe par `make test`, `make run`, `make export-public`, puis build Hugo si l'export public est touche.
- **Politesse API** : Crossref et OpenAlex doivent identifier le projet avec une adresse locale configuree hors Git.
- **Sources bornees** : limites basses, fenetre recente de 18 mois, runs live isoles et inspectes.
- **Dedupe avant volume** : DOI normalise prioritaire, puis URL normalisee, puis titre/date/source.
- **Curation humaine protegee** : ne jamais ecraser silencieusement `to_read`, `ignored`, `exported` ou toute decision humaine.
- **Public deny-by-default** : un champ non explicitement whiteliste est interdit en public.

---

# Conversation 1 - Crossref propre, DOI et anti-fuite

But : passer de "Crossref prepare mais desactive" a une activation controlee, documentee et sure.

## Prompt 1.1 - Audit de l'etat Crossref reel

```text
Objectif : Auditer l'etat actuel de Crossref dans le depot avant toute activation durable.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/README.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repere les chemins reels des fichiers avant d'en creer de nouveaux ;
- ne lance aucune ingestion live non demandee ;
- ne cree aucun cron ;
- ne cree aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores, auteurs, tags ou chemins locaux.

Taches :
1. Inspecter l'existant :
   - antenne_radio/config/sources.yaml ;
   - antenne_radio/scripts/ingest/ingest_crossref.py ;
   - antenne_radio/scripts/core/normalize.py ;
   - antenne_radio/scripts/core/models.py ;
   - antenne_radio/tests/test_ingest_crossref.py ;
   - antenne_radio/tests/test_normalize.py ;
   - antenne_radio/LEGAL_AUDIT.md ;
   - antenne_radio/01_RESSOURCES_SUIVIES.md.
2. Verifier que Crossref :
   - reste desactive par defaut tant que l'activation n'est pas decidee ;
   - exige `CROSSREF_MAILTO` ou une valeur locale equivalente avant tout appel reseau ;
   - n'inscrit aucune adresse personnelle ou secret dans Git ;
   - conserve `rows` bas et `polite_delay_seconds` actif ;
   - ecrit seulement un dump local sous antenne_radio/data/raw/crossref_latest.json.
3. Verifier la doctrine abstract :
   - les abstracts Crossref peuvent exister dans le dump prive ou db.json si le modele les conserve ;
   - aucun abstract ne doit entrer dans static/antenne-radio/index.json ni dans le HTML public.
4. Si la documentation est obsolete, mettre a jour seulement :
   - antenne_radio/README.md ;
   - antenne_radio/LEGAL_AUDIT.md ;
   - antenne_radio/01_RESSOURCES_SUIVIES.md.
5. Lancer make test depuis antenne_radio si des fichiers du module ont ete modifies.

Verification :
- Le depot indique clairement ce qui est deja pret et ce qui bloque encore l'activation.
- Aucun run live Crossref n'a ete lance sans demande explicite.
- Le contrat "mailto obligatoire + pas d'abstract public" est documente.

Ajoute un handoff dans antenne_radio/codex_memoire_materielle.md :
- fichiers lus et modifies ;
- commandes lancees ;
- resultats reels ;
- limites restantes ;
- prochaine etape recommandee pour une conversation fraiche.
```

## Prompt 1.2 - Dedupe DOI inter-sources

```text
Objectif : Rendre le dedoublonnage DOI suffisamment robuste avant d'ajouter du volume Crossref.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/README.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repere les chemins reels des fichiers avant d'en creer de nouveaux ;
- ne lance aucune ingestion live non demandee ;
- ne cree aucun cron ;
- ne cree aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores, auteurs, tags ou chemins locaux.

Taches :
1. Auditer la logique existante de `normalize_doi`, `generate_stable_id` et `merge_items_without_duplicates`.
2. Renforcer le merge si necessaire pour dedoublonner :
   - DOI normalise, avec ou sans prefixe `doi:` ou `https://doi.org/` ;
   - URL normalisee si DOI absent ;
   - titre normalise + date de publication si DOI et URL absents.
3. En cas de doublon, fusionner sans casser la curation :
   - conserver l'ID stable deja present dans db.json ;
   - conserver le statut humain existant ;
   - ne pas ecraser `to_read`, `ignored`, `exported` ;
   - preferer le DOI normalise quand il apparait dans une source plus recente ;
   - conserver les metadonnees utiles en prive seulement.
4. Ajouter des tests unitaires couvrant au minimum :
   - HAL + Crossref avec le meme DOI ;
   - RSS/Taylor & Francis + Crossref avec DOI equivalent ;
   - DOI avec variations de casse et de prefixe ;
   - preservation d'un statut humain existant ;
   - absence de champ nouveau dans l'export public.
5. Lancer make test depuis antenne_radio.

Verification :
- Deux notices portant le meme DOI normalise ne creent pas deux entrees finales.
- Les decisions humaines de curation restent intactes.
- L'export public conserve strictement sa whitelist.

Ajoute un handoff dans antenne_radio/codex_memoire_materielle.md :
- fichiers modifies ;
- commandes lancees ;
- resultats reels ;
- limites restantes ;
- prochaine etape recommandee pour une conversation fraiche.
```

## Prompt 1.3 - Activation Crossref controlee et recette anti-fuite

```text
Objectif : Activer Crossref de maniere controlee, avec un vrai `mailto` local et une recette de validation complete.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/README.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repere les chemins reels des fichiers avant d'en creer de nouveaux ;
- ne lance aucune ingestion live non demandee ;
- ne cree aucun cron ;
- ne cree aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores, auteurs, tags ou chemins locaux.

Taches :
1. Demander ou verifier une variable locale `CROSSREF_MAILTO` sans jamais l'ecrire dans le depot.
2. Decider explicitement le mode d'activation :
   - activation temporaire pour recette live ;
   - ou activation durable si et seulement si le comportement sans `CROSSREF_MAILTO` reste propre et documente.
3. Lancer une ingestion Crossref limitee a une seule famille de revues et a `rows: 20` ou moins.
4. Inspecter :
   - antenne_radio/data/raw/crossref_latest.json ;
   - antenne_radio/data/logs/api.log ;
   - antenne_radio/data/logs/pipeline.log ;
   - antenne_radio/data/normalized/db.json.
5. Lancer :
   - make test ;
   - make run, seulement si l'activation live a ete explicitement retenue ;
   - make export-public ;
   - un build Hugo complet si static/antenne-radio/index.json a change.
6. Scanner le JSON public et le HTML genere pour verifier l'absence de :
   - abstract ;
   - raw ;
   - score ;
   - score_explanation ;
   - keywords_matched ;
   - negative_keywords_matched ;
   - authors ;
   - tags ;
   - chemins locaux ;
   - secrets.
7. Mettre a jour :
   - antenne_radio/README.md ;
   - antenne_radio/01_RESSOURCES_SUIVIES.md ;
   - antenne_radio/LEGAL_AUDIT.md si le verdict Crossref evolue.

Verification :
- Crossref fonctionne avec mailto local, limites basses et logs lisibles.
- Le dedoublonnage DOI evite les doublons academiques.
- Aucun abstract Crossref n'est publie.

Ajoute un handoff dans antenne_radio/codex_memoire_materielle.md :
- mode d'activation retenu ;
- compteurs Crossref reels ;
- compteurs db.json et export public ;
- commandes lancees ;
- resultats de scan anti-fuite ;
- prochaine etape recommandee pour une conversation fraiche.
```

---

# Conversation 2 - OpenAlex cible et score de pertinence

But : ajouter OpenAlex sans ouvrir les vannes du bruit technique.

## Prompt 2.1 - Audit OpenAlex et design des requetes

```text
Objectif : Concevoir l'integration OpenAlex a partir des contraintes reelles du projet avant de coder.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/README.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repere les chemins reels des fichiers avant d'en creer de nouveaux ;
- ne lance aucune ingestion live non demandee ;
- ne cree aucun cron ;
- ne cree aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores, auteurs, tags ou chemins locaux.

Taches :
1. Lire l'etat Crossref issu de la conversation 1 dans antenne_radio/codex_memoire_materielle.md.
2. Auditer les conditions OpenAlex utiles :
   - API Works ;
   - identification polie avec `mailto` ;
   - limites de requetes ;
   - champs disponibles ;
   - prudence autour des abstracts et de `abstract_inverted_index`.
3. Definir 3 a 5 profils de requete stricts, par exemple :
   - radio studies ;
   - radio and audio media ;
   - sound studies ;
   - podcast studies ;
   - community radio / free radio.
4. Definir aussi les exclusions de bruit :
   - radio frequency ;
   - radiotherapy ;
   - radioactive ;
   - radio telescope ;
   - electromagnetic radiation ;
   - cognitive radio ;
   - 5G / 6G / MIMO / beamforming.
5. Proposer la structure de configuration la plus simple :
   - soit une section `openalex` dans antenne_radio/config/sources.yaml ;
   - soit un petit fichier dedie seulement si sources.yaml devient illisible.
6. Documenter la decision dans antenne_radio/LEGAL_AUDIT.md et antenne_radio/01_RESSOURCES_SUIVIES.md.

Contraintes :
- `openalex.enabled` doit rester `false` par defaut jusqu'a recette live.
- `OPENALEX_MAILTO` doit etre local, jamais commite.
- Ne pas reconstruire ni publier les abstracts OpenAlex.
- Le score de pertinence est prive et ne doit jamais entrer dans l'export public.

Verification :
- Le design OpenAlex est documente, borne et compatible avec la doctrine V2.
- Aucun code d'ingestion live n'est necessairement produit dans ce prompt.

Ajoute un handoff dans antenne_radio/codex_memoire_materielle.md :
- decisions de requetes ;
- champs autorises/interdits ;
- fichiers modifies ;
- commandes lancees ;
- prochaine etape recommandee pour une conversation fraiche.
```

## Prompt 2.2 - Ingestor OpenAlex mocke et desactive par defaut

```text
Objectif : Ajouter le connecteur OpenAlex en tests mockes, sans activation live implicite.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/README.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repere les chemins reels des fichiers avant d'en creer de nouveaux ;
- ne lance aucune ingestion live non demandee ;
- ne cree aucun cron ;
- ne cree aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores, auteurs, tags ou chemins locaux.

Taches :
1. Creer antenne_radio/scripts/ingest/ingest_openalex.py sur le modele des ingestors existants.
2. Ajouter une section `openalex` dans antenne_radio/config/sources.yaml :
   - `enabled: false` par defaut ;
   - `mailto_env: OPENALEX_MAILTO` ;
   - limite basse par run ;
   - fenetre de 18 mois ;
   - profils de requete radio/audio/sound studies.
3. Ecrire le dump brut dans antenne_radio/data/raw/openalex_latest.json.
4. Ne pas reconstruire ni stocker d'abstract OpenAlex dans les donnees normalisees, sauf decision ulterieure explicitement auditee.
5. Ajouter antenne_radio/tests/test_ingest_openalex.py avec mocks reseau :
   - source desactivee n'appelle pas le reseau ;
   - mailto obligatoire ;
   - parametres de requete conformes aux profils ;
   - limites de volume respectees ;
   - erreurs HTTP/timeouts loggees proprement.
6. Integrer l'appel OpenAlex dans antenne_radio/scripts/pipeline.py seulement derriere le flag/config `enabled`.
7. Lancer make test depuis antenne_radio.

Verification :
- OpenAlex est present dans le code, mais n'appelle pas le reseau sans activation explicite.
- Les tests valident mailto, limites et requetes ciblees.

Ajoute un handoff dans antenne_radio/codex_memoire_materielle.md :
- fichiers modifies ;
- commandes lancees ;
- resultats de tests ;
- limites restantes ;
- prochaine etape recommandee pour une conversation fraiche.
```

## Prompt 2.3 - Normalisation OpenAlex, score de pertinence et recette

```text
Objectif : Normaliser OpenAlex, attribuer un score de pertinence prive et verifier l'absence de fuite publique.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/README.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repere les chemins reels des fichiers avant d'en creer de nouveaux ;
- ne lance aucune ingestion live non demandee ;
- ne cree aucun cron ;
- ne cree aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores, auteurs, tags ou chemins locaux.

Taches :
1. Ajouter la normalisation OpenAlex dans antenne_radio/scripts/core/normalize.py :
   - DOI normalise si present ;
   - URL canonique ;
   - titre ;
   - date de publication ;
   - langue si disponible ;
   - source `OpenAlex` ;
   - `source_api: openalex`.
2. Integrer les items OpenAlex au dedoublonnage DOI existant.
3. Ajuster antenne_radio/config/keywords.yaml et antenne_radio/config/scoring.yaml si necessaire :
   - renforcer les signaux radio/audio/sound studies ;
   - penaliser le bruit technique ;
   - garder le score explicable.
4. Ajouter des tests :
   - normalisation d'un item OpenAlex ;
   - dedupe OpenAlex + Crossref avec meme DOI ;
   - score pertinent pour radio/audio/sound studies ;
   - rejet ou forte penalisation du bruit technique ;
   - export public sans score ni abstract.
5. Option live, seulement si `OPENALEX_MAILTO` est disponible et si le prompt le decide explicitement :
   - activer OpenAlex temporairement ;
   - lancer un run ultra-limite ;
   - inspecter openalex_latest.json, db.json et les logs ;
   - remettre `enabled: false` sauf decision contraire documentee.
6. Lancer :
   - make test ;
   - make export-public si db.json ou le pipeline public sont touches ;
   - build Hugo si static/antenne-radio/index.json change.

Verification :
- Les items OpenAlex pertinents peuvent entrer en base privee.
- Les faux positifs techniques ne polluent pas la veille.
- Le score reste strictement prive.
- Le public ne montre ni abstract, ni score, ni explication de score.

Ajoute un handoff dans antenne_radio/codex_memoire_materielle.md :
- compteurs OpenAlex si run live ;
- decisions de scoring ;
- fichiers modifies ;
- commandes lancees ;
- resultats anti-fuite ;
- prochaine etape recommandee pour une conversation fraiche.
```

---

# Conversation 3 - Venues et reseaux prioritaires

But : rendre la veille academique plus proche des lieux reels de publication et de sociabilite scientifique.

Sources visees :

- Radio Journal ;
- Sound Studies ;
- JSS / Journal of Sonic Studies ;
- Resonance ;
- IAMCR MAR ;
- ECREA Radio & Sound ;
- MeCCSA Radio & Audio Studies.

Certaines sources existent deja partiellement dans la V2, notamment Journal of Radio & Audio Media, Sounding Out! et MeCCSA Radio & Audio Studies. Cette conversation doit donc completer et qualifier, pas dupliquer.

## Prompt 3.1 - Audit des venues et reseaux

```text
Objectif : Identifier les points d'acces stables et legaux pour chaque venue ou reseau prioritaire.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/README.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repere les chemins reels des fichiers avant d'en creer de nouveaux ;
- ne lance aucune ingestion live non demandee ;
- ne cree aucun cron ;
- ne cree aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores, auteurs, tags ou chemins locaux.

Taches :
1. Pour chaque cible, verifier les points d'acces officiels actuels :
   - flux RSS/Atom ;
   - Crossref par ISSN ou DOI ;
   - OpenAlex par source/venue ou requete profilee ;
   - page d'annonces uniquement si elle expose un flux stable.
2. Cibles a traiter :
   - Radio Journal ;
   - Sound Studies ;
   - JSS / Journal of Sonic Studies ;
   - Resonance ;
   - IAMCR MAR ;
   - ECREA Radio & Sound ;
   - MeCCSA Radio & Audio Studies.
3. Classer chaque cible :
   - activable maintenant ;
   - activable via Crossref ;
   - activable via OpenAlex ;
   - reseau a suivre par RSS/annonces ;
   - a reporter faute de flux stable.
4. Consulter la manière de faire antenne_radio/LEGAL_AUDIT.md.
5. Mettre a jour antenne_radio/01_RESSOURCES_SUIVIES.md avec le statut humain :
   - actif ;
   - inactif configure ;
   - candidat ;
   - reporte.

Contraintes :
- Ne pas scraper HTML a la main si aucun flux/API stable n'existe.
- Ne pas ajouter de source live non auditee.
- Si une source est deja couverte par RSS, Crossref ou OpenAlex, preferer enrichir sa fiche plutot que creer un doublon.

Verification :
- Chaque venue/reseau a un statut explicite.
- Les sources sans acces stable sont reportees proprement au lieu d'etre forcees.

Ajoute un handoff dans antenne_radio/codex_memoire_materielle.md :
- tableau des venues avec statut ;
- fichiers modifies ;
- commandes lancees ;
- incertitudes restantes ;
- prochaine etape recommandee pour une conversation fraiche.
```

## Prompt 3.2 - Configuration des venues et profils de requete

```text
Objectif : Ajouter les venues et reseaux validés dans la configuration sans creer de doublons ni de bruit massif.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/README.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repere les chemins reels des fichiers avant d'en creer de nouveaux ;
- ne lance aucune ingestion live non demandee ;
- ne cree aucun cron ;
- ne cree aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores, auteurs, tags ou chemins locaux.

Taches :
1. Modifier antenne_radio/config/sources.yaml pour les sources validees :
   - RSS/Atom quand un flux stable existe ;
   - Crossref journal profile quand une revue est mieux suivie par ISSN ;
   - OpenAlex venue/query profile quand l'API donne une meilleure couverture ;
   - `enabled: false` pour toute source nouvelle qui n'a pas encore eu de run inspecte.
2. Eviter les doublons avec les sources V2 :
   - Journal of Radio & Audio Media existe deja ;
   - Sounding Out! existe deja ;
   - MeCCSA Radio & Audio Studies existe deja.
3. Ajouter ou ajuster les attributions publiques dans antenne_radio/scripts/export/export_public.py uniquement si de nouvelles sources peuvent apparaitre dans l'export public.
4. Ajouter les tests de configuration et d'attribution necessaires :
   - antenne_radio/tests/test_config.py ;
   - antenne_radio/tests/test_export_public.py ;
   - tests dedies si une logique de profil est ajoutee.
5. Lancer make test depuis antenne_radio.

Verification :
- La configuration est lisible et maintenable.
- Les nouvelles sources sont documentees, bornees et desactivees tant qu'elles n'ont pas ete validees.
- Les sources deja existantes ne sont pas dupliquees.

Ajoute un handoff dans antenne_radio/codex_memoire_materielle.md :
- sources ajoutees ou modifiees ;
- sources laissees inactives ;
- fichiers modifies ;
- commandes lancees ;
- resultats de tests ;
- prochaine etape recommandee pour une conversation fraiche.
```

## Prompt 3.3 - Recette finale V3 et gel du perimetre V4

```text
Objectif : Valider la V3 academique complete et preparer une reprise propre pour la V4 japonaise plus tard.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/README.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repere les chemins reels des fichiers avant d'en creer de nouveaux ;
- ne lance aucune ingestion live non demandee ;
- ne cree aucun cron ;
- ne cree aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores, auteurs, tags ou chemins locaux.

Taches :
1. Lancer la recette locale :
   - make test ;
   - make run, seulement avec les sources explicitement validees ;
   - make export-public ;
   - build Hugo complet depuis la racine du depot.
2. Inspecter les artefacts :
   - antenne_radio/data/raw/*.json ;
   - antenne_radio/data/normalized/db.json ;
   - antenne_radio/data/exports/* ;
   - antenne_radio/data/logs/api.log ;
   - antenne_radio/data/logs/pipeline.log ;
   - static/antenne-radio/index.json ;
   - public/antenne-radio/index.html si le build a ete lance.
3. Faire un scan anti-fuite du JSON public et du HTML :
   - pas de raw ;
   - pas d'abstract ;
   - pas d'auteurs ;
   - pas de tags ;
   - pas de score ;
   - pas de score_explanation ;
   - pas de keywords internes ;
   - pas de logs ;
   - pas de chemins locaux ;
   - pas de secrets.
4. Mettre a jour les docs de cloture :
   - antenne_radio/README.md ;
   - antenne_radio/01_RESSOURCES_SUIVIES.md ;
   - antenne_radio/LEGAL_AUDIT.md ;
   - antenne_radio/codex_memoire_materielle.md ;
   - docs/CHANTIERS.md si le backlog suit les versions.
5. Ajouter une section explicite "V4 japonaise plus tard" dans la memoire materielle :
   - CiNii ;
   - NDL ;
   - J-STAGE ;
   - litterature japonaise ;
   - conditions d'audit avant implementation.

Verification :
- La V3 est validée localement avec compteurs reels.
- Crossref et OpenAlex sont bornes, documentes et testés.
- Les venues/reseaux prioritaires ont un statut clair.
- La V4 japonaise est separee du bilan V3.

Ajoute un handoff final dans antenne_radio/codex_memoire_materielle.md :
- etat final V3 ;
- sources actives ;
- sources configurees mais inactives ;
- compteurs db.json et export public ;
- commandes et resultats ;
- scans anti-fuite ;
- limites restantes ;
- premiere proposition de Conversation 1 pour la V4 japonaise.
```

---

## Resume par conversation

| Conversation | But | Prompts | Sortie attendue |
|---:|---|---|---|
| 1 | Crossref propre | 1.1 audit, 1.2 dedupe DOI, 1.3 activation controlee | Crossref utilisable avec mailto, DOI dedupe, aucun abstract public |
| 2 | OpenAlex cible | 2.1 design, 2.2 ingestor, 2.3 scoring/QA | OpenAlex configure, teste, score prive, bruit technique controle |
| 3 | Venues/reseaux | 3.1 audit, 3.2 configuration, 3.3 recette finale | Sources prioritaires classees, configurees ou reportees, V3 verifiee |

## Fichiers probablement touches

| Zone | Fichiers |
|---|---|
| Configuration | `antenne_radio/config/sources.yaml`, `antenne_radio/config/keywords.yaml`, `antenne_radio/config/scoring.yaml` |
| Ingestion | `antenne_radio/scripts/ingest/ingest_crossref.py`, `antenne_radio/scripts/ingest/ingest_openalex.py`, `antenne_radio/scripts/pipeline.py` |
| Normalisation | `antenne_radio/scripts/core/models.py`, `antenne_radio/scripts/core/normalize.py`, `antenne_radio/scripts/core/scoring.py` |
| Export public | `antenne_radio/scripts/export/export_public.py`, `static/antenne-radio/index.json` |
| Tests | `antenne_radio/tests/test_ingest_crossref.py`, `antenne_radio/tests/test_ingest_openalex.py`, `antenne_radio/tests/test_normalize.py`, `antenne_radio/tests/test_scoring.py`, `antenne_radio/tests/test_config.py`, `antenne_radio/tests/test_export_public.py`, `antenne_radio/tests/test_pipeline.py` |
| Documentation | `antenne_radio/README.md`, `antenne_radio/LEGAL_AUDIT.md`, `antenne_radio/01_RESSOURCES_SUIVIES.md`, `antenne_radio/codex_memoire_materielle.md`, `docs/CHANTIERS.md` |

## Critere de sortie V3

La V3 est terminee seulement si :

- `make test` passe ;
- les runs live, s'ils ont lieu, sont volontaires et documentes ;
- Crossref utilise `CROSSREF_MAILTO` et reste borne ;
- OpenAlex utilise `OPENALEX_MAILTO`, reste cible et ne reconstruit pas d'abstract public ;
- les venues/reseaux prioritaires ont un statut lisible ;
- le JSON public respecte la whitelist v0 ;
- les scans anti-fuite sont documentes ;
- antenne_radio/codex_memoire_materielle.md permet a une conversation fraiche de reprendre sans ambiguite.

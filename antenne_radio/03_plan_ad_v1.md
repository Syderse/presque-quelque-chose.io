# Plan de finalisation - Antenne de veille radio v1

Ce document prend le relais de `antenne_radio/02_plan_ad_v02.md` pour conduire l'antenne vers une v1 exploitable dans la duree.

La v1 ne signifie pas "tout faire". Elle signifie : une antenne fiable, documentee, juridiquement prudente, publiable si l'audit l'autorise, et suffisamment automatisee pour devenir un outil de recherche ordinaire sans devenir un service fragile.

Le principe reste celui du plan general : capter des signaux heterogenes, les convertir vers un modele pivot, filtrer, puis redistribuer vers des sorties privees et publiques. Mais la finalisation v1 doit garder la discipline acquise en v0.1/v0.2 : petits chantiers, tests, logs lisibles, sources desactivables, pas de publication non auditee.

## 0. Conditions d'entree

Avant de lancer ce plan, verifier l'etat reel. Si certains groupes de `02_plan_ad_v02.md` ne sont pas termines, ne pas les sauter automatiquement : commencer par le groupe 1 ci-dessous pour produire une cartographie des manques.

Lecture obligatoire au debut de chaque prompt :

- `git status --short`
- `docs/AGENTS.md`
- `antenne_radio/codex_memoire_materielle.md`
- `antenne_radio/02_plan_ad_v02.md`
- `antenne_radio/RESSOURCES_SUIVIES.md`
- `antenne_radio/README.md`
- `antenne_radio/LEGAL_AUDIT.md` si le fichier existe

Commandes utiles depuis `antenne_radio/` :

```sh
make test
make run
tail -n 80 data/logs/api.log
tail -n 80 data/logs/pipeline.log
```

Regle d'execution : lancer les prompts un par un. Le troisieme prompt de chaque groupe est un prompt de QA, memoire materielle et handoff. Ne pas ouvrir le groupe suivant tant que le handoff du groupe precedent n'est pas clair.

## 1. Definition de la v1

La v1 vise cet etat :

- pipeline local et CI reproductible ;
- sources actives documentees, desactivables, juridiquement auditees ;
- RSS/Atom, HAL et au moins une API academique occidentale stabilises ;
- sources japonaises traitees par connecteurs officiels ou explicitement reportees avec raison ;
- pas de scraping HTML interne non audite ;
- scoring lexical explicable et calibre sur les faux positifs connus ;
- exports prives Obsidian et Zotero manuels ;
- export public expurge par whitelist stricte ;
- integration Hugo sobre si l'audit legal est favorable ;
- workflow GitHub Actions manuel, puis cron seulement si les garde-fous sont verts ;
- documentation de reprise suffisante pour relancer une conversation Codex sans redecouvrir le projet.

## 2. Hors-perimetre v1 par defaut

- Ecriture automatique dans Zotero.
- Ecriture automatique dans un vrai coffre Obsidian.
- Publication d'abstracts commerciaux.
- Publication de `raw`, logs, notes privees, secrets, `zotero_uri` ou `notes_path`.
- Scraping DOM comme strategie par defaut.
- Service serveur permanent.
- Resume LLM automatique.
- Auto-commit direct sur la branche principale.
- Cron si la GitHub Action manuelle n'a pas deja prouve sa stabilite.

## 3. Serie de prompts Codex groupes 3 par 3

Chaque groupe suit la meme forme : audit/decision, implementation limitee, QA/handoff. Si un audit conclut que le chantier est premature, le prompt d'implementation doit documenter le report plutot que forcer du code.

### Groupe 1 - Audit de reprise v0.2 vers v1

- Objectif : savoir exactement ce qui existe apres la v0.2 et ce qui manque pour v1.
- Niveau : faible.
- Fichiers concernes : documentation, tests, logs, `codex_memoire_materielle.md`.
- Risques : relancer de vieux prompts, confondre plan et etat reel.
- Tests obligatoires : `make test`, verification des compteurs si `db.json` existe.
- Handoff attendu : carte precise des groupes v0.2 termines, incomplets ou a reprendre.

#### Prompt 1 - Audit reel de l'etat v0.2

```text
Objectif : etablir l'etat reel de l'antenne avant d'ouvrir la finalisation v1.

Au debut, lance `git status --short`, lis `docs/AGENTS.md`, `antenne_radio/codex_memoire_materielle.md`, `antenne_radio/02_plan_ad_v02.md`, `antenne_radio/RESSOURCES_SUIVIES.md` et `antenne_radio/README.md`.

Taches :
1. Depuis `antenne_radio/`, lance `make test`.
2. Verifie quels fichiers prevus par la v0.2 existent : export Zotero, export public, workflow GitHub Actions, `LEGAL_AUDIT.md`, integration Hugo eventuelle.
3. Inspecte les logs recents si presents.
4. Verifie les compteurs de `data/normalized/db.json` si le fichier existe.
5. Compare l'etat reel aux groupes 1 a 10 de `02_plan_ad_v02.md`.
6. Classe chaque groupe v0.2 : termine, partiel, absent, bloque, a verifier.

Contraintes :
- Ne modifie aucun fichier.
- Ne lance pas de run reseau sauf si necessaire pour comprendre un blocage.
- Ne suppose pas qu'un fichier planifie existe.

Sortie attendue :
- tests passes/echoues ;
- compteurs observes ;
- groupes v0.2 termines/partiels/absents ;
- risques pour la v1 ;
- prochain prompt recommande.
```

#### Prompt 2 - Matrice des manques v1

```text
Objectif : transformer l'audit du Prompt 1 en matrice de finalisation.

Au debut, lance `git status --short`, relis `docs/AGENTS.md`, `codex_memoire_materielle.md`, puis relis le bilan du Prompt 1.

Taches :
1. Redige ou mets a jour un court fichier `antenne_radio/V1_GAPS.md`.
2. Liste les fonctions manquantes par categorie : sources, modele, scoring, exports, legal, Hugo, CI, documentation.
3. Pour chaque manque, indique : criticite, prerequis, fichiers probables, risque, test attendu.
4. Distingue les manques bloquants pour v1 des ameliorations reportables.
5. Ne cree aucun code fonctionnel.

Contraintes :
- Garder le document court et actionnable.
- Ne pas transformer `V1_GAPS.md` en second plan complet.
- Ne pas modifier les donnees.

Tests :
- Verifie `git diff --check -- antenne_radio/V1_GAPS.md`.
```

#### Prompt 3 - QA reprise + handoff v1

```text
Objectif : cloturer le groupe 1 avec une base de reprise propre.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis les Prompts 1 et 2.

Taches :
1. Lance `make test` depuis `antenne_radio/`.
2. Verifie `git diff --stat` et `git diff -- antenne_radio/V1_GAPS.md`.
3. Mets a jour `antenne_radio/codex_memoire_materielle.md` avec le statut v1 si cela aide la reprise.
4. Liste les fichiers modifies.
5. Liste les tests passes/echoues.
6. Donne la decision : reprendre des groupes v0.2 manquants ou continuer vers le groupe 2 du present plan.

Contraintes :
- Ne commence pas le groupe 2.
- Ne masque aucun test echoue.
```

### Groupe 2 - Contrats de donnees et curation humaine

- Objectif : stabiliser le modele v1 sans perdre la lisibilite du `db.json`.
- Niveau : moyen.
- Fichiers concernes : `models.py`, `normalize.py`, exports, tests, README.
- Risques : migration destructive, champs publics/prives melanges.
- Tests obligatoires : modeles, normalisation, exports, anti-fuite.
- Handoff attendu : contrat de donnees v1.

#### Prompt 4 - Audit des champs et statuts

```text
Objectif : auditer le modele actuel avant d'ajouter des champs v1.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis `scripts/core/models.py`, `scripts/core/normalize.py`, les exports et les tests.

Taches :
1. Liste les champs actuels de `RadioWatchItem`.
2. Repere les champs manquants pour la curation humaine : note publique, statut public, credit source, droits, URL canonique, date de premiere decouverte.
3. Distingue champs prives, champs publics possibles et champs strictement interdits en public.
4. Propose une migration non destructive si de nouveaux champs sont necessaires.
5. Indique quels tests devront changer.

Contraintes :
- Ne modifie rien.
- Ne change aucun statut dans `db.json`.
```

#### Prompt 5 - Modele v1 et migration non destructive

```text
Objectif : ajouter seulement les champs v1 necessaires et les tests associes.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis le bilan du Prompt 4.

Taches :
1. Modifie `models.py` de facon minimale.
2. Ajoute une migration ou normalisation retrocompatible si necessaire.
3. Preserve les items existants et leur `id`.
4. Ne supprime aucun champ `raw`.
5. Mets a jour les exports seulement si un champ nouveau doit etre ignore ou expose explicitement.
6. Ajoute ou ajuste les tests.

Contraintes :
- Pas de changement de source.
- Pas de publication.
- Pas de migration destructive.

Tests :
- Lance `make test`.
```

#### Prompt 6 - QA contrat donnees + handoff

```text
Objectif : verifier que le contrat de donnees v1 est stable.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis les Prompts 4 et 5.

Taches :
1. Lance `make test`.
2. Verifie qu'un ancien item minimal reste valide.
3. Verifie que l'export public n'expose pas de champ prive si cet export existe.
4. Verifie que l'export Obsidian/Zotero reste coherent.
5. Mets a jour `codex_memoire_materielle.md` avec le contrat de donnees v1.
6. Resume fichiers modifies, tests et limites.
7. Donne le contexte pour passer au groupe 3.
```

### Groupe 3 - Couverture academique occidentale finale

- Objectif : stabiliser Crossref/OpenAlex sans ajouter deux complexites d'un coup.
- Niveau : fort.
- Fichiers concernes : `sources.yaml`, connecteurs, normalisation, tests, logs.
- Risques : rate limits, API key, doublons DOI, bruit.
- Tests obligatoires : mocks HTTP, erreurs 403/429/500, idempotence.
- Handoff attendu : strategie occidentale finale.

#### Prompt 7 - Audit Crossref/OpenAlex restant

```text
Objectif : determiner si la v1 a besoin d'un complement Crossref ou OpenAlex.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis les connecteurs existants et `RESSOURCES_SUIVIES.md`.

Taches :
1. Verifie quelle API occidentale existe deja, le cas echeant.
2. Consulte les documentations officielles actuelles de Crossref et OpenAlex.
3. Compare la valeur ajoutee restante : revues par ISSN, DOI, topics, sources, decouverte large.
4. Verifie conditions, identification, rate limits, API key, attribution.
5. Choisis une seule action : durcir l'existant, ajouter l'API absente, ou reporter.

Contraintes :
- Ne code rien.
- Cite les URLs officielles consultees.
- Si l'information officielle est ambigue, recommander le report.
```

#### Prompt 8 - Connecteur occidental final ou durcissement

```text
Objectif : appliquer la decision du Prompt 7 sans elargir le chantier.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis le bilan du Prompt 7.

Taches selon decision :
1. Si un connecteur existe mais est fragile, durcis logs, backoff, config et tests.
2. Si une seule API doit etre ajoutee, cree le connecteur brut, desactivable, avec dump dans `data/raw/`.
3. Ajoute la normalisation seulement si les champs sont clairs et testes.
4. Preserve idempotence et dedoublonnage DOI/URL.
5. Mets a jour `RESSOURCES_SUIVIES.md`.

Contraintes :
- Pas de deuxieme API dans ce prompt.
- Pas de secret dans le depot.
- Pas de publication.

Tests :
- Lance `make test`.
```

#### Prompt 9 - QA API occidentale + handoff

```text
Objectif : verrouiller la couverture academique occidentale.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis les Prompts 7 et 8.

Taches :
1. Lance `make test`.
2. Verifie les tests de succes, timeout, 403, 429, 500 et reponse inattendue.
3. Verifie que le connecteur est desactivable.
4. Verifie les logs sans secret.
5. Si un run reel est lance, documente les compteurs et limites.
6. Mets a jour `codex_memoire_materielle.md`.
7. Donne le contexte pour passer au groupe 4.
```

### Groupe 4 - Source japonaise officielle : CiNii

- Objectif : integrer ou preparer CiNii sans forcer l'absence d'identifiant.
- Niveau : fort.
- Fichiers concernes : `sources.yaml`, `ingest_cinii.py`, tests, logs, ressources.
- Risques : appid absent, encodage japonais, conditions d'usage.
- Tests obligatoires : mocks, encodage UTF-8, erreur sans appid.
- Handoff attendu : CiNii actif, desactive proprement, ou reporte avec raison.

#### Prompt 10 - Audit CiNii officiel

```text
Objectif : verifier les conditions actuelles de CiNii avant toute implementation.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis le plan general et `02_plan_ad_v02.md`.

Taches :
1. Consulte les pages officielles CiNii/NII utiles.
2. Verifie endpoint, formats, appid, limites, attribution, stockage et publication.
3. Verifie les termes japonais cibles et les contraintes d'encodage.
4. Decide : implementation active, implementation desactivee faute d'appid, ou report.

Contraintes :
- Ne code rien.
- Cite les URLs officielles.
- Si un `appid` est requis et absent, ne pas inventer de contournement.
```

#### Prompt 11 - Connecteur CiNii desactivable

```text
Objectif : implementer CiNii seulement dans le cadre decide au Prompt 10.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis le bilan du Prompt 10.

Taches :
1. Ajoute `scripts/ingest/ingest_cinii.py` si l'audit l'autorise.
2. Lis l'identifiant depuis variable d'environnement si requis.
3. Ajoute une configuration desactivable dans `sources.yaml`.
4. Ecris uniquement un dump brut dans `data/raw/`.
5. Logue proprement appid absent, 403, 429, timeout, XML/JSON invalide.
6. Preserve les caracteres japonais en UTF-8.
7. Ajoute des tests sans reseau.

Contraintes :
- Pas de scraping.
- Pas de secret dans le depot.
- Pas de publication publique.

Tests :
- Lance `make test`.
```

#### Prompt 12 - QA CiNii + handoff

```text
Objectif : verifier CiNii et transmettre un etat clair.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis les Prompts 10 et 11.

Taches :
1. Lance `make test`.
2. Verifie les tests d'encodage japonais.
3. Verifie le comportement sans appid.
4. Verifie que la source est desactivable.
5. Mets a jour `RESSOURCES_SUIVIES.md` et `codex_memoire_materielle.md`.
6. Si CiNii est reporte, documente exactement pourquoi.
7. Donne le contexte pour passer au groupe 5.
```

### Groupe 5 - Source japonaise officielle : NDL Search

- Objectif : ajouter NDL Search avec attribution explicite.
- Niveau : fort.
- Fichiers concernes : `ingest_ndl.py`, config, tests, legal, ressources.
- Risques : XML/SRU, attribution, publication publique.
- Tests obligatoires : fixtures XML, droits/credit, erreurs HTTP.
- Handoff attendu : NDL active/desactivee et attribution verrouillee.

#### Prompt 13 - Audit NDL officiel

```text
Objectif : verifier NDL Search avant integration.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis `LEGAL_AUDIT.md` si present.

Taches :
1. Consulte les docs officielles NDL Search, SRU/OpenSearch et conditions d'utilisation.
2. Verifie attribution obligatoire, formats, limites et publication des metadonnees.
3. Determine les champs a stocker dans `rights` ou `source_credit`.
4. Decide le perimetre v1 : connecteur actif, desactive par defaut, ou report.

Contraintes :
- Ne code rien.
- Cite les URLs officielles.
```

#### Prompt 14 - Connecteur NDL avec attribution

```text
Objectif : implementer NDL Search de facon officielle et auditable.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis le bilan du Prompt 13.

Taches :
1. Cree `scripts/ingest/ingest_ndl.py` si le Prompt 13 l'autorise.
2. Utilise l'endpoint officiel choisi.
3. Parse une fixture XML ou JSON selon le format retenu.
4. Ajoute systematiquement `rights` ou `source_credit` selon l'audit.
5. Ecris un dump brut separe dans `data/raw/`.
6. Ajoute la configuration desactivable.
7. Ajoute des tests sans reseau.

Contraintes :
- Pas de scraping.
- Pas de publication d'abstract ou texte long.

Tests :
- Lance `make test`.
```

#### Prompt 15 - QA NDL + handoff

```text
Objectif : verifier NDL et son attribution.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis les Prompts 13 et 14.

Taches :
1. Lance `make test`.
2. Verifie que chaque item NDL normalise ou brut porte une attribution exploitable.
3. Verifie que l'export public n'expose rien de non autorise.
4. Mets a jour `RESSOURCES_SUIVIES.md`, `LEGAL_AUDIT.md` si present, et `codex_memoire_materielle.md`.
5. Donne le contexte pour passer au groupe 6.
```

### Groupe 6 - Source japonaise officielle : J-STAGE

- Objectif : integrer J-STAGE WebAPI sans scraping.
- Niveau : fort.
- Fichiers concernes : `ingest_jstage.py`, config, tests, legal, ressources.
- Risques : XML, conditions, abstracts, quotas.
- Tests obligatoires : fixtures, interdiction scraping, erreurs HTTP.
- Handoff attendu : J-STAGE actif/desactive ou reporte.

#### Prompt 16 - Audit J-STAGE WebAPI

```text
Objectif : verifier officiellement J-STAGE avant implementation.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis les notes legales existantes.

Taches :
1. Consulte les docs officielles J-STAGE et J-STAGE WebAPI.
2. Verifie les conditions interdisant ou encadrant le scraping.
3. Verifie les formats, limites, attribution et possibilite de stockage/publication.
4. Decide le perimetre v1 : connecteur, source desactivee documentee, ou report.

Contraintes :
- Ne code rien.
- Cite les URLs officielles.
- Ne considere jamais le scraping DOM comme fallback implicite.
```

#### Prompt 17 - Connecteur J-STAGE WebAPI

```text
Objectif : implementer J-STAGE uniquement via WebAPI officielle.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis le bilan du Prompt 16.

Taches :
1. Cree `scripts/ingest/ingest_jstage.py` si autorise.
2. Ajoute une configuration desactivable.
3. Parse le format officiel choisi via fixtures.
4. Ecris un dump brut separe dans `data/raw/`.
5. Logue timeouts, 403, 429, XML invalide et resultats vides.
6. Ajoute tests sans reseau.

Contraintes :
- Pas de scraping HTML.
- Pas de publication d'abstract sauf verdict legal explicite.

Tests :
- Lance `make test`.
```

#### Prompt 18 - QA J-STAGE + handoff

```text
Objectif : verifier J-STAGE et transmettre les limites.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis les Prompts 16 et 17.

Taches :
1. Lance `make test`.
2. Verifie que le code n'utilise pas de scraping DOM.
3. Verifie source desactivable et logs propres.
4. Mets a jour `RESSOURCES_SUIVIES.md`, `LEGAL_AUDIT.md` si present, et `codex_memoire_materielle.md`.
5. Donne le contexte pour passer au groupe 7.
```

### Groupe 7 - Sources sans API via flux externes controles

- Objectif : traiter les pages sans API sans introduire de scraping interne.
- Niveau : moyen.
- Fichiers concernes : config sources, RSS ingest, ressources, legal.
- Risques : ToS, robots.txt, bruit, dependance changedetection.
- Tests obligatoires : source desactivee, feed Atom externe, logs.
- Handoff attendu : decision claire sur changedetection ou report.

#### Prompt 19 - Audit pages sans API

```text
Objectif : determiner si certaines pages sans API doivent entrer en v1.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis `RESSOURCES_SUIVIES.md`.

Taches :
1. Liste les pages candidates sans RSS/API.
2. Verifie ToS, robots.txt et alternatives officielles.
3. Decide si changedetection.io peut servir de producteur externe de flux Atom/RSS.
4. Refuse toute integration qui demanderait du scraping interne non audite.
5. Limite la liste a quelques sources vraiment utiles.

Contraintes :
- Ne code rien.
- Cite les pages officielles ou conditions consultees si verification web faite.
```

#### Prompt 20 - Support source changedetection Atom/RSS

```text
Objectif : ajouter un support minimal pour des flux externes deja produits par changedetection, si l'audit l'autorise.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis le bilan du Prompt 19.

Taches :
1. Si le parseur RSS actuel suffit, ne cree pas de nouveau connecteur.
2. Ajoute seulement une convention de configuration pour les flux changedetection desactives par defaut.
3. Documente que le scraping n'est pas fait par ce depot.
4. Ajoute des tests si une structure de config change.
5. Mets a jour `RESSOURCES_SUIVIES.md`.

Contraintes :
- Pas de navigateur headless.
- Pas de scraping HTML dans le depot.
- Pas de publication automatique.

Tests :
- Lance `make test`.
```

#### Prompt 21 - QA sources sans API + handoff

```text
Objectif : verifier que le groupe n'a pas introduit de scraping fragile.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis les Prompts 19 et 20.

Taches :
1. Lance `make test`.
2. Verifie que les sources sans API sont desactivees si non configurees.
3. Verifie que `RESSOURCES_SUIVIES.md` explique les limites.
4. Mets a jour `codex_memoire_materielle.md`.
5. Donne le contexte pour passer au groupe 8.
```

### Groupe 8 - Qualite du signal et dedoublonnage non destructeur

- Objectif : reduire le bruit de v1 sans perdre les signaux rares.
- Niveau : moyen.
- Fichiers concernes : scoring, normalisation, tests, exports.
- Risques : faux negatifs, fuzzy matching destructeur.
- Tests obligatoires : distribution avant/apres, fixtures positives/negatives, doublons possibles.
- Handoff attendu : politique de signal v1.

#### Prompt 22 - Audit bruit, doublons et faux negatifs

```text
Objectif : mesurer la qualite du signal avant modification.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis inspecte `db.json`, scoring et exports.

Taches :
1. Mesure la distribution des statuts et sources.
2. Echantillonne les `to_read`, `candidate`, `ignored`.
3. Repere doublons probables entre RSS/HAL/API.
4. Repere faux positifs techniques.
5. Repere faux negatifs probables.
6. Propose une politique non destructive : `possible_duplicate`, score ajuste, note de source, ou report.

Contraintes :
- Ne modifie rien.
- Ne supprime aucun item.
```

#### Prompt 23 - Ajustements signal v1

```text
Objectif : ameliorer la qualite du signal sans suppression automatique.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis le bilan du Prompt 22.

Taches :
1. Ajuste mots-cles et ponderations si suffisant.
2. Ajoute un marquage `possible_duplicate` ou equivalent seulement s'il est non destructeur et teste.
3. Ne fusionne pas automatiquement deux items ambigus.
4. Preserve `score_explanation`.
5. Ajoute tests pour doublons DOI/URL, bruit technique et signal rare.

Tests :
- Lance `make test`.
- Si tu rescoring les donnees reelles, documente la distribution avant/apres.
```

#### Prompt 24 - QA signal + handoff

```text
Objectif : verrouiller la politique de signal v1.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis les Prompts 22 et 23.

Taches :
1. Lance `make test`.
2. Verifie que les bons items connus ne passent pas en `ignored`.
3. Verifie que les doublons probables ne sont pas supprimes automatiquement.
4. Mets a jour `codex_memoire_materielle.md` avec distribution, regles et limites.
5. Donne le contexte pour passer au groupe 9.
```

### Groupe 9 - Exports finaux prives et publics

- Objectif : aligner Obsidian, Zotero manuel et public JSON sur le contrat v1.
- Niveau : moyen.
- Fichiers concernes : exports, tests, README, legal.
- Risques : fuite de champs prives, mapping bibliographique pauvre.
- Tests obligatoires : anti-fuite, UTF-8, non-modification par defaut.
- Handoff attendu : formats finaux v1.

#### Prompt 25 - Audit des exports v1

```text
Objectif : verifier les exports avant gel v1.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis tous les scripts sous `scripts/export/`.

Taches :
1. Liste les exports existants et leurs chemins.
2. Verifie quels champs chaque export expose.
3. Compare avec le contrat de donnees v1 et `LEGAL_AUDIT.md`.
4. Repere les fuites possibles : abstract, raw, logs, notes privees, zotero_uri, notes_path.
5. Propose les corrections minimales.

Contraintes :
- Ne modifie rien.
```

#### Prompt 26 - Corrections exports v1

```text
Objectif : corriger les exports pour respecter le contrat v1.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis le bilan du Prompt 25.

Taches :
1. Corrige l'export Obsidian si necessaire.
2. Corrige l'export Zotero manuel si necessaire.
3. Corrige l'export public par whitelist stricte.
4. Ajoute ou renforce les tests anti-fuite.
5. Verifie que les exports ne modifient pas `db.json` par defaut.
6. Mets a jour README si les commandes changent.

Tests :
- Lance `make test`.
```

#### Prompt 27 - QA exports + handoff

```text
Objectif : cloturer les formats de sortie v1.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis les Prompts 25 et 26.

Taches :
1. Lance `make test`.
2. Genere les exports si les donnees locales le permettent.
3. Verifie explicitement l'absence de champs interdits dans l'export public.
4. Verifie UTF-8 japonais.
5. Mets a jour `codex_memoire_materielle.md` avec chemins, commandes et limites.
6. Donne le contexte pour passer au groupe 10.
```

### Groupe 10 - Hugo public et flux sortant

- Objectif : finaliser l'exposition publique seulement si le legal l'autorise.
- Niveau : fort.
- Fichiers concernes : Hugo content/layouts/data, export public, CSS si necessaire.
- Risques : fuite, page trompeuse, refonte inutile, RSS public premature.
- Tests obligatoires : anti-fuite, build Hugo, verification mobile simple.
- Handoff attendu : go/no-go publication publique.

#### Prompt 28 - Audit page publique v1

```text
Objectif : verifier l'integration Hugo existante ou concevoir la finalisation publique.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis `LEGAL_AUDIT.md` et l'export public.

Taches :
1. Verifie si une page Hugo antenne existe deja.
2. Verifie ce qu'elle affiche exactement.
3. Confirme que l'audit legal autorise l'affichage.
4. Decide si un flux RSS sortant public est autorise ou reporte.
5. Propose les corrections sobres : titres, filtres, methode, sources, limites, attribution.

Contraintes :
- Ne code rien.
- Si le verdict legal n'est pas favorable, recommander l'arret du groupe.
```

#### Prompt 29 - Finalisation Hugo sobre

```text
Objectif : finaliser la page publique avec l'export expurge.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis le bilan du Prompt 28.

Taches :
1. Utilise uniquement le JSON public expurge.
2. Affiche les champs autorises : titre, auteurs, source, date, lien DOI/URL, type, tags publics, attribution.
3. Ajoute ou ajuste la section "Methode / sources / limites".
4. Ajoute un flux RSS public seulement si le Prompt 28 l'autorise explicitement.
5. Respecte le style lightweight du site.
6. Ne fais pas de refonte esthetique radicale.

Contraintes :
- Aucun `raw`, abstract interdit, log, secret ou note privee.

Tests :
- Lance les tests antenne pertinents.
- Lance le build Hugo recommande par `docs/AGENTS.md`.
```

#### Prompt 30 - QA Hugo + handoff publication

```text
Objectif : donner un go/no-go publication publique.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis les Prompts 28 et 29.

Taches :
1. Lance `make test` dans `antenne_radio/`.
2. Lance le build Hugo recommande.
3. Verifie explicitement que la page n'affiche aucun champ interdit.
4. Verifie les liens sources/DOI et les attributions.
5. Verifie la lisibilite mobile de base si la page existe.
6. Verifie `git status --short`.
7. Mets a jour `codex_memoire_materielle.md`.
8. Donne un verdict : pret publication, pret apres corrections listees, ou non pret.
9. Donne le contexte pour passer au groupe 11.
```

### Groupe 11 - Automatisation v1 controlee

- Objectif : passer de manuel a semi-automatique sans perdre controle.
- Niveau : fort.
- Fichiers concernes : `.github/workflows/`, README, logs, data policy.
- Risques : secrets, bruit versionne, donnees privees, auto-commit dangereux.
- Tests obligatoires : YAML, tests CI locaux, verification permissions.
- Handoff attendu : workflow v1 et limites d'automatisation.

#### Prompt 31 - Audit cron et politique d'artefacts

```text
Objectif : decider si un cron v1 est acceptable.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis le workflow GitHub Actions existant.

Taches :
1. Verifie que le workflow manuel fonctionne conceptuellement.
2. Identifie les secrets necessaires et absents.
3. Decide quels fichiers peuvent etre produits en CI sans fuite.
4. Decide si un cron hebdomadaire est acceptable.
5. Decide si l'auto-commit est interdit, reporte, ou remplace par une PR manuelle.

Contraintes :
- Ne code rien.
- Par defaut, preferer cron sans auto-commit direct.
```

#### Prompt 32 - Workflow v1 programme prudemment

```text
Objectif : implementer seulement l'automatisation acceptee au Prompt 31.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis le bilan du Prompt 31.

Taches :
1. Ajuste le workflow existant ou cree le workflow v1.
2. Garde `workflow_dispatch`.
3. Ajoute `schedule` seulement si le Prompt 31 l'autorise.
4. Configure permissions minimales.
5. N'ajoute pas d'auto-commit direct sauf decision explicite.
6. Evite l'upload d'artefacts prives.
7. Documente les limites dans README ou memoire.

Tests :
- Verifie syntaxe YAML.
- Lance `make test` localement.
```

#### Prompt 33 - QA automation + handoff

```text
Objectif : verifier l'automatisation v1.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis les Prompts 31 et 32.

Taches :
1. Lance `make test`.
2. Verifie que le workflow contient encore `workflow_dispatch`.
3. Verifie que les permissions sont minimales.
4. Verifie absence de secret en clair.
5. Verifie absence d'auto-commit direct si non autorise.
6. Mets a jour `codex_memoire_materielle.md`.
7. Donne le contexte pour passer au groupe 12.
```

### Groupe 12 - Release candidate v1

- Objectif : produire le go/no-go final de l'antenne.
- Niveau : moyen.
- Fichiers concernes : tous les fichiers antenne et eventuellement Hugo.
- Risques : croire final un systeme non verifie.
- Tests obligatoires : tests antenne, build Hugo si publication, anti-fuite, logs.
- Handoff attendu : verdict v1.

#### Prompt 34 - Audit release candidate

```text
Objectif : auditer toute l'antenne comme candidate v1.

Au debut, lance `git status --short`, lis tous les fichiers de contexte, puis relis les handoffs des groupes precedents.

Taches :
1. Lance `make test` depuis `antenne_radio/`.
2. Lance `make run` seulement si le reseau est disponible et que les sources sont configurees prudemment.
3. Verifie logs, compteurs, exports, legal, Hugo et workflow.
4. Liste les anomalies bloquantes et non bloquantes.
5. Ne corrige rien dans ce prompt.

Sortie attendue :
- go potentiel ;
- no-go ;
- corrections strictement necessaires.
```

#### Prompt 35 - Corrections release candidate

```text
Objectif : corriger uniquement les blocages v1 identifies au Prompt 34.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis le bilan du Prompt 34.

Taches :
1. Corrige les blocages v1 un par un.
2. Ne fais pas de refonte.
3. Ne change pas les choix structurants sans les documenter.
4. Ajoute ou ajuste les tests correspondant aux corrections.
5. Mets a jour documentation ou memoire si necessaire.

Tests :
- Lance `make test`.
- Lance build Hugo si l'integration publique est touchee.
```

#### Prompt 36 - Verdict v1 final

```text
Objectif : donner le verdict final de l'antenne v1.

Au debut, lance `git status --short`, lis les fichiers de contexte, puis relis les Prompts 34 et 35.

Taches :
1. Lance `make test`.
2. Lance le build Hugo si la publication publique fait partie de v1.
3. Verifie anti-fuite public.
4. Verifie logs recents.
5. Verifie `git status --short`.
6. Mets a jour `antenne_radio/codex_memoire_materielle.md` avec un bilan v1 concis.
7. Redige un handoff final : fichiers modifies, commandes, tests, compteurs, sources, exports, legal, Hugo, CI, limites.
8. Donne un verdict unique :
   - v1 prete ;
   - v1 prete apres corrections listees ;
   - v1 non prete.

Contraintes :
- Ne pas donner de feu vert si un test echoue sans explication.
- Ne pas donner de feu vert si une fuite publique est detectee.
```

## 4. Handoff obligatoire en fin de groupe

Chaque prompt 3/6/9/12/15/18/21/24/27/30/33/36 doit produire un handoff avec :

- groupe termine ;
- date et heure locale si utile ;
- branche ou etat git ;
- fichiers modifies ;
- commandes lancees ;
- tests passes ;
- tests echoues ;
- compteurs observes ;
- sources ajoutees, desactivees ou reportees ;
- decisions legales ou editoriales ;
- limites restantes ;
- prochain groupe recommande ;
- raison de ne pas passer au groupe suivant si blocage.

`antenne_radio/codex_memoire_materielle.md` doit etre mis a jour quand une decision change la maniere de reprendre le projet.

## 5. Checklist v1 finale

- [ ] `make test` passe.
- [ ] Les connecteurs actifs sont documentes dans `RESSOURCES_SUIVIES.md`.
- [ ] Chaque source a un etat : active, desactivee, reportee ou bloquee.
- [ ] Les logs recents sont lisibles.
- [ ] Les erreurs reseau ne detruisent pas les donnees existantes.
- [ ] `db.json` reste lisible, UTF-8 et non destructif.
- [ ] Les exports prives ne modifient pas `db.json` par defaut.
- [ ] L'export public est strictement whitelist.
- [ ] Les tests anti-fuite passent.
- [ ] `LEGAL_AUDIT.md` existe si une publication publique existe.
- [ ] Les attributions obligatoires sont visibles dans les sorties publiques.
- [ ] Le site Hugo build si la page publique est incluse.
- [ ] Le workflow GitHub Actions conserve un declenchement manuel.
- [ ] Aucun secret n'est versionne.
- [ ] Aucun auto-commit direct n'existe sans decision explicite.
- [ ] `codex_memoire_materielle.md` contient le bilan v1.

## 6. Message minimal pour reprendre ce plan

```text
Lis `docs/AGENTS.md`, `antenne_radio/codex_memoire_materielle.md`, `antenne_radio/02_plan_ad_v02.md`, `antenne_radio/03_plan_ad_v1.md` et `antenne_radio/RESSOURCES_SUIVIES.md`.

Nous reprenons la finalisation v1 de l'antenne de veille radio.
Commence par `git status --short`.
Ne relance pas les anciens prompts v0.1.
Je veux lancer le groupe X, prompt Y du plan `03_plan_ad_v1.md`.
Respecte les criteres d'arret, les tests et le handoff.
```

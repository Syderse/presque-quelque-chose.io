# Plan de développement — Antenne de veille radio v0.2

Ce document transforme le plan général initial en trajectoire v0.2 réaliste, incrémentale et testable. Le plan général reste l'horizon architectural : une antenne superhétérodyne qui capte des signaux documentaires hétérogènes, les convertit vers un modèle pivot, les filtre, puis les redistribue vers Obsidian, Zotero et éventuellement le site Hugo.

La v0.2 ne doit pas appliquer tout cet horizon d'un coup. Elle doit prolonger la v0.1 stable sans casser sa qualité principale : une base locale, lisible, testée, réversible.

## 0. État réel de départ

### Ce que la v0.1 sait faire

- Ingérer des flux RSS/Atom activés dans `config/sources.yaml`.
- Interroger HAL via `scripts/ingest/ingest_hal.py`.
- Ecrire des dumps bruts dans `data/raw/rss_latest.json` et `data/raw/hal_latest.json`.
- Normaliser les dumps vers `data/normalized/db.json` avec `RadioWatchItem`.
- Dédupliquer strictement par `id`, sans fuzzy matching destructeur.
- Conserver les champs `raw` pour audit.
- Scorer lexicalement les items `new` avec `config/keywords.yaml` et `config/scoring.yaml`.
- Expliquer les scores avec `score_explanation`.
- Exporter un rapport Markdown hebdomadaire vers `data/exports/veille-YYYY-WW.md`.
- Orchestrer le flux avec `scripts/pipeline.py`.
- Continuer après certaines erreurs de source si les données suivantes existent.

### Ce qui est stable

- `make test` passe avec 41 tests dans l'état connu de départ.
- Le pipeline v0.1 a déjà été lancé réellement avec réseau.
- Les tests existants évitent le réseau avec fixtures et `httpx.MockTransport`.
- `db.json` est un tableau JSON lisible, pas un objet enveloppé.
- Les statuts actuels sont `new`, `candidate`, `to_read`, `ignored`, `exported`.
- L'export Obsidian ne marque pas les items comme `exported` par défaut.
- Les sources peuvent être activées ou désactivées sans suppression.

### Limites connues

- Le flux Transom actif a renvoyé 0 entrée au dernier run réel, avec statut 301 et warning de parsing.
- La requête HAL actuelle est volontairement large et remonte du bruit technique.
- Plusieurs items HAL techniques restent `candidate` parce que le terme `radio` est ambigu.
- Les abstracts RSS peuvent contenir du HTML brut.
- L'export Obsidian est utile mais encore peu éditorialisé.
- Le dédoublonnage fuzzy n'existe pas encore.
- Aucune intégration Crossref, OpenAlex, CiNii, NDL, J-STAGE, Zotero ou Hugo public n'existe.
- Aucune GitHub Action n'existe pour l'antenne.
- Aucune publication publique ne doit être faite avant audit légal.

### Données de départ connues

- Dernier run réel connu : 52 entrées RSS, 20 documents HAL, 72 items normalisés.
- Distribution connue : `to_read=56`, `candidate=11`, `ignored=5`, `exported=0`.
- `raw` est présent sur tous les items connus.
- `data/exports/veille-2026-21.md` existe comme export réel.

Ces chiffres doivent être revérifiés au début de chaque chantier. Ils sont un point de départ, pas une vérité permanente.

### Fichiers centraux

- `docs/AGENTS.md`
- `antenne_radio/codex_memoire_materielle.md`
- `antenne_radio/README.md`
- `antenne_radio/RESSOURCES_SUIVIES.md`
- `antenne_radio/01_plan.md`
- `antenne_radio/config/sources.yaml`
- `antenne_radio/config/keywords.yaml`
- `antenne_radio/config/scoring.yaml`
- `antenne_radio/scripts/core/models.py`
- `antenne_radio/scripts/core/normalize.py`
- `antenne_radio/scripts/core/scoring.py`
- `antenne_radio/scripts/ingest/ingest_rss.py`
- `antenne_radio/scripts/ingest/ingest_hal.py`
- `antenne_radio/scripts/export/export_obsidian.py`
- `antenne_radio/scripts/pipeline.py`
- `antenne_radio/tests/`

### Commandes de vérification

Depuis la racine du site :

```sh
git status --short
```

Depuis `antenne_radio/` :

```sh
make test
make run
tail -n 80 data/logs/api.log
tail -n 80 data/logs/pipeline.log
```

Pour une vérification rapide des compteurs, adapter selon disponibilité de `jq` :

```sh
jq -r '"total=\(length)", (group_by(.status)[] | "status \(.[0].status)=\(length)"), (group_by(.source_api)[] | "source_api \(.[0].source_api)=\(length)")' data/normalized/db.json
```

### Précautions générales

- Toujours commencer par `git status --short`.
- Toujours lire `docs/AGENTS.md` et `antenne_radio/codex_memoire_materielle.md`.
- Ne pas relancer les anciens prompts v0.1.
- Ne pas supprimer automatiquement les `ignored`.
- Ne pas écraser un item existant avec le même `id`.
- Ne pas modifier les scripts v0.1 pendant un prompt d'audit, sauf correction explicitement demandée.
- Ne pas ajouter deux connecteurs dans le même chantier.
- Ne pas publier `raw`, logs, abstracts douteux ou données privées.
- Ne pas ajouter de scraping par défaut.
- Ne jamais masquer un test échoué.

## 1. Principes de la v0.2

- Incrémentalité : une extension doit être petite, testée et réversible.
- Pas de refonte inutile : la v0.1 est une base stable, pas un brouillon à remplacer.
- Chaque étape doit avoir un critère de réussite et un critère d'arrêt.
- Chaque étape doit lancer les tests pertinents.
- Les prompts Codex doivent être autonomes, mais jamais aveugles : ils doivent lire l'état réel.
- La fin de chaque groupe de 3 prompts doit produire un handoff précis.
- Les données brutes privées sont conservées pour audit local.
- Les données publiques sont un export séparé, expurgé et minimal.
- Les logs doivent être lisibles et utiles pour comprendre un run raté.
- La publication publique est interdite tant que le prompt légal n'a pas donné un verdict favorable.
- GitHub Actions commence en manuel avec `workflow_dispatch`, jamais par cron.
- Aucun auto-commit agressif n'est autorisé en v0.2.
- Crossref et OpenAlex ne doivent pas être ajoutés ensemble.
- Les sources japonaises restent un horizon v0.3 tant que appid, conditions, formats et attribution ne sont pas verrouillés.

## 2. Limites connues de la v0.1

### Couverture

La couverture actuelle est trop étroite : deux sources RSS actives, dont une fragile, et une seule requête HAL. La v0.2 doit ajouter de meilleures sources simples avant les grands connecteurs.

### Pertinence

Le scoring lexical fonctionne mais doit mieux distinguer radio comme média, radiophonie, podcast, sound studies, radio libre, radio technique, radiologie, radiofréquence, wireless engineering et usages purement télécoms.

### Export privé

Le rapport Markdown fonctionne mais doit mieux aider la lecture : regroupements, statuts, liens, sections, candidats, bruit, items déjà vus, lisibilité des abstracts et éventuels liens vers notes.

### Droit et publication

Le pipeline stocke des abstracts et du `raw` utiles en privé. Ces champs ne sont pas publiables par défaut. Toute sortie Hugo doit être dérivée d'une whitelist stricte.

### Automatisation

La v0.1 est locale et manuelle. La v0.2 peut tester une GitHub Action manuelle, mais sans cron ni auto-commit tant que les données, secrets et artefacts ne sont pas maîtrisés.

## 3. Roadmap à difficulté croissante

### v0.1.1 - Stabilisation post-v0.1

- Objectif : consolider tests, logs, documentation et état de reprise.
- Intérêt recherche : éviter de perdre confiance dans la veille quand une source casse.
- Fichiers concernés : `tests/`, `Makefile`, `README.md`, `RESSOURCES_SUIVIES.md`, `codex_memoire_materielle.md`, éventuellement `pipeline.py` et `io.py`.
- Difficulté : faible.
- Risques : sur-ingénierie, bruit documentaire, changement inutile du pipeline stable.
- Tests obligatoires : `make test`, inspection logs, vérification des compteurs.
- Critère de réussite : une nouvelle conversation peut comprendre l'état en moins de cinq minutes.
- Critère d'arrêt : un test échoue ou une correction dépasse la stabilisation.
- Mémoire matérielle : noter les commandes, compteurs, anomalies et limites restantes.

### v0.1.2 - Sources RSS/Atom et HAL mieux configurés

- Objectif : améliorer la couverture sans changer l'architecture.
- Intérêt recherche : capter plus d'appels, revues et billets pertinents.
- Fichiers concernés : `config/sources.yaml`, `RESSOURCES_SUIVIES.md`, `ingest_rss.py`, `ingest_hal.py`, tests de fixtures.
- Difficulté : moyenne.
- Risques : flux morts, redirections, sources trop larges, HAL trop restrictif.
- Tests obligatoires : tests RSS/HAL, run manuel, rapport de santé des sources.
- Critère de réussite : chaque source a un statut humain clair et les sources cassées ne bloquent pas le pipeline.
- Critère d'arrêt : une source nécessite du scraping ou des conditions non vérifiées.
- Mémoire matérielle : noter chaque source ajoutée, désactivée ou rejetée.

### v0.1.3 - Pertinence, scoring et faux positifs

- Objectif : réduire le bruit et rendre les raisons de score plus utiles.
- Intérêt recherche : mieux prioriser les lectures et repérer les zones thématiques.
- Fichiers concernés : `keywords.yaml`, `scoring.yaml`, `scoring.py`, `test_scoring.py`, fixtures.
- Difficulté : moyenne.
- Risques : faux négatifs, pondérations opaques, score trop dépendant d'un seul mot.
- Tests obligatoires : cas positifs, cas négatifs, cas ambigus, distribution avant/après.
- Critère de réussite : moins de bruit technique en `candidate` sans perdre les items SHS importants.
- Critère d'arrêt : les bons items connus passent en `ignored`.
- Mémoire matérielle : noter les règles ajoutées et les exemples de bruit traités.

### v0.2.0 - API académique occidentale unique

- Objectif : ajouter Crossref ou OpenAlex, mais pas les deux.
- Intérêt recherche : trouver des revues sans flux RSS fiable et enrichir les DOI.
- Fichiers concernés : nouveau connecteur, `sources.yaml`, `normalize.py`, `models.py`, tests, logs.
- Difficulté : forte.
- Risques : rate limits, conditions d'usage, API key, doublons DOI, données pauvres.
- Tests obligatoires : mocks HTTP, headers de limite, erreurs 429/403/500, idempotence.
- Critère de réussite : nouveaux items normalisés sans casser RSS/HAL.
- Critère d'arrêt : documentation officielle insuffisante, secret requis non disponible, risque juridique non clair.
- Mémoire matérielle : noter l'API choisie, les conditions, limites et champs normalisés.

### v0.2.1 - Export Zotero manuel

- Objectif : produire un fichier CSL-JSON ou BibTeX importable manuellement.
- Intérêt recherche : préparer une bibliographie exploitable sans synchronisation dangereuse.
- Fichiers concernés : nouveau `export_csl.py` ou `export_bibtex.py`, `models.py`, tests, README.
- Difficulté : moyenne.
- Risques : mapping imparfait, auteurs mal encodés, types CSL incorrects.
- Tests obligatoires : fixture export, UTF-8, DOI, URL, import manuel si possible.
- Critère de réussite : fichier importable manuellement dans Zotero, sans modifier `db.json` par défaut.
- Critère d'arrêt : mapping trop pauvre pour être utile.
- Mémoire matérielle : noter le format choisi et les limites de mapping.

### v0.2.2 - GitHub Actions manuel

- Objectif : tester le pipeline en CI sur demande.
- Intérêt recherche : rendre la veille reproductible sans dépendre seulement de la machine locale.
- Fichiers concernés : `.github/workflows/`, `requirements.txt`, `Makefile`, README.
- Difficulté : moyenne.
- Risques : fuite de données, secrets, artefacts trop larges, divergence Python.
- Tests obligatoires : validation YAML, run manuel, logs, artefacts contrôlés.
- Critère de réussite : une Action `workflow_dispatch` lance tests et pipeline contrôlé sans cron.
- Critère d'arrêt : secret requis absent, données privées exposées, auto-commit envisagé.
- Mémoire matérielle : noter déclenchement, permissions, artefacts, limites.

### v0.2.3 - Données publiques filtrées

- Objectif : générer un export public expurgé pour Hugo.
- Intérêt recherche : préparer une veille partageable sans republier des contenus sous droits.
- Fichiers concernés : `scripts/export/export_public.py` ou `export_hugo.py`, tests, éventuellement `data/public/`.
- Difficulté : forte.
- Risques : fuite d'abstracts, `raw`, logs, notes privées ou métadonnées sous attribution obligatoire.
- Tests obligatoires : tests anti-fuite, JSON schema, audit de champs, build Hugo si intégré.
- Critère de réussite : JSON public ne contient que des champs whitelistés.
- Critère d'arrêt : audit légal défavorable ou attribution non résolue.
- Mémoire matérielle : noter whitelist, blacklist, verdict légal et champs publiés.

### v0.3 ou plus tard

- CiNii, NDL Search, J-STAGE.
- `changedetection.io`.
- Cron automatique.
- Auto-commit.
- Flux RSS sortant public.
- Publication complète sur le site.
- Résumés LLM.
- Scraping contrôlé éventuel, seulement si une source sans API l'autorise clairement.

## 4. Stratégie de tests et de sécurité

- Garder des tests unitaires sans réseau pour chaque connecteur.
- Ajouter une fixture brute par source nouvelle.
- Tester les erreurs HTTP et timeouts avant les runs réels.
- Tester l'idempotence de la normalisation.
- Tester explicitement les doublons par DOI et URL.
- Comparer les distributions de statuts avant/après scoring.
- Ne jamais rendre un run vert uniquement parce qu'il n'a pas levé d'exception : vérifier les compteurs.
- Capturer dans les logs les sources à 0 résultat, les redirections, les erreurs de parsing, les 429 et les timeouts.
- Prévoir des commandes de rollback simples : désactivation par `enabled: false`, pas suppression.
- Ne pas introduire de secrets dans le dépôt.
- Ne pas mettre `data/raw`, `db.json`, logs ou exports privés dans une publication publique.

## 5. Stratégie de sources

### RSS/Atom

Commencer par les sources simples et explicites : revues, carnets, plateformes de revues, appels à contributions. Chaque source doit avoir un identifiant stable, une URL, un état observé, une raison d'inclusion et une date de vérification.

### HAL

Améliorer HAL avant d'ajouter trop de nouvelles API. Explorer officiellement les champs `fl`, `fq`, `sort`, `rows`, les filtres de langue, les types de documents et les champs DOI. Tester les requêtes avec `rows=0` ou faible limite avant d'élargir.

### Crossref

Crossref est le meilleur premier connecteur académique occidental si l'objectif est de suivre des revues par ISSN et récupérer des DOI. Le connecteur doit utiliser une identification polie : `mailto`, `User-Agent`, limite basse, cache, backoff et lecture des headers de rate limit.

### OpenAlex

OpenAlex est intéressant pour la découverte large par travaux, sources et topics. Attention : les concepts historiques sont dépréciés au profit des topics dans les docs récentes consultées. Prévoir une API key si les conditions officielles actuelles l'exigent. Ne pas ajouter OpenAlex dans le même lot que Crossref.

### Zotero

Préférer un export manuel CSL-JSON ou BibTeX. Ne pas écrire dans la base Zotero, ne pas piloter l'application, ne pas synchroniser automatiquement. Les champs `zotero_uri` peuvent rester pour plus tard, après import manuel.

### Obsidian

Le rapport Markdown doit rester portable. Il peut devenir plus lisible avec des sections, statuts et liens, mais ne doit pas dépendre fortement de Dataview. Les notes personnelles relèvent d'un champ privé ou d'un fichier séparé, pas de l'export public.

### Hugo

La publication future doit passer par un fichier JSON public expurgé. Hugo peut lire des données locales JSON, mais le site ne doit recevoir que des champs explicitement publics.

### GitHub Actions

Commencer par `workflow_dispatch`. Le cron attendra un audit de stabilité. L'auto-commit attendra une décision séparée, car il peut versionner des données privées ou du bruit.

### Sources japonaises

CiNii, NDL et J-STAGE sont importants pour l'horizon du projet, mais ils demandent un audit officiel : appid, formats, attribution, conditions, encodage, XML ou JSON-LD. Ils sont probablement v0.3.

### Absence de scraping par défaut

Le scraping HTML n'est pas une stratégie par défaut. Si une source n'a ni flux ni API, il faut d'abord vérifier ToS, robots.txt, alternatives RSS/OpenSearch, et seulement ensuite décider.

## 6. Stratégie d'exports privés : Obsidian / Zotero

### Obsidian

Objectif : produire un rapport de lecture hebdomadaire plus utile, sans modifier un vrai coffre Obsidian.

Champs privés acceptables :

- `abstract`
- `raw`
- `score_explanation`
- logs de source
- notes personnelles
- éventuels marqueurs de tri

Améliorations possibles :

- section "Nouveaux items"
- section "Déjà vus"
- section "Candidats à vérifier"
- section "Bruit utile à inspecter"
- liens propres vers DOI ou URL
- résumé court des compteurs
- avertissement quand une source active retourne 0 item

### Zotero

Objectif : générer un fichier importable manuellement, sans automatisation.

Formats à étudier :

- CSL-JSON : bon candidat pour champs bibliographiques structurés.
- BibTeX : plus universel mais plus fragile pour types non standards et caractères.

Règles :

- aucun write direct dans Zotero ;
- aucun usage obligatoire de Better BibTeX ;
- pas de modification automatique de `db.json` au moment de l'export ;
- les items exportés doivent être traçables par DOI ou URL ;
- les champs non mappables doivent être documentés.

## 7. Stratégie de publication publique : Hugo / site

La publication doit présenter l'antenne comme un carnet de veille éditorialisé, pas comme une republication de contenus.

Formes possibles :

- page sobre de ressources ;
- carnet de veille expérimental ;
- "antenne" éditorialisée, avec signalement des critères ;
- index par thèmes : radio libre, sound studies, podcast, Japon, archives, appels ;
- page "Méthode / sources / limites".

Règles éditoriales :

- distinguer automatiquement détecté et humainement sélectionné ;
- mentionner "veille expérimentale" ;
- afficher les liens vers sources originales ;
- éviter de donner l'impression de republier un abstract ou une notice complète ;
- afficher les critères de sélection ;
- afficher les limites du scoring ;
- afficher les mentions d'attribution source par source ;
- ne pas publier les `raw`, logs, abstracts commerciaux, notes privées ou scores internes trop verbeux.

Champs publics probables, sous réserve d'audit :

- `id` public dérivé ou slug non sensible ;
- `title`
- `title_original` si pertinent ;
- `authors`
- `source_name`
- `source_type`
- `language`
- `published_at`
- `url`
- `doi`
- `tags` filtrés ;
- `keywords_matched` filtrés ;
- `rights`
- `source_credit`
- `curation_note` rédigée par le chercheur ;
- `discovered_at` éventuellement arrondi ou conservé.

Champs non publiables par défaut :

- `raw`
- `abstract`
- logs
- erreurs API détaillées
- requêtes avec secrets
- notes privées
- `zotero_uri`
- `notes_path`
- tout champ dont la licence n'est pas claire.

Le flux RSS sortant ne vient qu'après un export public juridiquement propre.

## 8. Audit légal et éthique obligatoire

La publication publique est interdite tant que l'audit légal n'a pas produit un verdict favorable. Le plan initial est une hypothèse de conception ; il ne suffit pas. Les conditions officielles doivent être vérifiées au moment du chantier.

### Prompt légal — Vérification complète avant publication publique

```text
Objectif :
Vérifier légalement et éthiquement si l'antenne de veille radio peut produire un export public et une page Hugo, sans republier de contenus sous droits ni violer les conditions d'utilisation des sources.

Préambule obligatoire :
1. Commence par `git status --short`.
2. Lis `docs/AGENTS.md`.
3. Lis `antenne_radio/codex_memoire_materielle.md`.
4. Lis `antenne_radio/RESSOURCES_SUIVIES.md`.
5. Lis `antenne_radio/02_plan_ad_v02.md`.
6. Ne te contente jamais du plan initial : vérifie les conditions officielles et actuelles des sources.
7. Navigue sur les pages officielles des sources et cite-les précisément.

Sources à vérifier au minimum :
- Crossref REST API.
- HAL / API archives-ouvertes.
- OpenAlex.
- Calenda.
- OpenEdition.
- Flux RSS de revues suivies ou candidates.
- NDL Search.
- CiNii Research / CiNii API.
- J-STAGE WebAPI.
- GitHub Actions, uniquement pour risques de publication d'artefacts ou secrets.
- Hugo/site public, uniquement pour distinguer build privé et exposition publique.

Questions à trancher source par source :
1. Quelles données peut-on interroger ?
2. Quelle identification est requise : User-Agent, mailto, API key, appid, autre ?
3. Quelles limites de requêtes ou règles de politesse sont imposées ?
4. Les métadonnées bibliographiques peuvent-elles être stockées en privé ?
5. Les métadonnées bibliographiques peuvent-elles être publiées publiquement ?
6. Les abstracts peuvent-ils être stockés en privé pour usage de recherche ?
7. Les abstracts peuvent-ils être publiés publiquement ?
8. Les textes intégraux, extraits longs ou pages HTML peuvent-ils être stockés ou publiés ?
9. Quelle attribution est obligatoire ?
10. Quelle licence ou mention doit accompagner les données ?
11. Y a-t-il une interdiction explicite de scraping ?
12. Si une source n'a pas d'API, que disent robots.txt et les ToS ?
13. La source autorise-t-elle un flux RSS sortant dérivé ?

Catégories de données à distinguer :
- métadonnées bibliographiques minimales ;
- abstracts ;
- textes intégraux ;
- citations courtes ;
- liens vers sources originales ;
- notes personnelles rédigées par le chercheur ;
- scores et catégories internes ;
- dumps `raw` ;
- logs ;
- secrets, appid, API keys, tokens.

Livrables :
1. Un tableau des sources officielles consultées avec :
   - source ;
   - URL officielle ;
   - date de consultation ;
   - éléments vérifiés ;
   - contrainte principale ;
   - conséquence pour le projet.
2. Une whitelist des champs publiables.
3. Une blacklist des champs à ne jamais publier.
4. Une liste des mentions d'attribution obligatoires source par source.
5. Une recommandation par défaut : ne pas publier les abstracts commerciaux.
6. Une vérification explicite que le projet n'utilise pas de scraping interdit.
7. Si pertinent, créer ou mettre à jour `antenne_radio/LEGAL_AUDIT.md`.
8. Donner un verdict final parmi :
   - publiable ;
   - publiable après corrections ;
   - non publiable.

Contraintes :
- Ne code aucune fonctionnalité nouvelle.
- Ne modifie pas les connecteurs sauf si tu découvres une fuite juridique immédiate et mineure à corriger.
- Ne donne pas de conclusion vague.
- Si une condition officielle est introuvable ou ambiguë, le verdict ne peut pas être "publiable".
- Vérifie `git status --short` à la fin.
- Mets à jour `antenne_radio/codex_memoire_materielle.md` si une décision juridique structurante est prise.
```

## 9. Série de prompts Codex groupés 3 par 3

Chaque prompt ci-dessous doit être lancé séparément. Le troisième prompt de chaque groupe sert de QA, documentation et handoff. Ne pas ouvrir le groupe suivant tant que le handoff du groupe précédent n'est pas clair.

### Groupe 1 - Stabilisation post-v0.1

- Objectif : rendre la base actuelle plus lisible, vérifiable et transmissible.
- Niveau : faible.
- Prérequis : v0.1 déjà installée, `.venv` disponible ou `make install` relançable.
- Fichiers concernés : `README.md`, `Makefile`, `tests/`, `data/logs/`, `codex_memoire_materielle.md`.
- Risques : toucher trop largement au pipeline.
- Tests obligatoires : `make test`, inspection logs, `git status --short`.
- Critère de réussite : état de départ reproductible et documenté.
- Handoff attendu : compteurs, commandes, tests, limites.

#### Prompt 1 - Audit ciblé tests/logs/docs

```text
Objectif : auditer la stabilité post-v0.1 sans modifier le comportement.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis seulement les morceaux utiles de `antenne_radio/README.md`, `antenne_radio/RESSOURCES_SUIVIES.md` et `antenne_radio/02_plan_ad_v02.md`.

Tâches :
1. Depuis `antenne_radio/`, lance `make test`.
2. Inspecte `data/logs/api.log` et `data/logs/pipeline.log` si présents.
3. Vérifie les compteurs de `data/normalized/db.json` si le fichier existe.
4. Liste les tests actuellement disponibles par fichier.
5. Repère les zones fragiles sans les corriger.

Contraintes :
- Ne code rien.
- Ne lance pas de run réseau sauf si nécessaire pour comprendre l'état.
- Ne modifie aucun fichier.

Sortie attendue :
- tests passés ou échoués ;
- compteurs observés ;
- anomalies de logs ;
- fichiers fragiles ;
- recommandations limitées pour le prompt suivant.
```

#### Prompt 2 - Petites corrections robustesse

```text
Objectif : corriger uniquement les petites fragilités révélées par le Prompt 1.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis le bilan du Prompt 1.

Tâches :
1. Corrige les problèmes simples de documentation, messages de logs, commandes Makefile ou tests si le Prompt 1 les a identifiés.
2. Ne change pas la logique métier du scoring ou de la normalisation.
3. Ajoute un test seulement si une fragilité claire peut être verrouillée sans refonte.
4. Garde les changements réversibles.

Contraintes :
- Pas de nouvelle source.
- Pas de nouveau connecteur.
- Pas de publication.
- Pas de cron.

Tests :
- Lance `make test`.
- Vérifie `git status --short`.

Critère de réussite :
- Les tests passent et la robustesse de reprise est meilleure.

Critère d'arrêt :
- Si une correction exige une refonte, documente-la seulement.
```

#### Prompt 3 - QA + mémoire matérielle + handoff

```text
Objectif : clôturer le groupe 1 par une QA complète et un handoff exploitable.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis les résultats des Prompts 1 et 2.

Tâches :
1. Lance `make test` depuis `antenne_radio/`.
2. Vérifie les fichiers modifiés avec `git diff --stat` et `git diff -- antenne_radio`.
3. Vérifie `git status --short`.
4. Mets à jour `antenne_radio/codex_memoire_materielle.md` si des décisions ou compteurs utiles ont changé.
5. Résume exactement ce qui a été fait.
6. Liste les fichiers modifiés.
7. Liste les tests passés/échoués.
8. Liste les limites restantes.
9. Donne le contexte nécessaire pour ouvrir une nouvelle conversation Codex et passer au groupe 2.

Contraintes :
- Ne commence pas le groupe 2.
- Ne masque aucun test échoué.
- Ne modifie pas les scripts hors corrections déjà prévues.
```

### Groupe 2 - Sources RSS/Atom et ressources suivies

- Objectif : améliorer la couverture simple avant les API lourdes.
- Niveau : moyen.
- Prérequis : groupe 1 terminé.
- Fichiers concernés : `config/sources.yaml`, `RESSOURCES_SUIVIES.md`, `ingest_rss.py`, tests RSS.
- Risques : sources mortes, conditions inconnues, bruit.
- Tests obligatoires : tests RSS, run limité, rapport de santé.
- Critère de réussite : sources suivies auditées et désactivables.
- Handoff attendu : liste de sources, état, décisions.

#### Prompt 4 - Audit des sources existantes

```text
Objectif : auditer les sources RSS/Atom actuelles et candidates sans les intégrer automatiquement.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis `antenne_radio/RESSOURCES_SUIVIES.md` et `antenne_radio/config/sources.yaml`.

Tâches :
1. Vérifie l'état déclaré des sources actuelles.
2. Identifie les flux cassés, redirigés ou à faible rendement.
3. Propose une petite liste de sources candidates pertinentes.
4. Pour chaque candidate, indique si elle a un flux RSS/Atom ou une API officielle.
5. Rejette toute source qui nécessiterait du scraping non vérifié.

Contraintes :
- Ne modifie aucun fichier.
- Si tu vérifies sur le web, privilégie les pages officielles.
- Ne propose pas plus de 5 candidates pour ce lot.

Sortie attendue :
- tableau source / URL / type / intérêt / risque / action proposée.
```

#### Prompt 5 - Amélioration de `RESSOURCES_SUIVIES.md` et `sources.yaml`

```text
Objectif : intégrer seulement les sources simples validées au Prompt 4.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis le bilan du Prompt 4.

Tâches :
1. Modifie `config/sources.yaml` pour ajouter ou corriger les sources RSS/Atom validées.
2. Utilise `enabled: false` pour toute source intéressante mais incertaine.
3. Mets à jour `RESSOURCES_SUIVIES.md` avec état humain, date de vérification, raison d'inclusion et risques.
4. Ne supprime pas brutalement une source existante : désactive-la si nécessaire.
5. Ajoute ou ajuste les tests RSS si la structure de config change.

Contraintes :
- Pas de scraping.
- Pas de Crossref/OpenAlex.
- Pas de source japonaise avancée.
- Pas de run réseau massif.

Tests :
- Lance `make test`.
- Lance éventuellement un run limité ou documente pourquoi il est reporté.
```

#### Prompt 6 - Tests de santé des flux + handoff

```text
Objectif : vérifier les sources RSS/Atom et produire le handoff du groupe 2.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis les Prompts 4 et 5.

Tâches :
1. Lance `make test`.
2. Lance `make run` seulement si le réseau est disponible et que les sources ajoutées sont raisonnables.
3. Vérifie `data/raw/rss_latest.json`, `data/logs/api.log` et `data/logs/pipeline.log`.
4. Vérifie `git status --short`.
5. Mets à jour `codex_memoire_materielle.md` avec sources ajoutées, désactivées, compteurs et anomalies.
6. Résume exactement les fichiers modifiés.
7. Liste les tests passés/échoués.
8. Liste les limites restantes.
9. Donne le contexte nécessaire pour ouvrir une nouvelle conversation Codex et passer au groupe 3.

Critère de réussite :
- Les sources ont un état de santé documenté.

Critère d'arrêt :
- Si un flux casse le pipeline, désactive-le ou documente le blocage.
```

### Groupe 3 - Pertinence, scoring, faux positifs

- Objectif : réduire le bruit sans perdre les signaux rares.
- Niveau : moyen.
- Prérequis : groupes 1 et 2 terminés.
- Fichiers concernés : `keywords.yaml`, `scoring.yaml`, `scoring.py`, `test_scoring.py`, fixtures.
- Risques : faux négatifs et score trop opaque.
- Tests obligatoires : fixtures positives/négatives, comparaison de distribution.
- Critère de réussite : les faux positifs techniques reculent.
- Handoff attendu : règles modifiées, exemples.

#### Prompt 7 - Audit des scores et faux positifs

```text
Objectif : comprendre les erreurs du scoring actuel avant de changer les règles.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis `keywords.yaml`, `scoring.yaml` et `scoring.py`.

Tâches :
1. Analyse la distribution actuelle des statuts.
2. Echantillonne quelques `to_read`, `candidate` et `ignored`.
3. Repère les faux positifs radio technique, radiologie, radiofrequency, wireless engineering.
4. Repère les bons items qui risqueraient d'être trop pénalisés.
5. Propose des changements de mots-clés et de pondérations avec justification.

Contraintes :
- Ne modifie rien.
- Ne supprime aucun item.
- Ne modifie aucun statut manuellement.

Sortie attendue :
- tableau exemple / score / problème / correction proposée.
```

#### Prompt 8 - Amélioration scoring explicable

```text
Objectif : améliorer le scoring lexical en restant explicable et testable.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis le bilan du Prompt 7.

Tâches :
1. Ajuste `keywords.yaml` et `scoring.yaml` de façon minimale.
2. Modifie `scoring.py` seulement si les fichiers YAML ne suffisent pas.
3. Conserve `score_explanation`.
4. Préserve les items `exported`.
5. Ne supprime pas les `ignored`.
6. Ajoute des tests pour les cas positifs, négatifs et ambigus.

Tests :
- Lance `make test`.
- Si tu rescoring des données réelles, documente précisément l'effet sur la distribution.

Critère de réussite :
- Les explications restent compréhensibles et les tests couvrent le bruit principal.
```

#### Prompt 9 - Fixtures + QA + handoff

```text
Objectif : verrouiller le scoring par fixtures, QA complète et handoff.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis les Prompts 7 et 8.

Tâches :
1. Vérifie que les tests couvrent au moins un item très pertinent, un candidat, un bruit technique, un cas radiologie/radiofrequency et un item déjà `exported`.
2. Lance `make test`.
3. Vérifie la distribution réelle si `db.json` a été rescored.
4. Vérifie `git status --short`.
5. Mets à jour `codex_memoire_materielle.md` avec règles, distributions et limites.
6. Résume les fichiers modifiés.
7. Liste les tests passés/échoués.
8. Liste les limites restantes.
9. Donne le contexte nécessaire pour ouvrir une nouvelle conversation Codex et passer au groupe 4.
```

### Groupe 4 - Export Obsidian amélioré

- Objectif : rendre le rapport hebdomadaire plus utile.
- Niveau : moyen.
- Prérequis : groupe 3 terminé.
- Fichiers concernés : `export_obsidian.py`, `test_export_obsidian.py`, README.
- Risques : Markdown trop complexe, dépendance Obsidian non portable.
- Tests obligatoires : snapshot Markdown, UTF-8, non-modification par défaut.
- Critère de réussite : rapport plus lisible, sans écrire dans un vault réel.
- Handoff attendu : format exact du rapport.

#### Prompt 10 - Audit de l'export actuel

```text
Objectif : auditer l'export Obsidian actuel avant modification.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis `export_obsidian.py` et `test_export_obsidian.py`.

Tâches :
1. Inspecte `data/exports/veille-YYYY-WW.md` si présent.
2. Note les défauts de lisibilité.
3. Vérifie si le HTML RSS brut gêne la lecture.
4. Propose une structure Markdown améliorée.
5. Préserve la portabilité : pas de dépendance obligatoire à Dataview.

Contraintes :
- Ne modifie rien.
- Ne marque aucun item comme `exported`.
```

#### Prompt 11 - Rapport plus lisible et utile

```text
Objectif : améliorer le Markdown privé sans changer le sens des données.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis le bilan du Prompt 10.

Tâches :
1. Améliore `export_obsidian.py` pour rendre le rapport plus lisible.
2. Conserve le frontmatter utile.
3. Conserve les sections `À lire` et `Candidats`, sauf justification claire.
4. Ajoute éventuellement compteurs, source, statut, score, explication, lien DOI/URL.
5. Nettoie ou neutralise le HTML dans les abstracts si cela reste privé et utile.
6. Ne change pas `db.json` par défaut.
7. Mets à jour les tests.

Tests :
- Lance `make test`.
- Génère un export sur fixture ou données réelles sans `--mark-exported`.
```

#### Prompt 12 - Tests Markdown/UTF-8 + handoff

```text
Objectif : clôturer l'export Obsidian avec QA complète et handoff.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis les Prompts 10 et 11.

Tâches :
1. Lance `make test`.
2. Vérifie que les caractères japonais restent lisibles.
3. Vérifie que l'export ne modifie pas `db.json` par défaut.
4. Vérifie que `--mark-exported` conserve le comportement attendu si ce chemin existe encore.
5. Vérifie `git status --short`.
6. Mets à jour `codex_memoire_materielle.md` si le format du rapport change.
7. Résume fichiers modifiés, tests, limites et format final.
8. Donne le contexte nécessaire pour ouvrir une nouvelle conversation Codex et passer au groupe 5.
```

### Groupe 5 - Zotero / CSL-JSON manuel

- Objectif : préparer un export bibliographique privé, importable manuellement.
- Niveau : moyen.
- Prérequis : export Obsidian stabilisé.
- Fichiers concernés : `scripts/export/`, tests, README.
- Risques : mapping bibliographique incorrect.
- Tests obligatoires : fixture CSL/BibTeX, UTF-8, DOI, URL.
- Critère de réussite : import manuel plausible, aucune synchronisation automatique.
- Handoff attendu : format choisi et limites.

#### Prompt 13 - Étude de faisabilité

```text
Objectif : choisir entre CSL-JSON et BibTeX pour un export Zotero manuel minimal.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis les modèles de données et l'export Obsidian.

Tâches :
1. Vérifie la documentation officielle Zotero actuelle pour les formats importables.
2. Compare CSL-JSON et BibTeX pour les champs disponibles dans `RadioWatchItem`.
3. Identifie les champs non mappables.
4. Propose un format unique pour v0.2.1.
5. Définis le périmètre : export manuel, pas de sync, pas d'écriture dans Zotero.

Contraintes :
- Ne code rien.
- Cite les docs officielles consultées.
```

#### Prompt 14 - Export manuel minimal

```text
Objectif : implémenter l'export Zotero manuel choisi au Prompt 13.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis le bilan du Prompt 13.

Tâches :
1. Crée un export minimal dans `scripts/export/`.
2. Ecris dans `data/exports/` ou un sous-dossier privé équivalent, pas dans un vrai Zotero.
3. Mappe title, authors, date, DOI, URL, source, type quand possible.
4. Ne modifie pas `db.json` par défaut.
5. Ajoute des tests avec `tmp_path`.
6. Documente les limites du mapping.

Tests :
- Lance `make test`.
```

#### Prompt 15 - Tests d'import + handoff

```text
Objectif : vérifier l'export Zotero manuel et transmettre le contexte.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis les Prompts 13 et 14.

Tâches :
1. Lance `make test`.
2. Vérifie la syntaxe du fichier exporté.
3. Si possible, décris la procédure d'import manuel dans Zotero sans automatiser l'application.
4. Vérifie `git status --short`.
5. Mets à jour `codex_memoire_materielle.md` avec format choisi, chemins et limites.
6. Résume fichiers modifiés, tests, limites.
7. Donne le contexte nécessaire pour ouvrir une nouvelle conversation Codex et passer au groupe 6.
```

### Groupe 6 - Crossref ou OpenAlex

- Objectif : ajouter une API académique occidentale unique.
- Niveau : fort.
- Prérequis : groupes 1 à 5 terminés.
- Fichiers concernés : `config/sources.yaml`, nouveau connecteur, `normalize.py`, `models.py`, tests.
- Risques : conditions, rate limits, API key, doublons.
- Tests obligatoires : mocks, backoff, erreurs HTTP, idempotence.
- Critère de réussite : un seul connecteur nouveau, désactivable, testé.
- Handoff attendu : API choisie, conditions, champs.

#### Prompt 16 - Recherche officielle API / conditions / rate limits

```text
Objectif : choisir officiellement entre Crossref et OpenAlex pour v0.2.0.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis `RESSOURCES_SUIVIES.md`, `sources.yaml` et `02_plan_ad_v02.md`.

Tâches :
1. Consulte les docs officielles actuelles de Crossref.
2. Consulte les docs officielles actuelles d'OpenAlex.
3. Vérifie User-Agent, mailto, API key, rate limits, headers, backoff et conditions.
4. Vérifie la meilleure stratégie : Crossref par ISSN ou OpenAlex par works/sources/topics.
5. Choisis une seule API pour ce groupe.
6. Propose les champs à stocker en brut et à normaliser.

Contraintes :
- Ne code rien.
- Cite les URLs officielles.
- Si une API key est nécessaire et absente, ne choisis cette API que pour un spike désactivé.
```

#### Prompt 17 - Implémentation du connecteur choisi

```text
Objectif : implémenter le connecteur choisi au Prompt 16, en mode brut et désactivable.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis le bilan du Prompt 16.

Tâches :
1. Ajoute la configuration nécessaire dans `sources.yaml`.
2. Crée un seul connecteur : Crossref ou OpenAlex.
3. Ecris un dump brut séparé dans `data/raw/`.
4. Logue erreurs HTTP, timeouts, 429, 403 et réponses inattendues.
5. Respecte User-Agent, mailto ou API key selon documentation officielle.
6. N'écris pas directement dans `db.json` depuis le connecteur.
7. Ajoute des tests mockés.

Contraintes :
- Pas de deuxième API.
- Pas de publication.
- Pas de secret dans le dépôt.
```

#### Prompt 18 - Mocks, backoff, QA + handoff

```text
Objectif : sécuriser le connecteur API par mocks, QA et handoff.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis les Prompts 16 et 17.

Tâches :
1. Lance `make test`.
2. Vérifie les tests de succès, timeout, erreur HTTP, 429 et backoff si applicable.
3. Vérifie que le connecteur est désactivable.
4. Vérifie que les données brutes restent dans `data/raw/`.
5. Si normalisation ajoutée, vérifie l'idempotence et les doublons DOI/URL.
6. Vérifie `git status --short`.
7. Mets à jour `RESSOURCES_SUIVIES.md` et `codex_memoire_materielle.md`.
8. Résume API choisie, fichiers modifiés, tests, limites, conditions officielles.
9. Donne le contexte nécessaire pour ouvrir une nouvelle conversation Codex et passer au groupe 7.
```

### Groupe 7 - GitHub Actions manuel

- Objectif : tester une exécution CI contrôlée.
- Niveau : moyen.
- Prérequis : pipeline local stable.
- Fichiers concernés : `.github/workflows/`, README, éventuellement Makefile.
- Risques : secrets, artefacts, fuite de données.
- Tests obligatoires : validation YAML, run manuel si possible.
- Critère de réussite : workflow manuel sans cron.
- Handoff attendu : permissions, secrets, artefacts.

#### Prompt 19 - Audit CI possible

```text
Objectif : déterminer ce qu'une GitHub Action peut faire sans risque.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis le pipeline actuel.

Tâches :
1. Vérifie les commandes nécessaires en CI.
2. Identifie les secrets éventuels.
3. Détermine quels artefacts peuvent être conservés sans publier de données privées.
4. Propose un workflow `workflow_dispatch` minimal.
5. Refuse cron et auto-commit pour ce groupe.

Contraintes :
- Ne code rien.
- Ne crée pas de workflow avant décision.
```

#### Prompt 20 - Workflow `workflow_dispatch`

```text
Objectif : créer une GitHub Action manuelle minimale.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis le bilan du Prompt 19.

Tâches :
1. Crée `.github/workflows/antenne-radio.yml`.
2. Utilise uniquement `workflow_dispatch`.
3. Installe Python et dépendances de `antenne_radio/requirements.txt`.
4. Lance `make test`.
5. Ne configure pas de cron.
6. Ne configure pas d'auto-commit.
7. N'upload pas d'artefact privé sauf justification explicite.

Tests :
- Vérifie la syntaxe YAML.
- Lance les tests locaux si possible.
```

#### Prompt 21 - Test sans cron, logs, handoff

```text
Objectif : clôturer la GitHub Action manuelle avec QA et handoff.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis les Prompts 19 et 20.

Tâches :
1. Lance `make test` localement.
2. Vérifie que le workflow ne contient ni `schedule`, ni auto-commit.
3. Vérifie que les secrets ne sont pas écrits en clair.
4. Vérifie les permissions GitHub minimales.
5. Vérifie `git status --short`.
6. Mets à jour README ou mémoire matérielle si nécessaire.
7. Résume fichiers modifiés, tests, limites.
8. Donne le contexte nécessaire pour ouvrir une nouvelle conversation Codex et passer au groupe 8.
```

### Groupe 8 - Export public expurgé

- Objectif : produire des données publiques sans fuite.
- Niveau : fort.
- Prérequis : audit interne des champs, pas encore publication.
- Fichiers concernés : nouvel export public, tests, `data/public/`.
- Risques : abstracts, raw, logs, notes privées.
- Tests obligatoires : anti-fuite, schema, UTF-8.
- Critère de réussite : JSON public whitelisté.
- Handoff attendu : whitelist, blacklist.

#### Prompt 22 - Définition whitelist/blacklist champs publics

```text
Objectif : définir les champs publics avant de coder l'export.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis `models.py`, `db.json` si présent et `02_plan_ad_v02.md`.

Tâches :
1. Liste tous les champs actuels de `RadioWatchItem`.
2. Propose une whitelist public.
3. Propose une blacklist absolue.
4. Distingue publication technique et publication éditorialisée.
5. Indique les champs qui attendent l'audit légal.

Contraintes :
- Ne code rien.
- Par défaut, `abstract`, `raw`, logs, `zotero_uri`, `notes_path` et notes privées sont non publiables.
```

#### Prompt 23 - `export_public` ou `export_hugo`

```text
Objectif : créer un export public expurgé, sans intégration Hugo complète.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis le bilan du Prompt 22.

Tâches :
1. Crée `scripts/export/export_public.py` ou `export_hugo.py`.
2. Lis `db.json`.
3. Ecris un JSON public dans `data/public/`.
4. N'exporte que les champs whitelistés.
5. Supprime ou neutralise les abstracts.
6. Exclue `raw`, logs et champs privés.
7. Ajoute des tests anti-fuite.

Contraintes :
- Ne crée pas de page Hugo dans ce prompt.
- Ne publie rien.
```

#### Prompt 24 - Tests anti-fuite abstracts + handoff

```text
Objectif : vérifier l'export public et transmettre le contexte.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis les Prompts 22 et 23.

Tâches :
1. Lance `make test`.
2. Vérifie que le JSON public ne contient aucun `abstract`, `raw`, log, secret, `zotero_uri` ou `notes_path`.
3. Vérifie les caractères UTF-8.
4. Vérifie `git status --short`.
5. Mets à jour `codex_memoire_materielle.md` avec whitelist, blacklist et chemin d'export.
6. Résume fichiers modifiés, tests, limites.
7. Donne le contexte nécessaire pour ouvrir une nouvelle conversation Codex et passer au groupe 9.

Critère d'arrêt :
- Si une fuite est détectée, corrige avant handoff.
```

### Groupe 9 - Audit légal avant site

- Objectif : décider si l'export public est publiable.
- Niveau : fort.
- Prérequis : export public expurgé disponible.
- Fichiers concernés : `LEGAL_AUDIT.md`, `RESSOURCES_SUIVIES.md`, mémoire.
- Risques : conclusion vague, source non vérifiée.
- Tests obligatoires : vérification officielle source par source.
- Critère de réussite : verdict clair.
- Handoff attendu : publiable ou corrections obligatoires.

#### Prompt 25 - Recherche officielle source par source

```text
Objectif : vérifier les conditions officielles et actuelles de chaque source avant publication.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis lis le Prompt légal dans `02_plan_ad_v02.md`.

Tâches :
1. Exécute le Prompt légal sans écrire encore `LEGAL_AUDIT.md`.
2. Consulte les pages officielles des sources réellement utilisées et des sources prévues.
3. Cite les URLs officielles.
4. Distingue stockage privé et publication publique.
5. Identifie les mentions d'attribution obligatoires.

Contraintes :
- Ne code rien.
- Si une source est ambiguë, marque-la bloquante.
```

#### Prompt 26 - Rédaction `LEGAL_AUDIT.md`

```text
Objectif : formaliser l'audit légal.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis le bilan du Prompt 25.

Tâches :
1. Crée ou mets à jour `antenne_radio/LEGAL_AUDIT.md`.
2. Ajoute le tableau des sources officielles consultées.
3. Ajoute whitelist et blacklist.
4. Ajoute mentions d'attribution source par source.
5. Ajoute verdict provisoire.
6. Liste les corrections obligatoires avant Hugo.

Contraintes :
- Ne modifie pas les connecteurs.
- Ne publie rien.
```

#### Prompt 27 - Verdict publication + corrections obligatoires

```text
Objectif : produire le verdict légal final avant toute intégration site.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis les Prompts 25 et 26.

Tâches :
1. Relis `LEGAL_AUDIT.md`.
2. Vérifie que chaque source a une URL officielle et une conséquence projet.
3. Vérifie que les abstracts commerciaux sont exclus par défaut.
4. Vérifie que l'export public respecte whitelist/blacklist.
5. Lance `make test` si l'export public existe.
6. Vérifie `git status --short`.
7. Mets à jour `codex_memoire_materielle.md` avec le verdict.
8. Donne un verdict : publiable, publiable après corrections, ou non publiable.
9. Liste les corrections obligatoires avant groupe 10.
10. Donne le contexte nécessaire pour ouvrir une nouvelle conversation Codex et passer au groupe 10 seulement si le verdict le permet.

Critère d'arrêt :
- Si le verdict n'est pas favorable, ne pas lancer le groupe 10.
```

### Groupe 10 - Préparation publication Hugo/site

- Objectif : intégrer sobrement l'antenne au site, seulement après verdict légal favorable.
- Niveau : fort.
- Prérequis : groupe 9 favorable.
- Fichiers concernés : export public, layouts/content Hugo, CSS si nécessaire.
- Risques : publication trop riche, fuite, esthétique disproportionnée.
- Tests obligatoires : build Hugo, anti-fuite, accessibilité de base.
- Critère de réussite : page sobre, sourcée, non trompeuse.
- Handoff attendu : go/no-go publication.

#### Prompt 28 - Conception éditoriale de la page

```text
Objectif : concevoir la présentation publique de l'antenne sans coder.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis `LEGAL_AUDIT.md` et le verdict du Prompt 27.

Tâches :
1. Propose une page sobre de veille expérimentale.
2. Distingue données automatiques et sélection humaine.
3. Propose une page ou section "Méthode / sources / limites".
4. Propose les filtres utiles : thème, langue, source, date, type.
5. Définis les mentions visibles.
6. Confirme que les abstracts ne seront pas affichés sauf autorisation explicite.

Contraintes :
- Ne code rien.
- Ne lance pas Hugo.
```

#### Prompt 29 - Intégration Hugo sobre

```text
Objectif : intégrer la veille publique dans Hugo avec un rendu sobre et minimal.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis le Prompt 28 et `LEGAL_AUDIT.md`.

Tâches :
1. Utilise uniquement l'export public expurgé.
2. Crée ou ajuste les fichiers Hugo nécessaires.
3. Affiche titre, auteurs, source, date, DOI/URL, type, tags publics, attribution.
4. Ajoute une page ou section "Méthode / sources / limites".
5. Ne crée pas de flux RSS sortant sauf si l'audit légal l'autorise explicitement.
6. Respecte le style lightweight du site.

Contraintes :
- Ne pas publier `raw`, `abstract`, logs ou notes privées.
- Pas de refonte esthétique radicale.
```

#### Prompt 30 - QA finale, build, accessibilité, handoff publication

```text
Objectif : vérifier l'intégration Hugo et donner un go/no-go publication.

Au début, lance `git status --short`, lis `docs/AGENTS.md`, lis `antenne_radio/codex_memoire_materielle.md`, puis relis les Prompts 28 et 29.

Tâches :
1. Lance les tests antenne pertinents.
2. Lance le build Hugo avec la commande projet recommandée dans `docs/AGENTS.md`.
3. Vérifie que la page n'affiche aucun abstract, raw, log, secret, note privée ou champ interdit.
4. Vérifie les liens source/DOI.
5. Vérifie les mentions d'attribution.
6. Vérifie la lisibilité mobile de base si une page a été créée.
7. Vérifie `git status --short`.
8. Mets à jour `codex_memoire_materielle.md` avec l'état de publication.
9. Résume fichiers modifiés, tests passés/échoués, limites restantes.
10. Donne un verdict : prêt pour publication, prêt après corrections listées, ou non prêt.
11. Donne le contexte nécessaire pour une future conversation Codex.

Critère d'arrêt :
- Toute fuite de champ interdit bloque la publication.
```

## 10. Handoff entre conversations Codex

Chaque fin de groupe doit produire un bloc de handoff contenant :

- groupe terminé ;
- date et heure locale si utile ;
- branche ou état git ;
- fichiers modifiés ;
- commandes lancées ;
- tests passés ;
- tests échoués ;
- compteurs observés ;
- sources ajoutées/désactivées ;
- décisions structurantes ;
- limites restantes ;
- prochain groupe recommandé ;
- raison de ne pas passer au groupe suivant si blocage.

La mémoire matérielle `antenne_radio/codex_memoire_materielle.md` doit être mise à jour quand un changement modifie la manière de reprendre le projet.

## 11. Critères avant publication publique

- `LEGAL_AUDIT.md` existe ou une section équivalente documente l'audit.
- Le verdict légal est `publiable` ou `publiable après corrections`, et toutes les corrections obligatoires sont faites.
- L'export public est généré depuis une whitelist.
- Les tests anti-fuite passent.
- Aucun abstract commercial n'est publié par défaut.
- Aucun `raw`, log, secret, note privée, `zotero_uri` ou `notes_path` n'est publié.
- Les mentions d'attribution sont visibles.
- Les liens pointent vers les sources originales.
- La page explique le caractère expérimental et les limites de la veille.
- Le build Hugo passe.
- `git status --short` est compris.

## 12. Checklist avant de lancer la v0.2

- [ ] `git status --short` lu.
- [ ] `docs/AGENTS.md` lu.
- [ ] `codex_memoire_materielle.md` lu.
- [ ] `make test` passe.
- [ ] `RESSOURCES_SUIVIES.md` correspond à `config/sources.yaml`.
- [ ] Les compteurs de `db.json` sont connus.
- [ ] Les logs récents sont consultés.
- [ ] Le groupe de prompts choisi est identifié.
- [ ] Un seul objectif est lancé à la fois.

## 13. Checklist avant publication publique

- [ ] Groupe 8 terminé.
- [ ] Groupe 9 terminé.
- [ ] Verdict légal favorable.
- [ ] Whitelist et blacklist figées.
- [ ] Tests anti-fuite passés.
- [ ] Attributions obligatoires présentes.
- [ ] Page "Méthode / sources / limites" prête.
- [ ] Build Hugo passé.
- [ ] Aucune donnée privée exposée.

## 14. Checklist avant cron automatique

- [ ] GitHub Action manuelle fonctionne plusieurs fois.
- [ ] Les logs sont compréhensibles.
- [ ] Les erreurs réseau n'écrasent pas les données utiles.
- [ ] Les sources à problème sont désactivables.
- [ ] Aucun secret n'est logué.
- [ ] Aucun artefact privé n'est publié.
- [ ] L'auto-commit a fait l'objet d'un prompt séparé.
- [ ] Le volume de changements automatiques est acceptable.
- [ ] Un rollback simple existe.

## 15. Ne pas faire pour l'instant

- Ne pas ajouter Crossref et OpenAlex dans le même chantier.
- Ne pas ajouter CiNii, NDL et J-STAGE en v0.2 sans audit dédié.
- Ne pas publier les abstracts commerciaux.
- Ne pas publier `raw`.
- Ne pas publier les logs.
- Ne pas automatiser Zotero.
- Ne pas écrire dans un vrai vault Obsidian.
- Ne pas créer de cron.
- Ne pas créer d'auto-commit.
- Ne pas scraper une page faute de flux sans vérifier ToS et robots.txt.
- Ne pas créer un mini site Hugo séparé si l'intégration au site existant suffit.
- Ne pas transformer l'antenne en service serveur.

## 16. À reporter v0.3

Le plan général complet contient encore au moins une phase v0.3/v1.0 :

intégrations japonaises : CiNii, NDL, J-STAGE ;
surveillance de pages sans API, probablement via changedetection.io ;
cron automatique ;
auto-commit contrôlé ;
flux RSS sortant ;
publication publique plus complète par taxonomies ;
durcissement long terme après plusieurs runs réels.

- CiNii Research avec appid.
- NDL Search avec attribution publique.
- J-STAGE WebAPI XML.
- `changedetection.io`.
- Détection fuzzy avancée.
- Flux RSS sortant public.
- Cron automatique.
- Auto-commit contrôlé.
- Résumés LLM.
- Interface Hugo plus riche.

## 17. Comment ouvrir une nouvelle conversation Codex sans perte de contexte

Message minimal recommandé :

```text
Lis `docs/AGENTS.md`, `antenne_radio/codex_memoire_materielle.md`, `antenne_radio/02_plan_ad_v02.md` et `antenne_radio/RESSOURCES_SUIVIES.md`.

Nous reprenons l'antenne de veille radio après la v0.1 stable.
Ne relance pas les anciens prompts v0.1.
Commence par `git status --short`.
Je veux lancer le groupe X, prompt Y du plan v0.2.
Respecte les critères de réussite, critères d'arrêt, tests et handoff du fichier `02_plan_ad_v02.md`.
```

Si la conversation précédente a produit un handoff, le coller après ce message.

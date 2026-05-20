# 04_master_plan — Antenne de veille radio, de la v0.1 stable à la v1

Ce fichier remplace les plans dispersés `02_plan_ad_v02.md` et `03_plan_ad_v1.md` comme plan de travail principal.  
Il ne remplace pas la mémoire matérielle : `antenne_radio/codex_memoire_materielle.md` reste la source de vérité factuelle sur l’état réel du dépôt.

## 0. Intention générale

L’objectif n’est plus de lancer une longue suite de conversations Codex qui redécouvrent sans cesse le projet.  
L’objectif est d’amener l’antenne de veille vers une **v1 sobre, fiable, testée, documentée et publiable seulement si l’audit légal l’autorise**.

La v1 ne signifie pas “tout intégrer”.  
La v1 signifie :

- conserver les acquis de la v0.1 stable ;
- améliorer la qualité du signal ;
- ajouter au plus une API académique occidentale si elle est vraiment utile ;
- produire des exports privés utiles ;
- produire, si possible, un export public strictement expurgé ;
- préparer une intégration Hugo sobre ;
- tester une automatisation contrôlée, sans cron agressif ni auto-commit risqué ;
- documenter clairement les limites et les reports.

## 1. Point de départ : acquis v0.1 à ne pas refaire

La v0.1 est considérée comme stable. Elle ne doit pas être reconstruite.

Acquis à préserver :

- sous-projet dans `antenne_radio/` ;
- ingestion RSS/Atom ;
- ingestion HAL ;
- dumps bruts dans `data/raw/` ;
- normalisation en `RadioWatchItem` ;
- base normalisée dans `data/normalized/db.json` ;
- dédoublonnage strict par identifiant stable ;
- conservation de `raw` en privé ;
- scoring lexical explicable ;
- statuts `new`, `candidate`, `to_read`, `ignored`, `exported` ;
- export Markdown Obsidian ;
- pipeline local `scripts/pipeline.py` ;
- commandes Makefile ;
- tests existants ;
- documentation `README.md`, `01_RESSOURCES_SUIVIES.md`, `codex_memoire_materielle.md`.

Ne pas relancer les prompts de construction v0.1.  
Ne pas transformer un chantier de consolidation en refonte.

## 2. Définition de la v1 retenue

La v1 visée ici est une **v1 minimale forte**, pas une v1 encyclopédique.

Elle doit aboutir à :

1. un pipeline local toujours fonctionnel ;
2. une couverture RSS/HAL mieux configurée et documentée ;
3. un scoring moins bruyant, avec cas négatifs explicites ;
4. un dédoublonnage plus utile mais non destructeur ;
5. un export Obsidian plus lisible ;
6. un export Zotero manuel, probablement CSL-JSON ou BibTeX ;
7. au plus un connecteur académique occidental supplémentaire, Crossref ou OpenAlex, seulement après audit ;
8. un export public expurgé par whitelist ;
9. un audit légal source par source ;
10. une intégration Hugo sobre si, et seulement si, l’audit est favorable ;
11. une GitHub Action manuelle `workflow_dispatch`, sans cron par défaut ;
12. une documentation de reprise qui permet à une nouvelle conversation Codex de comprendre l’état réel rapidement.

## 3. Ce qui est volontairement reporté en bonus

Ces éléments ne sont pas supprimés du projet. Ils sont sortis de la trajectoire v1 principale.

À garder pour plus tard, seulement si le besoin devient clair :

- CiNii ;
- NDL Search ;
- J-STAGE ;
- `changedetection.io` ;
- surveillance de pages sans flux/API ;
- flux RSS sortant public ;
- cron automatique ;
- auto-commit ;
- écriture automatique dans Zotero ;
- écriture automatique dans un coffre Obsidian réel ;
- résumés LLM ;
- scraping HTML ;
- service serveur permanent ;
- interface d’administration.

Règle : si l’un de ces bonus devient indispensable, il devra être lancé comme cartouche autonome après la v1, avec audit légal et tests dédiés.

## 4. Discipline commune à toutes les conversations Codex

### 4.1. Principe de continuité

Le premier prompt de chaque conversation doit obliger Codex à relire le contexte réel, mais seulement la partie utile.  
Le dernier prompt de chaque conversation doit obliger Codex à écrire l’état réel dans `codex_memoire_materielle.md`.

Cette règle évite deux problèmes :

- Codex qui repart d’un ancien plan au lieu de l’état réel ;
- Codex qui termine un chantier sans laisser de handoff exploitable.

### 4.2. Clause d’ouverture à inclure dans le premier prompt de chaque conversation

Chaque premier prompt de conversation doit contenir une version adaptée de cette clause :

```text
Avant toute action, lance `git status --short`.

Lis ensuite :
- `docs/AGENTS.md` ;
- `antenne_radio/codex_memoire_materielle.md`, en priorité les sections liées au chantier actuel ;
- `antenne_radio/README.md` ;
- `antenne_radio/01_RESSOURCES_SUIVIES.md` si le chantier touche aux sources ;
- `antenne_radio/04_master_plan.md`, uniquement la conversation en cours et les règles générales.

Ne suppose jamais que le plan décrit l’état réel. Vérifie les fichiers existants avant de modifier quoi que ce soit.
```

### 4.3. Clause de clôture à inclure dans le dernier prompt de chaque conversation

Chaque dernier prompt de conversation doit contenir une version adaptée de cette clause :

```text
À la fin, mets à jour `antenne_radio/codex_memoire_materielle.md` avec un bilan factuel :
- date ;
- objectif du chantier ;
- fichiers modifiés ;
- commandes lancées ;
- tests passés ou échoués ;
- compteurs observés si `db.json` existe ;
- décisions prises ;
- limites restantes ;
- prochain chantier recommandé.

Ajoute aussi un court handoff prêt à copier dans une nouvelle conversation Codex.
Ne masque aucun échec de test.
```

### 4.4. Règles de sécurité

- Toujours commencer par `git status --short`.
- Ne jamais revert des changements hors périmètre.
- Ne jamais supprimer automatiquement les `ignored`.
- Ne jamais publier `raw`, logs, notes privées, abstracts sous droits ou données non auditées.
- Ne pas ajouter deux connecteurs complexes dans la même conversation.
- Ne pas introduire de secret dans le dépôt.
- Ne pas faire de cron avant validation manuelle stable.
- Ne pas faire d’auto-commit vers `main`.
- Préférer `enabled: false` à la suppression d’une source.
- En cas d’ambiguïté légale : documenter et reporter.

## 5. Vue d’ensemble du nouveau groupement

Total : **9 conversations**, **25 prompts**.

C’est volontairement plus court que les anciens plans.

| Conversation | Sujet | Prompts | Difficulté | Résultat attendu |
|---:|---|---:|---|---|
| 1 | Audit de reprise et gel du périmètre v1 | 2 | faible | état réel + périmètre v1 confirmé |
| 2 | Sources RSS/HAL et documentation des sources | 3 | moyenne | sources mieux tenues, sans nouvelle API complexe |
| 3 | Scoring, bruit, faux positifs, doublons non destructeurs | 3 | moyenne | meilleur signal sans perdre les bons items |
| 4 | Export Obsidian et export Zotero manuel | 3 | moyenne | exports privés réellement utiles |
| 5 | API occidentale unique : Crossref ou OpenAlex | 3 | forte | un connecteur ou un report documenté |
| 6 | Contrat public et audit légal | 3 | forte | whitelist publique + `LEGAL_AUDIT.md` |
| 7 | Export public et Hugo sobre | 3 | forte | intégration site possible, sinon désactivée |
| 8 | GitHub Actions manuelle | 3 | moyenne | CI déclenchable à la demande, sans cron |
| 9 | Release candidate v1 | 2 | moyenne | verdict v1, documentation et handoff final |

## 6. Conversations et prompts Codex

---

# Conversation 1 — Audit de reprise et gel du périmètre v1

Nombre optimal : **2 prompts**.  
But : éviter de partir dans tous les sens. Cette conversation ne doit pas “coder” la v1 ; elle doit établir une photographie fiable et décider ce qui est vraiment inclus.

## Prompt 1 — Audit réel de reprise v0.1 stable

```text
Objectif : établir l’état réel de l’antenne avant de lancer le master plan v1.

Avant toute action, lance `git status --short`.

Lis ensuite :
- `docs/AGENTS.md` ;
- `antenne_radio/codex_memoire_materielle.md`, en priorité `Reprise rapide`, `État actuel du pipeline`, `Données présentes`, `Contrats de données à préserver` et `Fragilités` ;
- `antenne_radio/README.md` ;
- `antenne_radio/01_RESSOURCES_SUIVIES.md` ;
- `antenne_radio/04_master_plan.md`, sections 0 à 5 et Conversation 1 seulement.

Tâches :
1. Depuis `antenne_radio/`, lance `make test`.
2. Vérifie si `data/normalized/db.json` existe.
3. Si oui, calcule les compteurs : total, statuts, `source_api`, présence de `raw`.
4. Inspecte rapidement les derniers logs disponibles : `data/logs/api.log` et `data/logs/pipeline.log` s’ils existent.
5. Vérifie quels éléments v0.1 sont réellement présents : RSS, HAL, normalisation, scoring, export Obsidian, pipeline, tests, README, ressources suivies.
6. Liste ce qui manque vraiment pour une v1 minimale forte.

Contraintes :
- Ne modifie aucun fichier.
- Ne lance pas de run réseau sauf si les tests ou les fichiers l’exigent explicitement.
- Ne relance aucun ancien prompt v0.1.
- Ne transforme pas l’audit en refonte.

Sortie attendue :
- état Git ;
- résultat des tests ;
- compteurs observés ;
- acquis confirmés ;
- fragilités confirmées ;
- liste courte des chantiers v1 nécessaires ;
- liste courte des bonus à reporter.
```

## Prompt 2 — Gel du périmètre v1 + mémoire matérielle

```text
Objectif : clore la reprise et fixer le périmètre v1 à partir de l’audit réel.

Au début, lance `git status --short`, relis `docs/AGENTS.md`, `antenne_radio/codex_memoire_materielle.md`, puis relis le bilan du Prompt 1.

Tâches :
1. Crée ou mets à jour un court fichier `antenne_radio/V1_SCOPE.md`.
2. Il doit contenir :
   - ce qui est inclus dans la v1 ;
   - ce qui est explicitement reporté ;
   - les critères de réussite v1 ;
   - les critères d’arrêt ;
   - la liste des conversations restantes du master plan.
3. Ne duplique pas tout `04_master_plan.md`.
4. Lance `git diff --check -- antenne_radio/V1_SCOPE.md`.
5. Mets à jour `antenne_radio/codex_memoire_materielle.md` avec un bilan factuel :
   - date ;
   - objectif du chantier ;
   - fichiers modifiés ;
   - commandes lancées ;
   - tests passés ou échoués ;
   - compteurs observés si `db.json` existe ;
   - décisions prises ;
   - limites restantes ;
   - prochain chantier recommandé.
6. Ajoute aussi un court handoff prêt à copier dans une nouvelle conversation Codex.

Contraintes :
- Ne modifie aucun code.
- Ne masque aucun échec de test.
- Ne commence pas la conversation 2.
```

---

# Conversation 2 — Sources RSS/HAL et documentation des sources

Nombre optimal : **3 prompts**.  
But : améliorer la couverture sans ajouter de nouvelle API lourde.

## Prompt 3 — Audit des sources actuelles RSS/HAL

```text
Objectif : comprendre et améliorer les sources existantes sans changer l’architecture.

Avant toute action, lance `git status --short`.

Lis ensuite :
- `docs/AGENTS.md` ;
- `antenne_radio/codex_memoire_materielle.md`, en priorité les sections sur sources RSS/HAL, données présentes, fragilités et dernier run ;
- `antenne_radio/README.md` ;
- `antenne_radio/01_RESSOURCES_SUIVIES.md` ;
- `antenne_radio/config/sources.yaml` ;
- `antenne_radio/04_master_plan.md`, Conversation 2 seulement.

Tâches :
1. Audite les sources RSS/Atom activées et désactivées.
2. Audite la configuration HAL actuelle : requête, champs, filtres, limite, tri.
3. Lance les tests pertinents.
4. Lance un `make run` seulement si cela est raisonnable et utile pour vérifier les sources.
5. Inspecte `api.log` et `pipeline.log`.
6. Identifie :
   - sources à garder ;
   - sources à désactiver ;
   - sources à corriger ;
   - sources simples à ajouter seulement si elles ont un flux RSS/Atom clair ou une configuration HAL propre.

Contraintes :
- Pas de Crossref/OpenAlex ici.
- Pas de CiNii/NDL/J-STAGE ici.
- Pas de scraping.
- Ne supprime pas les sources douteuses : préfère `enabled: false`.
- Ne code pas encore de nouvelle logique.
```

## Prompt 4 — Ajustement des sources simples

```text
Objectif : appliquer seulement les corrections simples issues du Prompt 3.

Au début, lance `git status --short`, relis la mémoire matérielle et le bilan du Prompt 3.

Tâches :
1. Mets à jour `config/sources.yaml` pour corriger, désactiver ou ajouter uniquement des sources simples.
2. Mets à jour `01_RESSOURCES_SUIVIES.md` en miroir.
3. Si HAL doit être resserré, ajuste la configuration sans rendre la requête trop fragile.
4. Si une source est incertaine, ajoute-la désactivée avec une note claire.
5. Lance `make test`.
6. Si pertinent, lance `make run` et vérifie les logs.

Contraintes :
- Ne modifie pas le modèle de données.
- Ne modifie pas le scoring.
- Pas de scraping.
- Pas de connecteur nouveau.
- Ne masque pas les sources qui renvoient 0 entrée : documente leur état.
```

## Prompt 5 — QA sources + mémoire matérielle

```text
Objectif : clore le chantier sources avec une base documentée.

Au début, lance `git status --short`, relis `docs/AGENTS.md`, la mémoire matérielle, puis les bilans des Prompts 3 et 4.

Tâches :
1. Lance `make test`.
2. Lance `make run` si le Prompt 4 a modifié des sources actives.
3. Vérifie les compteurs de `db.json` si disponible.
4. Inspecte les 80 dernières lignes de `data/logs/api.log` et `data/logs/pipeline.log` si disponibles.
5. Vérifie que `01_RESSOURCES_SUIVIES.md` correspond à `config/sources.yaml`.
6. Mets à jour `antenne_radio/codex_memoire_materielle.md` avec un bilan factuel :
   - date ;
   - objectif du chantier ;
   - fichiers modifiés ;
   - commandes lancées ;
   - tests passés ou échoués ;
   - compteurs observés ;
   - sources ajoutées, corrigées, désactivées ou rejetées ;
   - limites restantes ;
   - prochain chantier recommandé.
7. Ajoute un handoff prêt à copier dans une nouvelle conversation Codex.

Contraintes :
- Ne commence pas la conversation 3.
- Ne masque aucun échec de test.
```

---

# Conversation 3 — Scoring, bruit, faux positifs, doublons non destructeurs

Nombre optimal : **3 prompts**.  
But : rendre la veille plus utile sans perdre des items intéressants.

## Prompt 6 — Audit du signal et des faux positifs

```text
Objectif : auditer la qualité du signal avant de toucher au scoring.

Avant toute action, lance `git status --short`.

Lis ensuite :
- `docs/AGENTS.md` ;
- `antenne_radio/codex_memoire_materielle.md`, en priorité les sections sur scoring, statuts, données présentes, fragilités et contrats de données ;
- `antenne_radio/config/keywords.yaml` ;
- `antenne_radio/config/scoring.yaml` ;
- `antenne_radio/scripts/core/scoring.py` ;
- les tests liés au scoring ;
- `antenne_radio/04_master_plan.md`, Conversation 3 seulement.

Tâches :
1. Analyse la distribution actuelle des statuts si `db.json` existe.
2. Identifie des exemples de bons `to_read`, de `candidate` utiles, de bruit technique et de faux positifs.
3. Vérifie comment les mots négatifs fonctionnent.
4. Repère les cas où `radio` désigne autre chose que média/radiophonie.
5. Évalue si un champ `possible_duplicate` ou équivalent est utile, sans suppression automatique.
6. Propose des ajustements précis de scoring et de tests.

Contraintes :
- Ne modifie rien dans ce prompt.
- Ne supprime aucun item.
- Ne passe pas à du fuzzy matching destructeur.
```

## Prompt 7 — Amélioration scoring + doublons prudents

```text
Objectif : améliorer le signal avec des changements petits, testés et réversibles.

Au début, lance `git status --short`, relis la mémoire matérielle, puis le bilan du Prompt 6.

Tâches :
1. Ajuste `keywords.yaml` et/ou `scoring.yaml` selon l’audit.
2. Modifie `scoring.py` seulement si la configuration ne suffit pas.
3. Ajoute des tests couvrant :
   - item SHS/radio à conserver ;
   - item podcast/radio libre à favoriser ;
   - item radiologie/radiofréquence/télécom à pénaliser ;
   - item ambigu à garder en `candidate` plutôt qu’à ignorer brutalement.
4. Si un mécanisme de doublon non destructeur est ajouté, il doit seulement marquer ou expliquer, jamais supprimer.
5. Lance `make test`.

Contraintes :
- Pas de nouvelle source.
- Pas de modification d’export public.
- Ne change pas les statuts existants de façon irréversible sans commande explicite.
```

## Prompt 8 — QA signal + mémoire matérielle

```text
Objectif : vérifier que le scoring amélioré ne casse pas la veille.

Au début, lance `git status --short`, relis `docs/AGENTS.md`, la mémoire matérielle, puis les Prompts 6 et 7.

Tâches :
1. Lance `make test`.
2. Lance `make run` si les changements de scoring nécessitent une vérification réelle.
3. Compare la distribution des statuts avant/après si possible.
4. Vérifie que les bons items connus ne tombent pas en `ignored`.
5. Vérifie que les items techniques bruyants sont mieux traités.
6. Mets à jour `antenne_radio/codex_memoire_materielle.md` avec :
   - règles ajoutées ou modifiées ;
   - exemples de bruit traité ;
   - tests ajoutés ;
   - compteurs observés ;
   - limites restantes ;
   - prochain chantier recommandé.
7. Ajoute un handoff prêt à copier dans une nouvelle conversation Codex.

Contraintes :
- Ne commence pas la conversation 4.
- Ne masque aucun test échoué.
```

---

# Conversation 4 — Export Obsidian et export Zotero manuel

Nombre optimal : **3 prompts**.  
But : rendre les sorties privées plus utiles sans automatisation intrusive.

## Prompt 9 — Audit des exports privés

```text
Objectif : auditer l’export Obsidian actuel et décider du format Zotero manuel.

Avant toute action, lance `git status --short`.

Lis ensuite :
- `docs/AGENTS.md` ;
- `antenne_radio/codex_memoire_materielle.md`, en priorité les sections export Obsidian, contrats de données et hors-périmètre Zotero automatique ;
- `antenne_radio/scripts/export/export_obsidian.py` ;
- les tests d’export ;
- `antenne_radio/README.md` ;
- `antenne_radio/04_master_plan.md`, Conversation 4 seulement.

Tâches :
1. Audite l’export Obsidian actuel : lisibilité, sections, frontmatter, abstract, score, explication, UTF-8.
2. Propose des améliorations utiles mais sobres.
3. Compare CSL-JSON et BibTeX pour un export Zotero manuel.
4. Choisis un seul format de départ, sauf raison forte.
5. Liste le mapping minimal depuis `RadioWatchItem`.
6. Ne code rien dans ce prompt.

Contraintes :
- Pas d’écriture automatique dans Zotero.
- Pas de modification d’un vrai coffre Obsidian.
- Pas de publication publique.
```

## Prompt 10 — Amélioration Obsidian + export Zotero manuel

```text
Objectif : améliorer les exports privés sans toucher aux données sources.

Au début, lance `git status --short`, relis la mémoire matérielle, puis le bilan du Prompt 9.

Tâches :
1. Améliore `export_obsidian.py` de façon sobre si nécessaire.
2. Ajoute un export Zotero manuel dans un nouveau script, par exemple `scripts/export/export_csl.py` ou `export_bibtex.py`.
3. Le script doit écrire dans `data/exports/`.
4. Il ne doit pas modifier `db.json` par défaut.
5. Il doit gérer UTF-8, DOI, URL, auteurs, titre, date, source, type approximatif.
6. Ajoute des tests.
7. Mets à jour le README si une nouvelle commande existe.
8. Lance `make test`.

Contraintes :
- Pas d’API Zotero.
- Pas de synchronisation.
- Pas d’écriture hors `antenne_radio/data/exports/`.
```

## Prompt 11 — QA exports privés + mémoire matérielle

```text
Objectif : vérifier que les exports privés sont utilisables et documentés.

Au début, lance `git status --short`, relis `docs/AGENTS.md`, la mémoire matérielle, puis les Prompts 9 et 10.

Tâches :
1. Lance `make test`.
2. Génère un export Obsidian de test.
3. Génère un export Zotero manuel de test si le script existe.
4. Vérifie UTF-8, titres japonais éventuels, DOI, URL, auteurs, dates.
5. Vérifie que `db.json` n’est pas modifié par défaut.
6. Mets à jour `antenne_radio/codex_memoire_materielle.md` avec :
   - format Zotero choisi ;
   - commande d’export ;
   - fichiers créés ;
   - tests passés/échoués ;
   - limites de mapping ;
   - prochain chantier recommandé.
7. Ajoute un handoff prêt à copier dans une nouvelle conversation Codex.

Contraintes :
- Ne commence pas la conversation 5.
- Ne masque aucun échec.
```

---

# Conversation 5 — API académique occidentale unique : Crossref ou OpenAlex

Nombre optimal : **3 prompts**.  
But : ajouter une seule complexité externe, ou documenter clairement le report.

## Prompt 12 — Audit officiel Crossref/OpenAlex

```text
Objectif : choisir entre Crossref, OpenAlex, durcissement de l’existant ou report.

Avant toute action, lance `git status --short`.

Lis ensuite :
- `docs/AGENTS.md` ;
- `antenne_radio/codex_memoire_materielle.md`, en priorité les sections sources, API non encore intégrées, contrats de données et fragilités ;
- `antenne_radio/01_RESSOURCES_SUIVIES.md` ;
- `antenne_radio/config/sources.yaml` ;
- les connecteurs existants ;
- `antenne_radio/04_master_plan.md`, Conversation 5 seulement.

Tâches :
1. Vérifie si Crossref ou OpenAlex existe déjà dans le code.
2. Consulte les documentations officielles actuelles de Crossref et OpenAlex.
3. Compare leur valeur pour le projet :
   - suivi de revues par ISSN ;
   - DOI ;
   - découverte large ;
   - topics/sources ;
   - qualité des métadonnées ;
   - conditions d’usage ;
   - rate limits ;
   - identification polie ;
   - besoin éventuel de clé/API key.
4. Choisis une seule décision :
   - ajouter Crossref ;
   - ajouter OpenAlex ;
   - durcir une intégration existante ;
   - reporter.
5. Cite dans le bilan les URLs officielles consultées.

Contraintes :
- Ne code rien.
- Si les conditions sont ambiguës, recommande le report.
- Ne traite pas les sources japonaises ici.
```

## Prompt 13 — Connecteur occidental ou report documenté

```text
Objectif : appliquer strictement la décision du Prompt 12.

Au début, lance `git status --short`, relis la mémoire matérielle, puis le bilan du Prompt 12.

Tâches si un connecteur est retenu :
1. Crée un connecteur minimal et désactivable.
2. Ajoute sa configuration dans `sources.yaml`.
3. Écris les dumps bruts dans `data/raw/`.
4. Normalise vers `RadioWatchItem` sans casser RSS/HAL.
5. Gère timeouts, 403, 429, 500 et réponses vides.
6. Implémente identification polie et limite basse si nécessaire.
7. Ajoute des tests avec mocks HTTP.
8. Lance `make test`.

Tâches si le report est retenu :
1. Documente le report dans `01_RESSOURCES_SUIVIES.md` ou un court fichier dédié.
2. Note les raisons : conditions, clé, bruit, utilité insuffisante, complexité.
3. Ajoute au besoin un placeholder désactivé, sans code mort.
4. Lance les tests pertinents.

Contraintes :
- Ne pas ajouter Crossref et OpenAlex ensemble.
- Pas de source japonaise.
- Pas de scraping.
- Pas de secret dans le dépôt.
```

## Prompt 14 — QA API occidentale + mémoire matérielle

```text
Objectif : vérifier que l’ajout ou le report est propre.

Au début, lance `git status --short`, relis `docs/AGENTS.md`, la mémoire matérielle, puis les Prompts 12 et 13.

Tâches :
1. Lance `make test`.
2. Si un connecteur a été ajouté, lance un run contrôlé si raisonnable.
3. Vérifie les logs API et pipeline.
4. Vérifie que RSS/HAL fonctionnent encore.
5. Vérifie l’idempotence et les doublons DOI/URL.
6. Vérifie que la source est désactivable par config.
7. Mets à jour `antenne_radio/codex_memoire_materielle.md` avec :
   - décision Crossref/OpenAlex ;
   - conditions d’usage retenues ;
   - fichiers modifiés ;
   - tests ;
   - compteurs observés ;
   - limites ;
   - prochain chantier recommandé.
8. Ajoute un handoff prêt à copier dans une nouvelle conversation Codex.

Contraintes :
- Ne commence pas la conversation 6.
- Ne masque aucun échec.
```

---

# Conversation 6 — Contrat public et audit légal

Nombre optimal : **3 prompts**.  
But : séparer sans ambiguïté privé/public avant toute intégration site.

## Prompt 15 — Définition whitelist/blacklist publique

```text
Objectif : définir le contrat de données publiques avant tout export public.

Avant toute action, lance `git status --short`.

Lis ensuite :
- `docs/AGENTS.md` ;
- `antenne_radio/codex_memoire_materielle.md`, en priorité contrats de données, raw, exports, sources et fragilités ;
- `antenne_radio/README.md` ;
- `antenne_radio/01_RESSOURCES_SUIVIES.md` ;
- les modèles et exports existants ;
- `antenne_radio/04_master_plan.md`, Conversation 6 seulement.

Tâches :
1. Liste les champs privés actuels.
2. Liste les champs publiables possibles.
3. Liste les champs interdits en public :
   - `raw` ;
   - logs ;
   - notes privées ;
   - abstracts non audités ;
   - données personnelles ;
   - champs de debug ;
   - chemins locaux ;
   - secrets ;
   - tout champ douteux.
4. Propose une whitelist stricte pour un futur JSON public.
5. Propose les attributions nécessaires par famille de source.
6. Ne code rien.

Contraintes :
- Ne crée pas encore l’export public.
- En cas de doute, champ interdit.
```

## Prompt 16 — Audit légal source par source

```text
Objectif : produire un audit légal/éthique minimal avant publication.

Au début, lance `git status --short`, relis la mémoire matérielle, `01_RESSOURCES_SUIVIES.md`, puis le bilan du Prompt 15.

Tâches :
1. Crée ou mets à jour `antenne_radio/LEGAL_AUDIT.md`.
2. Pour chaque famille de source active ou prévue pour publication, vérifie :
   - conditions d’usage officielles ;
   - attribution requise ;
   - droit de republier les métadonnées ;
   - droit de republier les abstracts ;
   - contraintes de rate limit ;
   - interdictions de scraping ;
   - risques.
3. Donne un verdict par source/famille :
   - publiable avec attribution ;
   - publiable partiellement ;
   - privé seulement ;
   - à reporter.
4. Les URLs officielles consultées doivent être notées dans le fichier.
5. Si l’audit ne peut pas conclure, le verdict doit être prudent.

Contraintes :
- Ne publie rien.
- Ne crée pas encore d’intégration Hugo.
- Ne considère jamais les abstracts comme publiables par défaut.
```

## Prompt 17 — QA contrat public + mémoire matérielle

```text
Objectif : clore l’audit public avant tout export.

Au début, lance `git status --short`, relis `docs/AGENTS.md`, la mémoire matérielle, puis les Prompts 15 et 16.

Tâches :
1. Vérifie `LEGAL_AUDIT.md`.
2. Vérifie que la whitelist publique exclut bien `raw`, logs, abstracts douteux et notes privées.
3. Lance `git diff --check` sur les fichiers modifiés.
4. Lance `make test` si des fichiers de code ont été touchés ; sinon explique pourquoi ce n’était pas nécessaire.
5. Mets à jour `antenne_radio/codex_memoire_materielle.md` avec :
   - verdict légal ;
   - whitelist publique ;
   - champs interdits ;
   - sources publiables ou non ;
   - limites restantes ;
   - prochain chantier recommandé.
6. Ajoute un handoff prêt à copier dans une nouvelle conversation Codex.

Contraintes :
- Ne commence pas la conversation 7.
- Si le verdict légal est défavorable, le prochain chantier doit être “export public désactivé ou privé seulement”.
```

---

# Conversation 7 — Export public et Hugo sobre

Nombre optimal : **3 prompts**.  
But : préparer la publication sans exposer de données privées. Si l’audit n’est pas favorable, cette conversation doit produire un export désactivé ou un report documenté.

## Prompt 18 — Audit d’intégration Hugo possible

```text
Objectif : décider si une intégration Hugo sobre est possible après audit légal.

Avant toute action, lance `git status --short`.

Lis ensuite :
- `docs/AGENTS.md`, surtout les garde-fous Hugo et endpoints JSON ;
- `antenne_radio/codex_memoire_materielle.md`, en priorité audit légal, whitelist publique et exports ;
- `antenne_radio/LEGAL_AUDIT.md` s’il existe ;
- `antenne_radio/README.md` ;
- les exports existants ;
- `antenne_radio/04_master_plan.md`, Conversation 7 seulement.

Tâches :
1. Vérifie le verdict légal.
2. Si le verdict est défavorable, propose un report sans intégrer Hugo.
3. Si le verdict est favorable ou partiellement favorable, propose :
   - structure du JSON public ;
   - emplacement du fichier public ;
   - emplacement Hugo éventuel ;
   - page ou partial minimal ;
   - textes d’attribution ;
   - tests anti-fuite.
4. Ne code rien dans ce prompt.

Contraintes :
- Pas d’abstracts publics sauf autorisation explicite vérifiée.
- Pas de `raw`.
- Pas de logs.
- Pas d’intégration décorative lourde.
```

## Prompt 19A — Export public expurgé et/ou intégration Hugo minimale

```text
Objectif : implémenter seulement ce que l’audit autorise.

Au début, lance `git status --short`, relis la mémoire matérielle, `LEGAL_AUDIT.md`, puis le bilan du Prompt 18.

Tâches si publication autorisée :
1. Crée un export public par whitelist stricte, par exemple `scripts/export/export_public.py`.
2. Le JSON public doit exclure `raw`, abstracts non autorisés, logs, notes privées, chemins locaux, secrets.
3. Ajoute des tests anti-fuite.
4. Ajoute une intégration Hugo sobre seulement si elle est simple.
5. Ne casse aucun endpoint JSON existant du site.
6. Mets à jour README ou documentation dédiée.
7. Lance `make test`.
8. Si Hugo est touché, lance le build Hugo recommandé dans `docs/AGENTS.md`.

Tâches si publication non autorisée :
1. Documente le report.
2. Crée au besoin une commande d’export public désactivée ou limitée, mais sans intégrer le site.
3. Ajoute des tests anti-fuite si un fichier public est produit.

Contraintes :
- Ne pas publier `raw`.
- Ne pas publier les abstracts par défaut.
- Ne pas faire de flux RSS sortant public dans cette conversation.
- Ne pas ajouter de JS lourd.
```

## Prompt 19B — Section Hugo publique minimale

```text
Objectif : créer la section publique minimale du site pour afficher les résultats de l’antenne radio.

Avant toute action, lance `git status --short`.

Lis :
- docs/AGENTS.md ;
- antenne_radio/codex_memoire_materielle.md ;
- antenne_radio/LEGAL_AUDIT.md ;
- antenne_radio/README.md ;
- l’export public généré ;
- la structure Hugo existante du site.

Tâches :
1. Vérifie que l’export public existe et ne contient aucun champ privé.
2. Crée une section Hugo sobre, par exemple `/antenne-radio/`, destinée à afficher les résultats publics.
3. Ajoute une page d’introduction courte expliquant :
   - ce qu’est l’antenne radio ;
   - la fréquence de mise à jour ;
   - les limites ;
   - les sources suivies ;
   - les critères de sélection/scoring si publiables.
4. Affiche une liste lisible des items publics :
   - titre ;
   - source ;
   - date ;
   - lien d’origine ;
   - score ou explication courte si autorisée ;
   - tags publics si disponibles.
5. N’affiche aucun abstract sauf autorisation explicitement validée.
6. N’affiche jamais `raw`, logs, notes privées, chemins locaux ou métadonnées internes.
7. Ajoute un lien discret depuis la navigation ou une page existante, sans bouleverser le site.
8. Prévois un état vide ou un message si l’export public n’existe pas.
9. Lance les tests anti-fuite.
10. Lance le build Hugo recommandé dans `docs/AGENTS.md`.
11. Mets à jour la mémoire matérielle avec :
   - URL/chemin de la section ;
   - fichiers Hugo créés ou modifiés ;
   - champs affichés ;
   - tests lancés ;
   - limites restantes.

Contraintes :
- Section sobre, sans JS lourd.
- Pas de RSS public sortant.
- Pas de publication d’abstracts par défaut.
- Ne pas casser les endpoints JSON existants.
```

## Prompt 20 — QA publication/Hugo + mémoire matérielle

```text
Objectif : vérifier l’absence de fuite et clore le chantier public.

Au début, lance `git status --short`, relis `docs/AGENTS.md`, la mémoire matérielle, `LEGAL_AUDIT.md`, puis les Prompts 18 et 19.

Tâches :
1. Lance `make test`.
2. Lance les tests anti-fuite.
3. Si Hugo a été touché, lance le build Hugo recommandé dans `docs/AGENTS.md`.
4. Inspecte le JSON public généré.
5. Vérifie explicitement l’absence de :
   - `raw` ;
   - logs ;
   - abstracts interdits ;
   - notes privées ;
   - chemins locaux ;
   - secrets.
6. Vérifie les textes d’attribution.
7. Mets à jour `antenne_radio/codex_memoire_materielle.md` avec :
   - verdict d’intégration ;
   - fichiers publics générés ;
   - champs publiés ;
   - tests ;
   - build Hugo si lancé ;
   - limites restantes ;
   - prochain chantier recommandé.
8. Ajoute un handoff prêt à copier dans une nouvelle conversation Codex.

Contraintes :
- Ne commence pas la conversation 8.
- Ne masque aucun échec.
```

---

# Conversation 8 — GitHub Actions manuelle

Nombre optimal : **3 prompts**.  
But : rendre le pipeline reproductible à la demande, sans cron et sans auto-commit.

## Prompt 21 — Audit CI possible

```text
Objectif : vérifier si une GitHub Action manuelle est sûre et utile.

Avant toute action, lance `git status --short`.

Lis ensuite :
- `docs/AGENTS.md` ;
- `antenne_radio/codex_memoire_materielle.md`, en priorité pipeline, exports, données privées, publication, limites et dernier état ;
- `antenne_radio/README.md` ;
- `antenne_radio/LEGAL_AUDIT.md` si le fichier existe ;
- `.github/workflows/` si le dossier existe ;
- `antenne_radio/04_master_plan.md`, Conversation 8 seulement.

Tâches :
1. Vérifie s’il existe déjà une Action liée à l’antenne.
2. Identifie les risques :
   - données privées dans artefacts ;
   - secrets ;
   - logs trop bavards ;
   - dépendances réseau ;
   - versions Python ;
   - divergence local/CI ;
   - auto-commit accidentel.
3. Propose une Action `workflow_dispatch` minimale :
   - installation ;
   - tests ;
   - pipeline optionnel ou run limité ;
   - artefacts contrôlés ou aucun artefact.
4. Ne code rien dans ce prompt.

Contraintes :
- Pas de cron.
- Pas d’auto-commit.
- Pas de push automatique.
- Pas de publication.
```

## Prompt 22 — Workflow manuel contrôlé

```text
Objectif : créer une GitHub Action manuelle minimale et prudente.

Au début, lance `git status --short`, relis la mémoire matérielle, puis le bilan du Prompt 21.

Tâches :
1. Crée ou modifie un workflow sous `.github/workflows/`.
2. Le workflow doit être déclenché par `workflow_dispatch`.
3. Il doit lancer les tests de `antenne_radio/`.
4. Il peut lancer le pipeline seulement si les risques sont maîtrisés.
5. Les artefacts doivent être absents ou strictement contrôlés.
6. Aucune donnée privée ne doit être exposée.
7. Pas de cron.
8. Pas d’auto-commit.
9. Mets à jour README ou documentation si nécessaire.
10. Lance les validations locales possibles.

Contraintes :
- Ne pas inclure de secret en clair.
- Ne pas committer ou pousser automatiquement.
- Ne pas publier sur le site.
```

## Prompt 23 — QA CI + mémoire matérielle

```text
Objectif : vérifier le workflow manuel et documenter ses limites.

Au début, lance `git status --short`, relis `docs/AGENTS.md`, la mémoire matérielle, puis les Prompts 21 et 22.

Tâches :
1. Vérifie le YAML.
2. Lance `make test`.
3. Vérifie que le workflow ne contient pas :
   - cron ;
   - auto-commit ;
   - push automatique ;
   - publication ;
   - secrets en clair ;
   - artefacts privés.
4. Si possible, explique comment déclencher manuellement l’Action.
5. Mets à jour `antenne_radio/codex_memoire_materielle.md` avec :
   - nom du workflow ;
   - déclencheur ;
   - commandes lancées ;
   - politique d’artefacts ;
   - tests ;
   - limites ;
   - prochain chantier recommandé.
6. Ajoute un handoff prêt à copier dans une nouvelle conversation Codex.

Contraintes :
- Ne commence pas la conversation 9.
- Ne masque aucun échec.
```

---

# Conversation 9 — Release candidate v1

Nombre optimal : **2 prompts**.  
But : obtenir un verdict v1 net, pas ouvrir une nouvelle phase infinie.

## Prompt 24 — Audit release candidate v1

```text
Objectif : auditer l’antenne comme release candidate v1.

Avant toute action, lance `git status --short`.

Lis ensuite :
- `docs/AGENTS.md` ;
- `antenne_radio/codex_memoire_materielle.md`, en entier si possible ;
- `antenne_radio/README.md` ;
- `antenne_radio/01_RESSOURCES_SUIVIES.md` ;
- `antenne_radio/V1_SCOPE.md` si le fichier existe ;
- `antenne_radio/LEGAL_AUDIT.md` si le fichier existe ;
- `antenne_radio/04_master_plan.md`, Conversation 9 et critères v1.

Tâches :
1. Lance `make test` depuis `antenne_radio/`.
2. Lance `make run` si cela est raisonnable pour valider le pipeline réel.
3. Vérifie les logs.
4. Vérifie les compteurs `db.json`.
5. Vérifie les exports privés.
6. Vérifie l’export public si présent.
7. Vérifie l’intégration Hugo si présente.
8. Vérifie la GitHub Action si présente.
9. Compare l’état réel aux critères v1.
10. Liste :
   - bloquants v1 ;
   - corrections mineures ;
   - reports assumés ;
   - bonus non nécessaires.

Contraintes :
- Ne modifie rien dans ce prompt.
- Ne transforme pas l’audit final en nouveau plan v2.
```

## Prompt 25 — Corrections finales + verdict v1 + mémoire matérielle

```text
Objectif : appliquer seulement les corrections finales nécessaires et donner un verdict v1.

Au début, lance `git status --short`, relis la mémoire matérielle, puis le bilan du Prompt 24.

Tâches :
1. Corrige uniquement les petits bloquants clairement identifiés.
2. Ne lance aucune refonte.
3. Mets à jour README, `01_RESSOURCES_SUIVIES.md`, `LEGAL_AUDIT.md` ou `V1_SCOPE.md` si nécessaire.
4. Lance `make test`.
5. Lance `make run` si une correction touche au pipeline.
6. Si Hugo est touché, lance le build recommandé dans `docs/AGENTS.md`.
7. Mets à jour `antenne_radio/codex_memoire_materielle.md` avec un bilan v1 final :
   - date ;
   - état Git ;
   - fichiers modifiés ;
   - commandes ;
   - tests ;
   - compteurs ;
   - sources actives ;
   - exports disponibles ;
   - statut légal/publication ;
   - statut CI ;
   - limites assumées ;
   - bonus reportés.
8. Ajoute un handoff final prêt à copier.
9. Donne un verdict explicite :
   - `v1 validée` ;
   - `v1 validée sauf publication publique` ;
   - `v1 non validée : bloquants restants`.

Contraintes :
- Ne masque aucun échec.
- Ne crée pas de nouvelle conversation/phase dans le verdict.
- Les gros sujets doivent rester en bonus reportés.
```

---

## 7. Critères de réussite v1

La v1 est réussie si :

- `make test` passe ;
- le pipeline local reste compréhensible et relançable ;
- RSS/HAL fonctionnent ou leurs limites sont documentées ;
- le scoring produit des explications utiles ;
- les faux positifs majeurs sont traités sans faux négatifs dangereux ;
- l’export Obsidian est exploitable ;
- l’export Zotero manuel existe ou son report est justifié ;
- l’API occidentale unique existe ou son report est justifié ;
- `01_RESSOURCES_SUIVIES.md` est à jour ;
- `codex_memoire_materielle.md` permet une reprise claire ;
- `LEGAL_AUDIT.md` existe avant toute publication ;
- aucun champ privé n’est exposé publiquement ;
- l’intégration Hugo, si présente, est sobre et testée ;
- la GitHub Action, si présente, est manuelle ;
- les bonus difficiles sont explicitement reportés.

## 8. Critères d’arrêt

Arrêter un chantier et documenter plutôt que forcer si :

- les tests échouent sans cause claire ;
- une API exige une clé ou des conditions non résolues ;
- une source interdit l’usage envisagé ;
- une publication risquerait d’exposer `raw`, abstracts sous droits ou logs ;
- une conversation commence à toucher trop de zones à la fois ;
- un connecteur devient plus gros que prévu ;
- le plan glisse vers cron, auto-commit, scraping ou LLM sans décision explicite.

## 9. Bonus reportables après v1

À transformer plus tard en cartouches autonomes :

1. **CiNii**  
   Audit officiel, appid, connecteur désactivable, attribution.

2. **NDL Search**  
   Audit SRU/OpenSearch, attribution, séparation stricte entre métadonnées publiques et contenus sous droits.

3. **J-STAGE**  
   WebAPI officielle, XML, conditions, pas de scraping.

4. **changedetection.io**  
   Seulement pour pages sans flux/API, via flux Atom/RSS généré, jamais scraping sauvage interne.

5. **Cron automatique**  
   Après stabilité de l’Action manuelle, avec politique d’artefacts claire.

6. **Flux RSS sortant public**  
   Après audit légal et export public stable.

7. **Résumé LLM**  
   Plus tard, éventuellement local/manuel, sans republier d’abstract sous droits.

8. **Interface de curation**  
   Plus tard, seulement si le fichier plat devient trop pénible à gérer.

## 10. Message minimal pour ouvrir une nouvelle conversation Codex

```text
On travaille sur `antenne_radio/`, antenne locale de veille en études radiophoniques.

Lis d’abord :
- `docs/AGENTS.md`
- `antenne_radio/codex_memoire_materielle.md`
- `antenne_radio/04_master_plan.md`
- puis seulement les fichiers liés à la conversation en cours.

Ne refais pas la v0.1 : elle est considérée comme stable.
Le but est d’avancer vers la v1 en suivant `04_master_plan.md`.
Commence toujours par `git status --short`.
À la fin de la conversation, mets à jour `codex_memoire_materielle.md` avec un bilan factuel et un handoff.
```

# V1_SCOPE - antenne radio

Dernier gel : 2026-05-19 JST.

Ce fichier fixe le périmètre court de la v1 à partir de l'audit réel de reprise.
Il ne remplace ni `04_master_plan.md` ni `codex_memoire_materielle.md`.

## Inclus dans la v1

- Préserver la v0.1 stable : RSS/Atom, HAL, normalisation `RadioWatchItem`, scoring lexical, export Obsidian, pipeline local et tests.
- Améliorer la couverture RSS/HAL existante et tenir `RESSOURCES_SUIVIES.md` à jour.
- Réduire le bruit du scoring avec des cas négatifs explicites, sans supprimer automatiquement les `ignored`.
- Ajouter un dédoublonnage plus utile mais non destructeur.
- Rendre l'export Obsidian plus lisible.
- Ajouter un export Zotero manuel, probablement CSL-JSON ou BibTeX, sans écriture automatique dans Zotero.
- Auditer Crossref et OpenAlex, puis ajouter au plus un connecteur académique occidental si l'intérêt est clair.
- Définir un contrat public par whitelist et réaliser un audit légal source par source avant tout export public.
- Préparer une intégration Hugo sobre seulement si l'audit légal la rend acceptable.
- Tester une GitHub Action manuelle `workflow_dispatch`, sans cron par défaut et sans auto-commit.
- Maintenir une mémoire de reprise courte et factuelle après chaque bloc.

## Reporté explicitement

- CiNii, NDL Search, J-STAGE.
- `changedetection.io` et surveillance de pages sans flux/API.
- Scraping HTML.
- Flux RSS sortant public.
- Cron automatique.
- Auto-commit.
- Écriture automatique dans Zotero ou dans un coffre Obsidian réel.
- Résumés ou traitements LLM.
- Service serveur permanent.
- Interface d'administration.

## Critères de réussite v1

- `make test` passe depuis `antenne_radio/`.
- Le pipeline local reste fonctionnel et documenté.
- Les compteurs de `data/normalized/db.json` sont lisibles et les logs sont inspectables.
- Les exports privés Obsidian et Zotero manuel sont utiles sans publier de données privées.
- Le bruit RSS/HAL est mieux contrôlé par configuration, scoring et dédoublonnage prudent.
- Aucun `raw`, log, note privée, abstract sous droits ou donnée non auditée n'est publié.
- L'export public et Hugo sont soit validés par l'audit légal, soit explicitement désactivés.
- L'automatisation éventuelle reste manuelle, contrôlée et sans commit automatique.

## Critères d'arrêt

- Ambiguïté légale non résolue sur les données à publier.
- Tests rouges non compris.
- Dérive vers scraping, cron, auto-commit, LLM ou service permanent.
- Tentative d'ajouter plusieurs connecteurs complexes dans un même bloc.
- Perte du champ `raw`, modification destructrice des `ignored` ou écrasement non voulu d'items existants.
- Pipeline qui réussit formellement mais dont les compteurs/logs montrent des données vides ou incohérentes.

## Conversations restantes

1. Conversation 2 : sources RSS/HAL et documentation des sources.
2. Conversation 3 : scoring, bruit, faux positifs, doublons non destructeurs.
3. Conversation 4 : export Obsidian et export Zotero manuel.
4. Conversation 5 : API académique occidentale unique, Crossref ou OpenAlex.
5. Conversation 6 : contrat public et audit légal.
6. Conversation 7 : export public et Hugo sobre.
7. Conversation 8 : GitHub Actions manuelle.
8. Conversation 9 : release candidate v1.

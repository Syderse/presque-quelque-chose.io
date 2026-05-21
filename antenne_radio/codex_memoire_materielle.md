# Mémoire matérielle - antenne radio

## Reprise rapide & État du pipeline v2
- **Démarrage rapide** : Lancer `git status --short`, lire `docs/AGENTS.md` et `antenne_radio/README.md`.
- **Architecture & Local** : Le sous-projet vit exclusivement dans `antenne_radio/` avec son `.venv` et ses dépendances. Pas de cron, pas d'auto-commit, pas de LLM.
- **Pipeline opérationnel** : Ingestion RSS/Atom (10 sources actives) + HAL (requête ciblée resserrée) + Crossref contrôlé (1 revue, `rows: 20`, `CROSSREF_MAILTO` local obligatoire) -> Normalisation `RadioWatchItem` dédupliquée dans `data/normalized/db.json` (289 items) -> Scoring lexical (poids positifs, négatifs `-6` et techniques `-2`) -> Exports privés (Obsidian hebdomadaire, Zotero CSL JSON) et Export public (`static/antenne-radio/index.json`, 233 items whitelistés).
- **Intégration Hugo** : Page `/antenne-radio/` lisant le JSON public au build-time (avec fallback `<noscript>` de 50 cartes) et l'hydratant via JS Vanilla dynamique en mémoire (recherche, filtres ET multi-critères, deep-linking, chargement progressif par 50).

## Contrats de données & Sécurité
- **db.json** : Doit rester valide, UTF-8 non échappé, trié par clés. Déduplication par ID stable (DOI > URL > Title/Date). Jamais de suppression automatique des `ignored`.
- **Confidentialité absolue (Anti-fuite)** : Interdiction stricte de publier abstracts, raw dumps, logs, scores, explications, mots-clés internes, auteurs, tags ou chemins locaux. Seul le JSON whitelisté est public.
- **Crossref** : Connecteur activé durablement avec garde-fou (`enabled: true`). Sans `CROSSREF_MAILTO` local, il ne fait aucun appel réseau. Les revues ciblées prioritaires (`radio_journal`, `sound_studies_journal`, `resonance_journal`) sont désormais actives et interrogées à `rows: 20` par revue.
- **OpenAlex** : Connecteur pleinement actif (`openalex.enabled: true`). `OPENALEX_MAILTO` local obligatoire avant tout appel réseau. La venue ciblée (`journal_sonic_studies_venue`, ISSN `2212-6252`) est désormais active en production. Aucun abstract reconstruit, score de pertinence strictement privé.

---

## Synthèse historique de la construction (v0.1 & v1)
- **18 mai 2026 (v0.1)** : Initialisation du squelette Pydantic, configuration déclarative YAML (sources, scoring, keywords), création des connecteurs bruts RSS/Atom (`feedparser`) et HAL (`httpx`), normalisation dédupliquée de `db.json`, scoring lexical avec explications explicites, export Obsidian privé, et orchestration globale par `pipeline.py` (Makefile local validé avec 41 tests unitaires).
- **19 mai 2026 (v1 & audits)** : Gel du périmètre v1 stable et production de l'audit juridique (`LEGAL_AUDIT.md`). Ajustement des sources (désactivation de Transom suite à statut 301, resserrement de la requête HAL contre le bruit). Affinage du scoring avec pénalisation douce des faux positifs techniques (`technical_radio_noise: -2`). Implémentation d'un export privé Zotero au format stable CSL JSON. Création du pipeline d'exportation publique avec whitelist stricte anti-fuite (`id`, `title`, `url`, `doi`, `published_at`, `source_name`, `source_type`, `language`, `source_family`, `attribution_id`) et intégration de la première version de la section Hugo `/antenne-radio/`. Scission formelle de la roadmap en V2 (ergonomie et UX) et V3 (académique et connecteurs complexes).

---

## 2026-05-20 - Prompt 1 v2 audit réel et CI manuelle
- **Objectif** : Mettre en place une CI manuelle sans déclenchement automatique et clarifier la documentation utilisateur.
- **Workflow CI (`.github/workflows/tests.yml`)** : Nommé `Antenne Radio Tests`, déclenchement exclusif par `workflow_dispatch` (manuel). Configure Python 3.12, utilise le cache pip sur `antenne_radio/requirements.txt`, installe les dépendances et lance `make test` dans `antenne_radio/`. Permissions limitées à `contents: read`.
- **README.md** : Réécriture complète pour servir de guide débutant d'installation locale, de routine hebdomadaire manuelle, d'utilisation de la CI, d'explication des exports privés et de l'index public.
- **Validation** : Syntaxe YAML validée, `make test` passe avec 72 tests (Python 3.14.5 / pytest 9.0.3).

## 2026-05-20 - Prompt 2 v2 navigation Hugo antenne radio
- **Objectif** : Rendre la section `/antenne-radio/` visible dans la navigation desktop et mobile sans altérer le pipeline ou régénérer les données.
- **Menu Hugo (`config/_default/hugo.yaml`)** : Ajout de l'entrée `antenne radio` dans `menus.main` (`url: /antenne-radio/`, `weight: 35`), idéalement positionnée.
- **Intégration d'icônes (`layouts/partials/sidebar.html` et `mobile-nav.html`)** : Ajout d'une icône signal/antenne SVG personnalisée pour `antenne radio` et icône explicite pour `patafoin` (évitant le fallback).
- **Responsive** : Adaptation mobile pour afficher la nouvelle entrée de menu sur une seule ligne centrée et lisible.
- **Validation** : Build Hugo complet réussi avec Hugo 0.160.1 (83 pages). Rendu et liens fonctionnels testés sur desktop et mobile.

## 2026-05-20 - Prompt 5 v2 intégration RSS simples auditées
- **Objectif** : Activer les sources RSS validées par l'audit légal et mettre à jour le pipeline tout en préservant le contrat de non-divulgation des données privées.
- **Sources activées (`config/sources.yaml`)** : Radiomorphoses, Radio Fañch, Les Radios Libres, La Radio du Futur, La Lettre Pro de la Radio, MeCCSA Radio & Audio Studies, Nieman Storyboard (en plus de Radio Survivor, Journal of Radio & Audio Media, Sounding Out!).
- **Sources reportées / inactives** : Transom désactivé (`enabled: false`) car il retourne un statut 301 et 0 entrée.
- **Attributions publiques (`scripts/export/export_public.py`)** : Extension de la table d'attributions et de correspondance pour inclure proprement les nouvelles sources sans modifier la whitelist publique stricte.
- **Compteurs de run réel** :
  - **Dumps/DB** : Pipeline complet OK. La base `db.json` passe à 282 items (`to_read=140`, `candidate=86`, `ignored=56`).
  - **Export public** : 226 items whitelistés générés dans `static/antenne-radio/index.json`.
- **Validation** : `make test` passe avec 81 tests. Tests spécifiques ajoutés pour valider la configuration et les attributions du `LEGAL_AUDIT`.

## 2026-05-20 - Prompt 6 v2 refonte template Hugo no-JS
- **Objectif** : Remplacer l'affichage en tableau de `/antenne-radio/` par une grille de cartes néo-brutalistes avec filtrage JS fluide et un fallback statique accessible.
- **Template (`layouts/antenne-radio/list.html`)** : Lecture du JSON public whitelisted au build-time via Hugo (`transform.Unmarshal`). Affiche les compteurs, la date de génération et les attributions éthiques.
- **Fallback sans JavaScript** : Balise `<noscript>` affichant statiquement les 50 premiers items de la veille pour les navigateurs n'exécutant pas JS.
- **Design & CSS (Catppuccin Mocha)** : Grille responsive de cartes néo-brutalistes (bordures épaisses, ombres franches, contrastes visibles par défaut). Performance visuelle ciblée à 60fps avec transitions strictement limitées à `transform` et `box-shadow` (pas de `transition: all`, `will-change` ou effets lourds de flou).
- **Validation** : Build Hugo OK (83 pages). Fallback no-JS et réactivité mobile testés (viewport 390x844 sans débordement horizontal).

## 2026-05-20 - Prompt 7 v2 JS vanilla filtres et rendu progressif
- **Objectif** : Extraire le moteur JS de la page dans un asset autonome et optimisé, gérant un filtrage multi-critère en mémoire et un rendu progressif.
- **Architecture Script (`assets/js/antenne-radio.js`)** : Vanilla JS moderne de 7,6 Ko (4,4 Ko minifié), chargé de manière isolée via `js-loader.html` uniquement sur cette page. Charge dynamiquement `/antenne-radio/index.json` côté client.
- **Filtrage en mémoire** : Logique ET stricte combinant la recherche textuelle (titre/source) et les filtres de catégorie (source_type), de source (source_name) et de langue (language).
- **Pagination & Rendu** : Rendu initial de 50 cartes, avec un bouton "Afficher plus" pour charger les tranches suivantes par lots de 50 (évitant le scroll infini ou les `IntersectionObserver`).
- **Validation** : Le HTML final ne contient plus de JSON embarqué. Combinaisons complexes de recherche et filtres validées (ex. 16 items correspondants pour une recherche spécifique filtrée par langue/type).

## 2026-05-20 - Prompt 8 v2 Partage de filtres (Deep-linking) et polish UX
- **Objectif** : Synchroniser les filtres avec l'URL pour permettre le partage de vues, ajouter des badges de filtres actifs interactifs et soigner l'accessibilité.
- **Deep-linking** : Synchronisation bidirectionnelle utilisant `history.replaceState` pour ne pas polluer l'historique de navigation. Paramètres d'URL whitelistés : `q`, `cat`, `src`, `lang`. Les paramètres vides sont nettoyés et ceux non reconnus sont ignorés.
- **Barre de filtres actifs (`#active-filters-bar`)** : Rendu dynamique de badges de filtres actifs avec boutons de suppression individuels accessibles (équipés d'icônes SVG décoratives avec `aria-hidden` et de `aria-label` descriptifs). Restauration du focus clavier sur le contrôle associé lors de la suppression d'un badge.
- **État vide & Accessibilité** : Interface d'état vide ultra-légère (sans skeleton ni ressources tierces) avec un bouton de réinitialisation complète ramenant le focus sur la recherche.
- **Validation** : Build Hugo complet réussi. `make test` valide à 100% (81 tests unitaires).

## 2026-05-20 - Prompt 9 v2 Recette finale, validation et handoff de la v2
- **Objectif** : Exécuter la recette finale de la V2 stable, garantir l'étanchéité des données sensibles et planifier le passage à la V3.
- **Compteurs de production** :
  - **Base consolidée (`db.json`)** : 283 items (`to_read=141`, `candidate=86`, `ignored=56`).
  - **Index public (`static/antenne-radio/index.json`)** : 227 items whitelistés sous format `antenne-radio-public-v0`.
- **Garantie d'absence de fuites** : Scan complet du JSON et du HTML généré validant l'absence de champs sensibles (`raw`, `abstract`, logs, secrets, scores, auteurs, tags, etc.) ou de chemins locaux. Les quelques occurrences trouvées sont des faux positifs validés.
- **Handoff & Transition V3** : Le projet local V2 est gelé et stable (81 tests unitaires OK). Le prochain chantier majeur est la V3 académique, documentée dans `06_plan_v3_academique.md` (activation et déduplication DOI Crossref, connecteur OpenAlex avec score de pertinence privé, et intégration des venues/réseaux prioritaires). Les moissonnages DOAJ, Persée, CAIRN ou OpenEdition OPML sont explicitement reportés hors V3.

---

## 2026-05-20 - Conversation 1 - Crossref propre, DOI et anti-fuite (Prompt 1.1)
- **Objectif** : Auditer l'état actuel de Crossref dans le dépôt avant toute activation durable.
- **Fichiers lus et inspectés** :
  - `antenne_radio/config/sources.yaml`
  - `antenne_radio/scripts/ingest/ingest_crossref.py`
  - `antenne_radio/scripts/core/normalize.py`
  - `antenne_radio/scripts/core/models.py`
  - `antenne_radio/tests/test_ingest_crossref.py`
  - `antenne_radio/tests/test_normalize.py`
  - `antenne_radio/LEGAL_AUDIT.md`
  - `antenne_radio/01_RESSOURCES_SUIVIES.md`
- **Commandes lancées** :
  - `git status --short` : vérification de l'état du dépôt (worktree propre).
  - `make test` : exécution de la suite de tests (81 tests validés à 100% avec succès).
  - Vérification par script python de l'intégrité et du nombre d'items de `db.json` (283 items) et `static/antenne-radio/index.json` (227 items).
- **Résultats réels** :
  - **Crossref inactif par défaut** : configuré à `enabled: false` dans `sources.yaml`.
  - **Sécurité et anti-fuite** : `CROSSREF_MAILTO` est chargé dynamiquement depuis les variables d'environnement (`mailto_env: "CROSSREF_MAILTO"`), garantissant qu'aucun e-mail personnel ou secret n'est écrit dans le dépôt. Le pipeline lève proprement une erreur de type `missing_mailto` et s'arrête sans appel réseau si la variable est absente.
  - **Sobriété et politesse** : limite `rows: 20` et `polite_delay_seconds: 1` bien configurés et respectés dans `ingest_crossref.py`.
  - **Doctrine abstract & anti-fuite** : les abstracts peuvent être conservés en privé dans `db.json` et le dump brut local, mais `export_public.py` possède un filtre strict d'allowlist et un scan récursif d'interdiction qui empêche tout abstract ou donnée privée d'entrer dans `index.json` public.
  - **Documentation** : Entièrement à jour et cohérente dans `README.md`, `LEGAL_AUDIT.md` et `01_RESSOURCES_SUIVIES.md`.
- **Limites restantes & Bloquants** :
  - Crossref n'est pas encore activé en live (c'est le but de la conversation V3).
  - La déduplication des DOI (notamment le fait de dédupliquer des doublons issus de HAL et Crossref sur un même DOI) et l'activation durable ne sont pas encore effectives.
- **Prochaine étape recommandée** :
  - Procéder au point **1.2 Déduplication DOI robuste** de la roadmap V3 (dans `06_plan_v3_academique.md`) : s'assurer que si un article est ingéré via HAL et via Crossref avec le même DOI normalisé, la fusion dans `db.json` se passe proprement sans créer de doublon.

---

## 2026-05-20 - Conversation 1 - Déduplication DOI inter-sources (Prompt 1.2)
- **Objectif** : Renforcer la déduplication avant toute activation durable de Crossref, sans ingestion live, sans cron, sans commit automatique et sans élargir l'export public.
- **Fichiers modifiés** :
  - `antenne_radio/scripts/core/models.py`
  - `antenne_radio/scripts/core/normalize.py`
  - `antenne_radio/tests/test_models.py`
  - `antenne_radio/tests/test_normalize.py`
  - `antenne_radio/tests/test_export_public.py`
  - `antenne_radio/codex_memoire_materielle.md`
- **Commandes lancées** :
  - `git status --short` : worktree déjà modifié au départ sur `antenne_radio/codex_memoire_materielle.md` avec le handoff du Prompt 1.1.
  - Lecture de `docs/AGENTS.md`, `antenne_radio/README.md` et `antenne_radio/codex_memoire_materielle.md`.
  - `rg --files antenne_radio` et recherches ciblées sur `normalize_doi`, `generate_stable_id`, `merge_items_without_duplicates`.
  - `make test` depuis `antenne_radio` : premier passage à 91/92, révélant une extraction DOI trop large sur URL sans DOI ; correction immédiate.
  - `make test` depuis `antenne_radio` : 92 tests passent.
  - `git diff --check` : aucune erreur whitespace.
- **Résultats réels** :
  - `normalize_doi` accepte maintenant les variantes `doi:`, `https://doi.org/...`, casse mixte, et les URL éditeur contenant un DOI, notamment `tandfonline.com/doi/full/...`, tout en rejetant les URL ordinaires sans DOI.
  - `generate_stable_id` peut dériver un DOI depuis l'URL quand aucun champ DOI explicite n'est fourni, ce qui aligne les notices RSS éditeur et Crossref sur une identité stable commune.
  - `normalize_rss_entry` renseigne désormais `doi` quand un DOI est disponible dans le flux ou dans l'URL.
  - `merge_items_without_duplicates` ne dépend plus seulement de l'ID exact : il indexe les notices par ID, DOI normalisé, URL normalisée, puis titre normalisé + date si DOI et URL sont absents.
  - En cas de doublon, le merge conserve l'ID et le statut de la notice déjà présente, donc ne remplace pas `to_read`, `ignored` ou `exported`; il complète seulement les métadonnées privées utiles (`doi`, auteurs, tags, abstract privé, trace privée de source fusionnée).
  - L'export public reste strictement whitelisté : aucun champ nouveau, aucune fuite de `raw`, `abstract`, auteurs, tags, score, logs ou métadonnées de fusion.
- **Couverture de tests ajoutée** :
  - HAL + Crossref avec même DOI.
  - RSS Taylor & Francis + Crossref avec DOI équivalent via URL éditeur.
  - Variations de casse et de préfixe DOI.
  - Conservation des statuts humains `to_read`, `ignored`, `exported`.
  - Déduplication de secours par titre normalisé + date.
  - Export public inchangé malgré métadonnées privées fusionnées.
- **Limites restantes** :
  - Aucune ingestion live Crossref n'a été lancée dans cette conversation.
  - `db.json` et `static/antenne-radio/index.json` n'ont pas été régénérés.
  - L'extraction DOI depuis URL éditeur est couverte pour le cas Taylor & Francis ; d'autres éditeurs pourront mériter des fixtures spécifiques au moment de leur activation.
- **Prochaine étape recommandée** :
  - Conversation fraîche Prompt 1.3 : activation Crossref ponctuelle et contrôlée avec `CROSSREF_MAILTO` local, volume bas, vérification des compteurs `db.json`/export public, et scan anti-fuite avant toute décision de rendre Crossref durable.

---

## 2026-05-20 - Conversation 1 - Activation Crossref contrôlée et recette anti-fuite (Prompt 1.3)
- **Mode d'activation retenu** : activation durable conditionnelle. `crossref.enabled: true`, mais aucun appel réseau Crossref n'est possible sans `CROSSREF_MAILTO` local. `make run` charge désormais `../.env.local` puis `./.env.local` si disponibles, sans écrire de secret dans le dépôt.
- **Fichiers modifiés** :
  - `antenne_radio/Makefile`
  - `antenne_radio/config/sources.yaml`
  - `antenne_radio/scripts/ingest/ingest_crossref.py`
  - `antenne_radio/tests/test_config.py`
  - `antenne_radio/tests/test_ingest_crossref.py`
  - `antenne_radio/README.md`
  - `antenne_radio/01_RESSOURCES_SUIVIES.md`
  - `antenne_radio/LEGAL_AUDIT.md`
  - `antenne_radio/codex_memoire_materielle.md`
  - `static/antenne-radio/index.json`
- **Commandes lancées** :
  - `git status --short`
  - Lecture de `docs/AGENTS.md`, `antenne_radio/README.md`, `antenne_radio/codex_memoire_materielle.md`, `config/sources.yaml`, `scripts/ingest/ingest_crossref.py`, `LEGAL_AUDIT.md`, `01_RESSOURCES_SUIVIES.md`.
  - Vérification locale de présence de `CROSSREF_MAILTO` sans afficher sa valeur : variable d'abord absente.
  - `make test` : 92 tests OK.
  - `.venv/bin/python scripts/ingest/ingest_crossref.py` sans mailto : 0 item, erreur propre `missing_mailto`, 0 appel réseau.
  - `make export-public` puis `pnpm run build` avant live : export OK, build Hugo OK.
  - `make run` avec `CROSSREF_MAILTO` local : premier passage sandbox en échec DNS, puis relance réseau autorisée OK.
  - `make export-public` après live : 233 items publics.
  - `pnpm run build` après live : build Hugo OK (83 pages).
- **Résultats Crossref réels** :
  - `data/raw/crossref_latest.json` : `result_count=20`, `rows=20`, `journal_count=1`, `raw_response_count=1`, `errors=[]`.
  - Revue interrogée : `Journal of Radio & Audio Media`, ISSN primaire `1937-6529`, `total_results=623`.
  - Le connecteur n'écrit pas la valeur du mailto dans le dump ; les erreurs HTTP futures redacteront `mailto=<redacted>` dans les logs et les payloads d'erreur.
- **Compteurs DB et déduplication** :
  - `data/normalized/db.json` : 289 items (`to_read=144`, `candidate=89`, `ignored=56`).
  - 20 notices Crossref fusionnées par DOI avec les notices T&F/RSS existantes ; 16 sont publiables par statut (`to_read` ou `candidate`), 4 restent `ignored`.
  - 0 doublon DOI détecté dans `db.json`.
- **Export public et build** :
  - `static/antenne-radio/index.json` : 233 items, schéma `antenne-radio-public-v0`, 11 sources publiques.
  - Clés publiques par item inchangées : `id`, `title`, `url`, `doi`, `published_at`, `source_name`, `source_type`, `language`, `source_family`, `attribution_id`.
  - `public/antenne-radio/index.xml` reste absent.
- **Scan anti-fuite** :
  - Scan récursif JSON des clés interdites : `[]`.
  - `rg` sur `static/antenne-radio/index.json`, `public/antenne-radio/index.json` et `public/antenne-radio/index.html` : aucune clé `abstract`, `raw`, `score`, `score_explanation`, `keywords_matched`, `negative_keywords_matched`, `authors`, `tags`, `relevance_score`, `source_api`, `source_feed`, `raw_responses`, `logs`, `status`.
  - Scan secrets/chemins : aucune occurrence de chemin local, `CROSSREF_MAILTO`, mailto, adresse email, token, bearer ou clé API dans les artefacts publics.
  - Seul faux positif HTML : le mot `tags` dans le lien de navigation global `/tags/`, hors données Antenne.
- **Limites restantes** :
  - `api.log` contient encore des lignes anciennes de tests/sandbox antérieures à la redaction ; les tests ont été corrigés pour ne plus écrire dans le vrai log.
  - Crossref est validé sur une seule famille de revue ; ne pas élargir sans nouvelle recette limitée et scan anti-fuite.
- **Prochaine étape recommandée** :
  - Conversation fraîche Prompt 1.4 : audit du bruit et de la pertinence des 20 notices Crossref fusionnées, ajustement éventuel du scoring privé ou de la requête Crossref, sans élargir encore à OpenAlex.

---

## 2026-05-21 - Conversation 2 - Audit OpenAlex et design des requêtes (Prompt 2.1)
- **Objectif** : Concevoir l'intégration OpenAlex avant ingestor live, en gardant OpenAlex désactivé et en bornant le bruit technique.
- **État Crossref repris depuis la conversation 1** :
  - Crossref est activé durablement avec garde-fou (`crossref.enabled: true`) ; aucun appel Crossref sans `CROSSREF_MAILTO` local.
  - Recette validée sur une seule famille : `Journal of Radio & Audio Media`, `rows: 20`, `total_results=623`, `result_count=20`, 0 erreur.
  - `db.json` contient 289 items (`to_read=144`, `candidate=89`, `ignored=56`) ; export public : 233 items whitelistés ; 20 notices Crossref fusionnées par DOI ; 0 doublon DOI.
- **Sources OpenAlex auditées** :
  - Documentation officielle consultée : API Overview, Authentication & Pricing, List Works, Search, Select Fields, Get a single work.
  - OpenAlex Works expose `id`, DOI, titre, date, type, langue, source primaire, topics, keywords, `relevance_score`, `abstract_inverted_index`, etc.
  - L'API actuelle documente une clé API gratuite pour l'usage courant ; le projet garde donc `OPENALEX_API_KEY` local si nécessaire, en plus de `OPENALEX_MAILTO` local obligatoire pour l'identification polie du connecteur futur.
- **Décision de configuration** :
  - Section `openalex` ajoutée dans `antenne_radio/config/sources.yaml` plutôt qu'un fichier dédié : la configuration reste lisible et proche de HAL/Crossref.
  - `openalex.enabled: false` par défaut ; aucun ingestor OpenAlex n'est encore branché dans `scripts/pipeline.py`.
  - Sortie prévue seulement pour une future recette : `data/raw/openalex_latest.json`.
  - Fenêtre et volume : 18 mois, `per_page: 20`, 1 page maximum par profil, `polite_delay_seconds: 1`, `sort: relevance_score:desc`.
- **Profils de requête retenus** :
  - `radio_studies` : `"radio studies"`, `radiophonic`, `"radio art"`, `"broadcasting history"`.
  - `radio_audio_media` : `"radio and audio media"`, `"audio media"`, `"broadcast media"`, `"Journal of Radio & Audio Media"`.
  - `sound_studies` : `"sound studies"`, `"sonic media"`, `"auditory culture"`, `"listening studies"`.
  - `podcast_studies` : `"podcast studies"`, `podcasting`, `"audio storytelling"`, `"serialized audio"`.
  - `community_free_radio` : `"community radio"`, `"free radio"`, `"pirate radio"`, `"radio libre"`, `"radios libres"`.
- **Exclusions de bruit obligatoires** :
  - `radio frequency`, `radiofrequency`, `radiotherapy`, `radioactive`, `radio telescope`, `radio astronomy`, `electromagnetic radiation`, `cognitive radio`, `spectrum sensing`, `beamforming`, `MIMO`, `5G`, `6G`.
- **Champs autorisés/interdits** :
  - Autorisés en privé au premier passage : identifiants OpenAlex/DOI, titre, date, type, langue, source primaire, `topics`, `primary_topic`, `keywords`, `relevance_score` OpenAlex.
  - Interdits ou reportés : `abstract_inverted_index`, abstract reconstruit, auteurs, affiliations, `locations`, PDF/fulltext, références, `content_url`, `has_content`, raw/logs/secrets en public.
  - Le score de pertinence OpenAlex et le score interne restent strictement privés ; aucun champ nouveau ne doit entrer dans `static/antenne-radio/index.json`.
- **Fichiers modifiés** :
  - `antenne_radio/config/sources.yaml`
  - `antenne_radio/LEGAL_AUDIT.md`
  - `antenne_radio/01_RESSOURCES_SUIVIES.md`
  - `antenne_radio/codex_memoire_materielle.md`
- **Commandes lancées** :
  - `git status --short` : worktree propre au départ.
  - Lecture de `docs/AGENTS.md`, `antenne_radio/README.md`, `antenne_radio/codex_memoire_materielle.md`, `antenne_radio/06_plan_v3_academique.md`.
  - `rg --files antenne_radio` et lectures ciblées de `config/sources.yaml`, `LEGAL_AUDIT.md`, `01_RESSOURCES_SUIVIES.md`, `tests/test_config.py`, `scripts/pipeline.py`, `config/keywords.yaml`, `config/scoring.yaml`.
  - Recherche web documentaire officielle OpenAlex ; aucune ingestion live lancée.
  - `git diff --check` : OK.
  - `make test` depuis `antenne_radio` : 92 tests passent.
- **Limites restantes** :
  - Aucun connecteur `ingest_openalex.py`, aucune normalisation OpenAlex, aucun run OpenAlex, aucun export public régénéré.
  - Le premier ingestor devra gérer les secrets sans les logger, appliquer les exclusions dans les requêtes ou en post-filtrage, mocker les tests réseau, et refuser le réseau sans `OPENALEX_MAILTO`.
- **Prochaine étape recommandée** :
  - Conversation fraîche Prompt 2.2 : créer `scripts/ingest/ingest_openalex.py` avec tests mockés, lire la section `openalex` déjà présente, écrire `data/raw/openalex_latest.json`, ne pas reconstruire les abstracts, ne pas brancher d'appel réseau si `enabled: false`, puis lancer `make test`.

---

## 2026-05-21 - Conversation 2 - Ingestor OpenAlex mocké et désactivé (Prompt 2.2)
- **Objectif** : Ajouter le connecteur OpenAlex en code et tests mockés, sans activation live implicite, sans cron, sans auto-commit et sans publication de données sensibles.
- **Mode retenu** :
  - `openalex.enabled` reste `false` dans `config/sources.yaml`.
  - Le pipeline sait appeler `ingest_openalex`, mais l'ingestor écrit seulement un dump local `data/raw/openalex_latest.json` avec erreur `disabled` tant que la source n'est pas activée.
  - Sans `OPENALEX_MAILTO` local, l'ingestor renvoie `missing_mailto`, écrit le dump local, logge l'erreur dans le log fourni et ne fait aucun appel réseau.
  - `OPENALEX_API_KEY` reste optionnel côté code et strictement local ; si présent, il est envoyé comme paramètre API mais redacted dans les erreurs.
- **Fichiers modifiés** :
  - `antenne_radio/scripts/ingest/ingest_openalex.py` : nouveau connecteur Works mockable, profils multiples, fenêtre 18 mois, `select` borné, exclusions de bruit, redaction `mailto`/`api_key`, classification des erreurs HTTP.
  - `antenne_radio/scripts/pipeline.py` : ajout de `DEFAULT_OPENALEX_RAW`, `openalex_raw_path`, `PipelineFunctions.ingest_openalex`, étape `ingest_openalex` et option CLI `--skip-openalex`.
  - `antenne_radio/tests/test_ingest_openalex.py` : tests mockés sans réseau réel.
  - `antenne_radio/tests/test_pipeline.py` : ordre pipeline mis à jour avec OpenAlex et skip flag.
  - `antenne_radio/tests/test_config.py` : verrou `openalex.enabled: false`, `mailto_env`, limites basses, interdiction `abstract_inverted_index`, exclusions de bruit.
  - `antenne_radio/01_RESSOURCES_SUIVIES.md` : statut humain mis à jour : ingestor présent mais désactivé.
  - `antenne_radio/codex_memoire_materielle.md` : présent handoff.
- **Comportement testé** :
  - Source désactivée : aucun appel réseau, dump local écrit, `result_count=0`.
  - `OPENALEX_MAILTO` absent : aucun appel réseau, erreur `missing_mailto`, log local.
  - Paramètres : `/works`, `mailto`, `per_page`, `page`, `sort=relevance_score:desc`, User-Agent, `select` sans `abstract_inverted_index` ni `authorships`.
  - Requêtes : profils `radio_studies` et `sound_studies` utilisés, exclusions `NOT (...)`, fenêtre `from_publication_date` calculée.
  - Limites : `per_page` respecté, 1 page par profil dans la config, `request_count` attendu.
  - Erreurs : timeout et HTTP `403`/`429`/`500` loggés et classifiés ; secrets redacted dans les messages.
- **Commandes lancées** :
  - `git status --short`
  - Lecture de `docs/AGENTS.md`, `antenne_radio/README.md`, `antenne_radio/codex_memoire_materielle.md`.
  - `rg --files antenne_radio`
  - Lectures ciblées : `scripts/ingest/ingest_crossref.py`, `scripts/ingest/ingest_hal.py`, `scripts/core/io.py`, `scripts/pipeline.py`, `tests/test_ingest_crossref.py`, `tests/test_pipeline.py`, `tests/test_config.py`, `config/sources.yaml`.
  - `.venv/bin/pytest tests/test_ingest_openalex.py tests/test_pipeline.py tests/test_config.py` : 17 tests passent.
- **Limites restantes** :
  - Aucun run live OpenAlex lancé.
  - Aucune normalisation OpenAlex dans `normalize.py`.
  - `normalize_latest_dumps` ignore encore `openalex_latest.json`; ce sera le sujet du Prompt 2.3.
  - Aucun export public régénéré ; aucun champ public ajouté.
- **Prochaine étape recommandée** :
  - Conversation fraîche Prompt 2.3 : ajouter la normalisation OpenAlex privée dans `scripts/core/normalize.py`, dédupliquer par DOI avec Crossref/HAL/RSS, brancher le score de pertinence privé, vérifier que `abstract_inverted_index`, abstracts, auteurs, tags/topics/keywords et scores restent hors export public, puis lancer `make test` et seulement les recettes publiques explicitement demandées.

---

## 2026-05-21 - Conversation 3 - Normalisation OpenAlex, scoring et anti-fuite (Prompt 2.3)
- **Objectif** : Normaliser les items OpenAlex, les intégrer à la déduplication DOI inter-sources, ajuster le scoring, ajouter l'attribution publique OpenAlex, et vérifier l'absence de fuite de données privées.
- **Pas de run live OpenAlex** : aucun appel réseau, aucune donnée réelle ingérée.
- **Décisions de scoring** :
  - `keywords.yaml` enrichi :
    - `radio_core` : ajout de `broadcasting history`, `radio production`, `radio journalism`.
    - `sound_studies` : ajout de `sound art`, `sonic geography`, `audio culture`, `noise studies`.
    - `podcast` : ajout de `podcast studies`, `audio documentary`.
    - `negative_noise` : ajout de `radiotherapy`, `radiation therapy`, `nuclear medicine`.
    - `technical_radio_noise` : ajout de `beamforming`, `radio propagation`, `antenna array`, `signal processing`.
  - `scoring.yaml` : ajout du champ `source_name` avec multiplicateur `1` dans `fields`. Les noms de revues comme « Journal of Radio & Audio Media » apportent un petit boost explicable ; mais les poids négatifs techniques dominent toujours le bruit.
  - Poids inchangés : `radio_core`/`radio_free` à 3, `sound_studies`/`podcast` à 2, `negative_noise` à −6, `technical_radio_noise` à −2.
  - Seuils inchangés : `to_read ≥ 6`, `candidate ≥ 2`, `ignored < 2`.
- **Attribution publique OpenAlex** :
  - `export_public.py` : ajout de l'entrée `"openalex"` dans `AUDITED_ATTRIBUTIONS` (famille `openalex`, URL `https://openalex.org/`) et `ATTRIBUTION_BY_SOURCE_NAME` (`"OpenAlex"` → `"openalex"`).
  - Si un item existe **uniquement** via OpenAlex, il reçoit l'attribution publique `openalex`.
  - Si un item OpenAlex doublonne un item Crossref/HAL/RSS par DOI, l'item existant conserve son attribution/source canonique ; OpenAlex ne remplace ni `source_name`, ni `url`, ni `status`, ni `source_api`.
- **Normalisation OpenAlex dans `normalize.py`** :
  - `normalize_openalex_entry()` : DOI normalisé via `normalize_doi()` existant (accepte `https://doi.org/...`, `http://dx.doi.org/...`, `doi:...`, `10....`, et `entry["ids"]["doi"]`).
  - URL canonique : DOI → `https://doi.org/...` ; sinon `primary_location.landing_page_url` ; sinon `entry["id"]` OpenAlex en dernier fallback.
  - Titre depuis `display_name` ou `title`.
  - Date depuis `publication_date` (ISO), fallback `publication_year`.
  - Langue depuis `language` ou `"und"`.
  - `source_name` depuis `primary_location.source.display_name` ou `"OpenAlex"`.
  - `source_api = "openalex"`.
  - Tags : extraction défensive de `keywords` (gère `str`, `dict` avec `display_name`/`keyword`, et formes invalides silencieusement ignorées) + `primary_topic.display_name`.
  - `source_type` mappé depuis `entry["type"]` (article, book, book-chapter, dissertation, review).
  - **Interdit** : abstract jamais reconstruit, `abstract_inverted_index` jamais touché.
  - `raw = entry` (privé, jamais exporté publiquement).
  - `normalize_latest_dumps()` accepte et lit `openalex_raw_path`, les items OpenAlex passent par `merge_items_without_duplicates` → déduplication DOI avec toutes les sources.
  - CLI : `--openalex` ajouté à `parse_args()`.
- **Pipeline** :
  - `pipeline.py` : `openalex_raw_path=paths.openalex_raw_path` passé à `functions.normalize(...)`.
- **Fichiers modifiés** :
  - `antenne_radio/scripts/core/normalize.py` : `DEFAULT_OPENALEX_RAW`, `normalize_openalex_entry()` et helpers, mise à jour de `normalize_latest_dumps()`, CLI.
  - `antenne_radio/scripts/pipeline.py` : passage de `openalex_raw_path` au normalize.
  - `antenne_radio/config/keywords.yaml` : termes radio/audio/sound renforcés, bruit technique ajouté.
  - `antenne_radio/config/scoring.yaml` : `source_name: 1` ajouté aux champs scorés.
  - `antenne_radio/scripts/export/export_public.py` : attribution `openalex` ajoutée.
  - `antenne_radio/tests/test_normalize.py` : 12 tests OpenAlex ajoutés.
  - `antenne_radio/tests/test_scoring.py` : 4 tests ajoutés (radio/audio, sound studies, bruit technique, source_name ne domine pas).
  - `antenne_radio/tests/test_export_public.py` : 3 tests ajoutés (item OpenAlex public sans score/abstract, mapping attribution, anti-fuite renforcé).
  - `antenne_radio/tests/test_config.py` : assertion `fields` mise à jour pour inclure `source_name`.
  - `antenne_radio/codex_memoire_materielle.md` : présent handoff.
- **Commandes lancées** :
  - `git status --short` : worktree propre au départ.
  - Lecture de `docs/AGENTS.md`, `antenne_radio/README.md`, `antenne_radio/codex_memoire_materielle.md`.
  - `find antenne_radio -type f` : inventaire complet des fichiers.
  - Lectures ciblées : `normalize.py`, `models.py`, `scoring.py`, `pipeline.py`, `ingest_openalex.py`, `export_public.py`, `keywords.yaml`, `scoring.yaml`, `sources.yaml`, `test_normalize.py`, `test_scoring.py`, `test_export_public.py`, `test_config.py`.
  - `.venv/bin/pytest tests/ -v --tb=short` : 119 tests passent (0 échecs).
- **Résultats anti-fuite** :
  - Tests vérifient que `abstract_inverted_index`, `authorships`, `abstract`, `raw`, `score`, `score_explanation`, `keywords_matched`, `negative_keywords_matched`, `authors`, `tags`, `source_api`, `source_feed`, `_merged_sources` sont absents du JSON public.
  - La whitelist publique reste strictement : `id`, `title`, `url`, `doi`, `published_at`, `source_name`, `source_type`, `language`, `source_family`, `attribution_id`.
- **Politique 18 mois** :
  - L'ingestion OpenAlex filtre déjà les items par `from_publication_date` dans l'ingestor (fenêtre 18 mois configurée dans `sources.yaml`).
  - La normalisation n'ajoute pas de filtre de rétention supplémentaire (pas le sujet de ce prompt).
  - Le pruning explicite (suppression des items anciens de `db.json`) reste un chantier futur documenté.
- **Compteurs OpenAlex** : aucun run live → 0 item OpenAlex réel ingéré.
- **Limites restantes** :
  - Aucun run live OpenAlex lancé.
  - `db.json` et `static/antenne-radio/index.json` n'ont pas été régénérés.
  - `LEGAL_AUDIT.md` pourrait être mis à jour pour documenter l'attribution OpenAlex publique.
  - Le pruning 18 mois de `db.json` n'est pas encore implémenté.
- **Prochaine étape recommandée** :
  - Conversation fraîche Prompt 2.4 : activation temporaire OpenAlex avec `OPENALEX_MAILTO` local, run ultra-limité (1 profil, 1 page, `per_page: 5`), inspection de `openalex_latest.json` et `db.json`, vérification des compteurs et de la déduplication réelle, `make export-public` + scan anti-fuite, puis remise à `enabled: false` sauf décision contraire documentée. Mise à jour de `LEGAL_AUDIT.md` pour l'attribution OpenAlex.

---

## 2026-05-21 - Conversation 3 - Audit des venues et réseaux prioritaires (Prompt 3.1)
- **Objectif** : Identifier les accès stables et légaux pour les venues/réseaux prioritaires sans ingestion live, sans cron, sans auto-commit et sans publication de données privées.
- **Résultat synthétique** :

| Venue/réseau | Statut humain | Classement retenu | Décision |
|---|---|---|---|
| Radio Journal: International Studies in Broadcast & Audio Media | `candidat` | Activable via Crossref ; RSS Intellect à valider | Revue distincte de Journal of Radio & Audio Media ; prochaine étape par ISSN `1476-4504` / `2040-1388`, pas de doublon. |
| Sound Studies: An Interdisciplinary Journal | `candidat` | Activable via Crossref ou OpenAlex ; RSS Taylor & Francis probable à valider | Revue T&F distincte de Sounding Out! ; prochaine étape par ISSN `2055-1940` / `2055-1959`. |
| JSS / Journal of Sonic Studies | `candidat` | Activable via OpenAlex ; Crossref à vérifier | ISSN `2212-6252`, DOIs JSS repérés, mais pas de RSS JSS dédié confirmé ; ne pas utiliser le flux global Research Catalogue. |
| Resonance: The Journal of Sound and Culture | `candidat` | Activable via Crossref ou OpenAlex ; RSS UC Press non confirmé | e-ISSN `2688-867X`, DOI UC Press ; ne pas scraper `online.ucpress.edu`. |
| IAMCR Music, Audio, Radio and Sound Working Group | `reporté` | Réseau à suivre par annonces | Page officielle riche mais aucun RSS/API stable repéré ; veille manuelle seulement pour l'instant. |
| ECREA Radio and Sound Section | `reporté` | Réseau à suivre par annonces | Page section + Weekly Digest général ; aucun flux stable spécifique repéré. |
| MeCCSA Radio & Audio Studies | `actif` | Réseau suivi par RSS/annonces | Déjà configuré via `meccsa_radio_audio_studies`, flux WordPress actif ; ne pas créer de doublon. |

- **Fichiers modifiés** :
  - `antenne_radio/01_RESSOURCES_SUIVIES.md` : ajout de la table d'audit venues/réseaux, qualification des statuts humains et enrichissement de la ligne MeCCSA active.
  - `antenne_radio/codex_memoire_materielle.md` : présent handoff.
- **Commandes lancées** :
  - `git status --short` : worktree propre au départ.
  - Lecture de `docs/AGENTS.md`, `antenne_radio/README.md`, `antenne_radio/codex_memoire_materielle.md`.
  - `rg --files antenne_radio` : chemins réels repérés avant modification.
  - Lectures ciblées : `antenne_radio/01_RESSOURCES_SUIVIES.md`, `antenne_radio/LEGAL_AUDIT.md`, `antenne_radio/config/sources.yaml`.
  - Recherches web officielles/documentaires : pages Intellect/Intellect Discover, Taylor & Francis, Research Catalogue/JSS, ISSN Portal, DOAJ, UC Press/Scholastica, IAMCR, ECREA, MeCCSA, OpenAlex docs, Crossref docs.
- **Contraintes respectées** :
  - Aucune ingestion live lancée.
  - Aucun cron créé.
  - Aucun auto-commit.
  - Aucune source live ajoutée dans `config/sources.yaml`.
  - Aucun raw, log, abstract, score, auteur, tag privé ou chemin local publié.
  - Pas de scraping HTML retenu comme stratégie pour IAMCR/ECREA/JSS.
- **Incertitudes restantes** :
  - Les URL exactes de RSS article pour Radio Journal/Intellect, Sound Studies/Taylor & Francis et Resonance/UC Press devront être validées techniquement dans une recette séparée avant configuration.
  - La couverture Crossref de JSS doit rester prudente : les DOIs existent, mais OpenAlex/DOAJ/ISSN sont les points d'accès les plus propres à ce stade.
  - IAMCR et ECREA sont intellectuellement prioritaires, mais restent non automatisables sans flux officiel stable spécifique.
- **Prochaine étape recommandée pour une conversation fraîche** :
  - Prompt 3.2 : ajouter uniquement des sources candidates désactivées ou une recette de test ultra-limitée pour une seule revue à la fois, en commençant par Radio Journal ou Sound Studies via Crossref par ISSN avec `CROSSREF_MAILTO` local, `rows: 5`, tests mockés si code changé, puis scan anti-fuite avant toute activation durable. Garder IAMCR/ECREA hors pipeline automatisé tant qu'aucun flux officiel stable n'est confirmé.

---

## 2026-05-21 - Conversation 3 - Configuration des venues et profils de requête (Prompt 3.2)
- **Objectif** : Ajouter les venues validées dans la configuration sans doublonner les sources V2 et sans créer de bruit massif.
- **Aucune ingestion live** : aucun `make run`, aucun appel réseau Crossref/OpenAlex, aucun export public régénéré.
- **Sources ajoutées ou modifiées** :
  - `crossref.journals.radio_journal` : nouvelle revue candidate désactivée (`enabled: false`), ISSN `1476-4504` et `2040-1388`, métadonnées Crossref uniquement jusqu'à run inspecté.
  - `crossref.journals.sound_studies_journal` : nouvelle revue candidate désactivée, ISSN `2055-1940` et `2055-1959`, distincte de `sounding_out_blog`.
  - `crossref.journals.resonance_journal` : nouvelle revue candidate désactivée, e-ISSN `2688-867X`, sans RSS UC Press forcé.
  - `openalex.profiles.journal_sonic_studies_venue` : nouveau profil de venue désactivé, filtre `primary_location.source.issn:2212-6252`, tri `publication_date:desc`.
  - `scripts/ingest/ingest_openalex.py` : support réel des filtres par profil OpenAlex, y compris les profils sans `search` mais avec filtre de venue, et support d'un `sort` propre au profil.
  - `scripts/export/export_public.py` : attributions publiques ajoutées pour `radio_journal`, `sound_studies_journal`, `journal_sonic_studies`, `resonance_journal`, sans modifier la whitelist publique.
- **Sources laissées inactives ou non ajoutées** :
  - Les quatre nouvelles venues restent désactivées tant qu'aucun run contrôlé n'a été inspecté.
  - IAMCR MAR et ECREA Radio & Sound restent hors `config/sources.yaml` faute de flux officiel stable spécifique.
  - `journal_radio_audio_media`, `sounding_out_blog` et `meccsa_radio_audio_studies` n'ont pas été dupliqués.
- **Fichiers modifiés** :
  - `antenne_radio/config/sources.yaml`
  - `antenne_radio/scripts/ingest/ingest_openalex.py`
  - `antenne_radio/scripts/export/export_public.py`
  - `antenne_radio/tests/test_config.py`
  - `antenne_radio/tests/test_ingest_openalex.py`
  - `antenne_radio/tests/test_export_public.py`
  - `antenne_radio/01_RESSOURCES_SUIVIES.md`
  - `antenne_radio/codex_memoire_materielle.md`
- **Commandes lancées** :
  - `git status --short` : worktree déjà modifié par le handoff/documentation du Prompt 3.1.
  - Lecture de `docs/AGENTS.md`, `antenne_radio/README.md`, `antenne_radio/codex_memoire_materielle.md`.
  - `rg --files antenne_radio` : chemins réels repérés avant modification.
  - Lectures ciblées : `config/sources.yaml`, `scripts/ingest/ingest_crossref.py`, `scripts/ingest/ingest_openalex.py`, `scripts/core/normalize.py`, `scripts/export/export_public.py`, `tests/test_config.py`, `tests/test_ingest_openalex.py`, `tests/test_ingest_crossref.py`, `tests/test_export_public.py`, `01_RESSOURCES_SUIVIES.md`.
  - Recherche documentaire officielle OpenAlex sur les filtres de Works, notamment `primary_location.source.issn`.
  - `.venv/bin/pytest tests/test_config.py tests/test_ingest_openalex.py tests/test_export_public.py -v --tb=short` : 40 tests passent.
- **Résultats de tests** :
  - Tests ciblés : 40 passed.
  - `make test` depuis `antenne_radio` : 127 passed.
- **Contraintes respectées** :
  - Pas de cron, pas d'auto-commit.
  - Pas de nouvelle source activée.
  - Pas de publication de raw, logs, abstracts, scores, auteurs, tags ou chemins locaux.
  - Whitelist publique inchangée : `id`, `title`, `url`, `doi`, `published_at`, `source_name`, `source_type`, `language`, `source_family`, `attribution_id`.
- **Prochaine étape recommandée pour une conversation fraîche** :
  - Prompt 3.3 : recette de validation contrôlée pour une seule venue désactivée à la fois, idéalement `radio_journal` ou `sound_studies_journal`, avec `CROSSREF_MAILTO` local, `rows` abaissé temporairement à `5`, activation d'un seul profil, inspection de `crossref_latest.json`/normalisation/déduplication, puis `make export-public` et scan anti-fuite avant toute activation durable. Ne pas activer IAMCR/ECREA tant qu'un flux officiel stable spécifique n'existe pas.

---

## 2026-05-21 - Conversation 3 - Recette finale V3 et gel du périmètre V4 (Prompt 3.3)
- **État final V3** : V3 académique validée localement puis gelée. Le pipeline reste volontairement manuel, sans cron, sans auto-commit, sans publication automatique et sans élargissement silencieux de la whitelist publique.
- **Pré-vol demandé** :
  - `git status --short` lancé avant modification : worktree déjà modifié par les travaux 3.1/3.2 (`01_RESSOURCES_SUIVIES.md`, `codex_memoire_materielle.md`, `config/sources.yaml`, `export_public.py`, `ingest_openalex.py`, tests OpenAlex/export/config).
  - Lecture effectuée de `docs/AGENTS.md`, `antenne_radio/README.md`, `antenne_radio/codex_memoire_materielle.md`.
  - Chemins réels repérés avec `rg --files`/`find` avant création ou édition ; aucun nouveau fichier créé pour la V3.
- **Sources actives dans la recette finale** :
  - RSS/Atom : 10 sources actives (`radio_survivor`, `radiomorphoses`, `radio_fanch`, `les_radios_libres`, `la_radio_du_futur`, `la_lettre_pro`, `meccsa_radio_audio_studies`, `nieman_storyboard`, `journal_radio_audio_media`, `sounding_out_blog`).
  - HAL : actif, limite 20.
  - Crossref : actif seulement sur `journal_radio_audio_media`, `rows: 20`, `polite_delay_seconds: 1`, `CROSSREF_MAILTO` fourni uniquement comme variable d'environnement de commande pour le run final, sans écriture dans le dépôt ni dans les docs.
- **Sources configurées mais inactives** :
  - RSS : `transom`, `sounding_out_podcast`, `example_disabled_journal`.
  - Crossref candidates : `radio_journal`, `sound_studies_journal`, `resonance_journal`.
  - OpenAlex : `openalex.enabled: false`, profils désactivés ou inactifs (`radio_studies`, `radio_audio_media`, `sound_studies`, `podcast_studies`, `community_free_radio`, `journal_sonic_studies_venue`).
  - Réseaux reportés hors config : IAMCR MAR et ECREA Radio and Sound tant qu'aucun flux officiel stable spécifique n'est identifié.
- **Commandes et résultats** :
  - `make test` depuis `antenne_radio` : 127 tests passent.
  - `make run` sans contact Crossref local : pipeline OK mais Crossref a correctement déclenché `missing_mailto`; ce passage a servi à vérifier le garde-fou.
  - `make run` final avec contact Crossref fourni en variable d'environnement locale et réseau autorisé : pipeline OK, `failed_steps=none`.
  - `make export-public` final : 239 items publics générés.
  - `pnpm run build` depuis la racine : Hugo 0.160.1, build OK, 83 pages.
- **Compteurs réels finaux** :
  - `data/raw/rss_latest.json` : 239 entrées, 0 erreur.
  - `data/raw/hal_latest.json` : 20 documents, `num_found=931`, 0 erreur.
  - `data/raw/crossref_latest.json` : 20 notices, `rows=20`, 0 erreur.
  - `data/raw/openalex_latest.json` : 0 item, erreur locale `disabled`, comportement attendu.
  - `data/normalized/db.json` : 295 items (`to_read=150`, `candidate=89`, `ignored=56`), 0 doublon DOI détecté.
  - `static/antenne-radio/index.json` et `public/antenne-radio/index.json` : 239 items, schéma `antenne-radio-public-v0`, clés publiques strictement limitées à `id`, `title`, `url`, `doi`, `published_at`, `source_name`, `source_type`, `language`, `source_family`, `attribution_id`.
  - Export privé Obsidian `veille-2026-21.md` : 238 entrées listées dans le rapport privé.
  - Export privé Zotero CSL `zotero-veille-2026-21.csl.json` : 152 items.
- **Scans anti-fuite** :
  - JSON public statique et buildé : 0 clé interdite (`raw`, `abstract`, `authors`, `tags`, `score`, `score_explanation`, `keywords`, `logs`, `status`, `source_api`, `source_feed`, `raw_responses`, `errors`, `relevance_score`, `abstract_inverted_index`, etc.).
  - JSON public et HTML : 0 email, 0 occurrence du contact fourni, 0 chemin local, 0 nom de variable sensible, 0 bearer/token/key.
  - Faux positifs contrôlés : le token `score` apparaît uniquement dans un titre/URL bibliographique public ; `tags` apparaît une seule fois dans la navigation globale Hugo (`/tags/`), pas dans les données Antenne.
  - Logs privés inspectés : aucune adresse email ni contact fourni détecté ; les paramètres `mailto=` présents dans l'historique du log ne contiennent pas d'adresse et les erreurs sensibles restent redacted.
- **Documentation mise à jour** :
  - `antenne_radio/README.md` : état de clôture V3, compteurs et périmètre V4.
  - `antenne_radio/01_RESSOURCES_SUIVIES.md` : recette finale, compteurs, statuts actifs/inactifs.
  - `antenne_radio/LEGAL_AUDIT.md` : note de clôture V3 et report explicite de CiNii/NDL/J-STAGE en V4.
  - `docs/CHANTIERS.md` : V3 marquée terminée, V4 japonaise séparée.
  - `antenne_radio/codex_memoire_materielle.md` : présent handoff.
- **Limites restantes** :
  - Crossref reste validé sur une seule revue active ; ne pas activer `radio_journal`, `sound_studies_journal` ou `resonance_journal` sans recette limitée par une seule revue, volume bas et scan anti-fuite.
  - OpenAlex est prêt techniquement mais reste inactif ; aucun run live OpenAlex n'a été lancé.
  - IAMCR/ECREA restent des veilles humaines tant qu'aucun flux officiel stable spécifique n'est confirmé.
  - Le pruning 18 mois de `db.json` reste un chantier futur.

### V4 japonaise plus tard

La V4 japonaise est explicitement hors bilan V3. Elle pourra couvrir :

- `CiNii` ;
- `NDL` ;
- `J-STAGE` ;
- littérature japonaise sur mini-FM, Tetsuo Kogawa, radios communautaires, micro-radios, sound/media studies au Japon.

Conditions d'audit avant implémentation V4 :

- relire `docs/AGENTS.md`, `antenne_radio/README.md`, `antenne_radio/LEGAL_AUDIT.md`, `01_RESSOURCES_SUIVIES.md` et cette mémoire ;
- auditer les APIs officielles, conditions d'utilisation, attribution obligatoire, cadence, encodage japonais, translittération et types de métadonnées ;
- définir une whitelist publique V4 avant toute ligne de code ;
- écrire les tests anti-fuite avant ingestion live ;
- commencer par une source unique, volume minimal, sans cron, sans auto-commit, sans abstracts publics et sans données brutes publiques.

Première proposition de Conversation 1 pour la V4 japonaise :

```text
Objectif : ouvrir la V4 japonaise sans implémenter encore de connecteur.

Avant toute modification :
- lancer git status --short ;
- lire docs/AGENTS.md ;
- lire antenne_radio/README.md ;
- lire antenne_radio/LEGAL_AUDIT.md ;
- lire antenne_radio/01_RESSOURCES_SUIVIES.md ;
- lire antenne_radio/codex_memoire_materielle.md ;
- ne lancer aucune ingestion live ;
- ne créer aucun cron ;
- ne publier aucun raw, log, abstract, score, auteur, tag, chemin local ou secret.

Tâches :
1. Auditer séparément CiNii, NDL et J-STAGE : API officielle, conditions d'utilisation, attribution, rate limit, formats, champs disponibles, risques de fuite.
2. Définir le contrat public V4 minimal, en distinguant titres japonais, romanisation éventuelle, auteurs, revue/source, date, DOI/identifiants, URL canonique.
3. Choisir une seule première source candidate pour Conversation 2, sans l'activer.
4. Mettre à jour LEGAL_AUDIT.md, 01_RESSOURCES_SUIVIES.md et codex_memoire_materielle.md avec les décisions.

Vérification :
- aucune donnée live collectée ;
- aucun secret écrit ;
- V4 reste séparée de la V3 ;
- prochain prompt limité à un seul connecteur mocké.
```

## 2026-05-21 - Conversation 4 - Activation de Crossref (plusieurs revues) et d'OpenAlex en production (Prompt 3.1)

- **Objectif** : Activer pleinement en production le connecteur OpenAlex (venue JSS) et les 3 revues académiques Crossref validées (`radio_journal`, `sound_studies_journal`, `resonance_journal`), tout en maintenant la politique stricte de confidentialité (zéro fuite, respect de `LEGAL_AUDIT.md`).
- **Actions réalisées** :
  - Mise à jour de `config/sources.yaml` : activation globale d'OpenAlex (`openalex.enabled: true`), de la venue JSS (`journal_sonic_studies_venue.enabled: true`) et des 3 revues prioritaires de la famille Crossref.
  - Mise à jour documentaire complète :
    - `01_RESSOURCES_SUIVIES.md` : mise à jour des statuts et compteurs d'activation.
    - `LEGAL_AUDIT.md` : note de clôture mise à jour pour refléter l'état "active: true" de Crossref (plusieurs revues) et OpenAlex (JSS venue).
    - `README.md` : actualisation de la section "Ce que fait le projet", de l'état de clôture de la V3 académique, et des consignes de rate limit / mailto locaux.
    - `codex_memoire_materielle.md` : actualisation du présent Codex.
  - Validation technique locale :
    - Exécution de `make test` : validation des 127 tests unitaires réussie à 100%.
    - Exécution de `make run` avec un fichier `.env.local` configuré localement (ignoré par Git) pour l'usage poli des API : aucun exception lancée, récolte fructueuse.
    - Exécution de `make export-public` : 239 items exportés en public avec application rigoureuse de la whitelist anti-fuite.


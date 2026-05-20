# Mémoire matérielle - antenne radio

## Reprise rapide & État du pipeline v2
- **Démarrage rapide** : Lancer `git status --short`, lire `docs/AGENTS.md` et `antenne_radio/README.md`.
- **Architecture & Local** : Le sous-projet vit exclusivement dans `antenne_radio/` avec son `.venv` et ses dépendances. Pas de cron, pas d'auto-commit, pas de LLM.
- **Pipeline opérationnel** : Ingestion RSS/Atom (10 sources actives) + HAL (requête ciblée resserrée) -> Normalisation `RadioWatchItem` dédupliquée dans `data/normalized/db.json` (283 items) -> Scoring lexical (poids positifs, négatifs `-6` et techniques `-2`) -> Exports privés (Obsidian hebdomadaire, Zotero CSL JSON) et Export public (`static/antenne-radio/index.json`, 227 items whitelistés).
- **Intégration Hugo** : Page `/antenne-radio/` lisant le JSON public au build-time (avec fallback `<noscript>` de 50 cartes) et l'hydratant via JS Vanilla dynamique en mémoire (recherche, filtres ET multi-critères, deep-linking, chargement progressif par 50).

## Contrats de données & Sécurité
- **db.json** : Doit rester valide, UTF-8 non échappé, trié par clés. Déduplication par ID stable (DOI > URL > Title/Date). Jamais de suppression automatique des `ignored`.
- **Confidentialité absolue (Anti-fuite)** : Interdiction stricte de publier abstracts, raw dumps, logs, scores, explications, mots-clés internes, auteurs, tags ou chemins locaux. Seul le JSON whitelisté est public.
- **Crossref** : Connecteur préparé mais désactivé par défaut (`enabled: false`). Nécessite la configuration d'un `CROSSREF_MAILTO` valide localement.
- **OpenAlex** : Intégration planifiée en V3 avec `OPENALEX_MAILTO` local obligatoire, requêtes ciblées et score de pertinence strictement privé.

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

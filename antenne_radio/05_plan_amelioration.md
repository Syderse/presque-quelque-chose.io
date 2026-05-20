# Antenne Radio v2 — Plan d'amélioration stable et publiable

```text
Note d'exécution :
- Ce plan vise une v2 validée localement et prête à publier, sans déploiement automatique.
- Le build Hugo ne doit jamais lancer l'ingestion.
- Le JSON public est généré par commande explicite avant build.
- Les sources RSS incertaines restent enabled: false tant que l'audit ne les valide pas clairement.
- Aucun infinite scroll en v2 : pagination par bouton explicite uniquement.
- Tous les chemins doivent être résolus à partir de l'état réel du dépôt ; ne jamais créer de doublons documentaires ou scripts à la racine.
- Tous les chemins de l'antenne sont à résoudre depuis le dossier réel du module antenne_radio/. Ne jamais créer de doublon à la racine si un fichier équivalent existe déjà dans antenne_radio/.
```

## Contexte et trajectoire de progression

L'antenne radio v1 est **fonctionnelle mais confidentielle** :
- Pipeline local robuste : RSS (3 sources actives) + HAL + Crossref (désactivé) → normalisation → scoring → exports privés + JSON public minimal.
- Page Hugo `/antenne-radio/` existe mais reste invisible dans les menus (accessible uniquement depuis le manuel d'aide).
- Rendu en simple tableau HTML statique de 152 items, sans filtre ni recherche possible.
- Philosophie lightweight respectée (0 dépendance externe, tests complets).

### Objectifs de la v2 (Stable et Publiable)
1. **Visibilité & Navigation** — Rendre l'antenne accessible de façon élégante dans la barre latérale et le menu mobile.
2. **Fenêtre temporelle & Limitation légale** — Exporter uniquement un index de liens publics limité aux **18 derniers mois (540 jours)** avec la catégorie publique (`source_category`).
3. **Audit et nouvelles sources RSS simples** — Réaliser l'audit documentaire et intégrer uniquement des sources RSS simples (sans connecteur d'API lourd).
4. **Page interactive premium & lightweight** — Remplacer le tableau par une grille de cartes au style neo-brutaliste premium (Catppuccin), avec filtrage instantané en mémoire, lazy rendering, deep-linking URL et un fallback statique accessible (no-JS).
5. **Garde-fous d'éco-conception** — Code JS vanilla pur, autonome, sous forme de mémoire dynamique (le DOM devenant une simple cible de rendu et non la source de vérité), sans framework ni CDN, et avec des animations CSS strictement optimisées.
6. **Pas d'inondation académique** — Toutes les sources universitaires lourdes ou connecteurs d'API complexes (OpenAlex, DOAJ, Persée, moissonnage OPML massif, etc.) sont explicitement reportés à la v3.

---

## Audit des sources RSS simples prioritaires

| Source | Type | Flux RSS stable | Statut recommandé | Priorité |
|---|---|---|---|---|
| **Radiomorphoses** | Revue académique (OpenEdition) | `https://journals.openedition.org/radiomorphoses/backend?format=rsspeople` | ✅ Activable après audit | Haute |
| **Radio Fañch** (Fañch Langoët) | Blog Blogger | `https://radiofanch.blogspot.com/feeds/posts/default` | ✅ Activable après audit | Haute |
| **Les Radios Libres** (S. Poulain) | Blog WordPress | `https://lesradioslibres.wordpress.com/feed/` | ✅ Activable après audit | Haute |
| **La Radio du Futur** (S. Poulain) | Blog WordPress | `https://radiodufutur.wordpress.com/feed/` | ✅ Activable après audit | Haute |
| **La Lettre Pro de la Radio** | Presse professionnelle | `https://www.lalettre.pro/xml/syndication.rss` | ✅ Activable après audit | Moyenne |
| **MeCCSA Radio & Audio Studies** | Blog WordPress académique | `https://meccsaradioaudiostudies.wordpress.com/feed/` | ✅ Activable après audit | Moyenne |
| **Nieman Storyboard** | Plateforme journalisme | Flux RSS principal disponible | ⚠️ À valider à l'audit | Basse |
| **Transom** | Plateforme audio | `https://transom.org/feed/` | ⚠️ À retester (301 connu) | Basse |

---

## Architecture de l'interface publique (Discipline AGENTS.md)

L'interaction client repose sur une structure propre et conditionnelle :
```
static/antenne-radio/index.json     ← Fichier JSON public whitelisted, généré avant le build par make export-public puis simplement lu par Hugo
layouts/antenne-radio/list.html      ← Template listant le fallback statique et la structure
assets/js/antenne-radio.js           ← Script de filtrage et rendu en mémoire (< 8-12 Ko)
```

### 1. Modèle de Rendu et de Filtrage (Client-Side)
- **Fallback No-JS** : Le template Hugo lit `static/antenne-radio/index.json` et rend les 50 premiers items de façon statique et accessible au build dans un conteneur `<noscript>`.
- **Rendu dynamique JS** : Si JavaScript est actif, le script intercepte le chargement, lit le fichier `index.json`, stocke l'index en mémoire, et génère dynamiquement l'interface. Le DOM n'est plus la source de vérité, mais simplement la sortie d'un état calculé en mémoire.
- **Rendu par lots (Lazy Rendering)** : Afin de préserver la réactivité sur mobile, l'affichage initial est limité à 50 cartes. Un bouton explicite "Afficher plus de signaux" permet de charger les 50 éléments suivants. Aucun infinite scroll ne doit être implémenté.

### 2. Charte UI/UX & Aesthétique Premium
- **Style Neo-brutaliste (Catppuccin)** : Utilisation de cartes géométriques avec des bordures franches (`border: 2px solid var(--border-color)`) et des ombres nettes décalées (`box-shadow: 4px 4px 0px var(--shadow-color)`).
- **Intolérance à la lenteur** :
  - **Interdiction formelle** d'utiliser `transition: all`, des filtres graphiques complexes (`filter`, `drop-shadow`), des flous (`backdrop-filter`) ou du `will-change` permanent.
  - Les transitions CSS de survol (hover) s'effectuent sur `transform` et `box-shadow` uniquement (`transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.2s cubic-bezier(0.4, 0, 0.2, 1)`).
- **Zéro Squelette (No Skeletons)** : Les squelettes pulsants génèrent du clignotement inutile pour un fichier JSON local statique. Ils sont supprimés du plan au profit d'un chargement instantané.
- **État Vide Simple (Empty State)** : Créer un état vide simple, élégant et léger : un message textuel soigné, une petite icône SVG inline ou des formes CSS minimales, et un bouton de réinitialisation. Une animation optionnelle est autorisée uniquement si elle reste triviale et désactivable. Respecter strictement la directive `prefers-reduced-motion`.

### 3. Schéma JSON public v1 (`antenne-radio-public-v1`)
Le format public évolue pour supporter le filtrage par catégories :
```json
{
  "schema_version": "antenne-radio-public-v1",
  "generated_at": "2026-05-19T17:45:00Z",
  "window_days": 540,
  "item_count": 152,
  "items": [
    {
      "id": "stable_uuid_hash",
      "title": "Titre de l'article",
      "url": "https://...",
      "doi": null,
      "published_at": "2026-05-15T00:00:00Z",
      "source_name": "Radiomorphoses",
      "source_type": "blog",
      "source_category": "revue",
      "language": "fr",
      "source_family": "rss",
      "attribution_id": "radiomorphoses"
    }
  ],
  "sources": [...]
}
```
> [!IMPORTANT]
> Le champ `source_category` sert à filtrer les articles par typologie (presse, revue, blog, podcast). La fenêtre temporelle exclut tout item publié il y a plus de 540 jours de l'export public. Les abstracts, scores, logs et chemins restent strictement confidentiels et ne quittent pas la base privée `db.json`.

---

## Séquence de 9 prompts pour la v2 stable

---

### Prompt 1 — Audit d'état réel et CI manuelle

**Périmètre :** Vérification de l'environnement local et configuration GitHub Actions initiale dans `antenne_radio/`.

```text
Objectif : Mettre en place un premier workflow d'intégration continue (CI) sans déclenchement invisible, tout en vérifiant l'état réel.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repère les chemins réels des fichiers avant d’en créer de nouveaux ;
- ne lance aucune ingestion live non demandée ;
- ne crée aucun cron ;
- ne crée aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores ou chemins locaux.
- Tous les chemins de l'antenne sont à résoudre depuis le dossier réel du module antenne_radio/. Ne jamais créer de doublon à la racine si un fichier équivalent existe déjà dans antenne_radio/.

Tâches :
1. Vérifier si un répertoire `.github/workflows/` existe à la racine du dépôt.
2. Créer le fichier `.github/workflows/tests.yml` contenant la définition d'un workflow GitHub Action :
   - Déclencheur : workflow_dispatch uniquement (déclenchement volontaire et manuel via l'UI GitHub). Aucun cron, aucun commit automatique sur pull request ou push.
   - Étapes : Checkout du dépôt, installation de Python 3.11 ou 3.12 (avec cache pip pour accélérer le processus), installation des dépendances à partir de `antenne_radio/requirements.txt` et exécution de la suite de tests via `make test` dans `antenne_radio/`.
3. Valider la syntaxe et s'assurer que la commande de test s'exécute correctement localement sans secrets.
4. Reprends à 0 le antenne_radio/README.md pour expliquer comme à un débutant comment faire l'opération manuelle, à quoi elle sert, comment actualiser la récolte de sources du projet chaque semaine, etc. 

Vérification : Le fichier `.github/workflows/tests.yml` est valide. La commande `make test` passe localement à 100%.

Ajoute un bref handoff dans antenne_radio/codex_memoire_materielle.md :
- fichiers modifiés ;
- commandes lancées ;
- résultats réels ;
- limites restantes ;
- prochaine étape recommandée.
```

---

### Prompt 2 — Navigation antenne radio dans Hugo

**Périmètre :** Configuration de la navigation desktop et mobile de la v2.

```text
Objectif : Rendre l'antenne radio visible dans la barre latérale et le menu mobile du site.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repère les chemins réels des fichiers avant d’en créer de nouveaux ;
- ne lance aucune ingestion live non demandée ;
- ne crée aucun cron ;
- ne crée aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores ou chemins locaux.
- Tous les chemins de l'antenne sont à résoudre depuis le dossier réel du module antenne_radio/. Ne jamais créer de doublon à la racine si un fichier équivalent existe déjà dans antenne_radio/.

Tâches :
1. Localiser le fichier de configuration Hugo principal (ex: `config/_default/hugo.yaml` ou équivalent).
2. Ajouter l'entrée `antenne radio` dans `menus.main` avec l'URL `/antenne-radio/` et un poids `weight: 35` (se positionnant proprement entre l'entrée "ondes & pixels" et "rhizome curieux").
3. Ajouter une icône SVG dédiée (signal / antenne) dans `layouts/partials/sidebar.html` et l'associer au dictionnaire `$icons` dans `layouts/partials/mobile-nav.html` pour la nav mobile.
4. Ajuster les variables ou classes de couleurs cycliques globales s'il y a lieu pour assurer un rendu esthétique impeccable.
5. Lancer un build de validation Hugo complet (avec flags de warning). Le build ne doit jamais lancer l'ingestion d'antenne radio, il doit simplement lire le JSON existant.

Vérification : Le build Hugo réussit sans erreur. La barre latérale et le menu mobile affichent l'entrée "antenne radio" avec son icône.

Ajoute un bref handoff dans antenne_radio/codex_memoire_materielle.md :
- fichiers modifiés ;
- commandes lancées ;
- résultats réels ;
- limites restantes ;
- prochaine étape recommandée.
```

---

### Prompt 3 — Fenêtre 18 mois et schéma public v1

**Périmètre :** Script d'export public (`antenne_radio/scripts/export/export_public.py`) et tests associés dans `antenne_radio/tests/`.

```text
Objectif : Implémenter le filtrage par fenêtre temporelle de 18 mois et faire évoluer le schéma JSON public en v1.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repère les chemins réels des fichiers avant d’en créer de nouveaux ;
- ne lance aucune ingestion live non demandée ;
- ne crée aucun cron ;
- ne crée aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores ou chemins locaux.
- Tous les chemins de l'antenne sont à résoudre depuis le dossier réel du module antenne_radio/. Ne jamais créer de doublon à la racine si un fichier équivalent existe déjà dans antenne_radio/.

Tâches :
1. Modifier `antenne_radio/scripts/export/export_public.py` pour introduire le paramètre `--window-days` (valeur par défaut : 540, soit 18 mois).
2. Filtrer les items lors de la génération du JSON public : les items dont `published_at` remonte à plus de 540 jours restent présents dans la base de données privée `antenne_radio/data/normalized/db.json` mais sont exclus du JSON public exporté.
3. Ajouter le champ `source_category` au schéma de sortie (mapping déterminé par la source ou l'attribution : `presse`, `blog`, `podcast`, `revue`, `académique`).
4. Mettre à jour `PUBLIC_ITEM_KEYS` avec `source_category` et changer le champ de version globale de schéma à `antenne-radio-public-v1`.
5. Écrire des tests unitaires dans `antenne_radio/tests/test_export_public.py` couvrant :
   - l'exclusion des items anciens (> 540 jours) ;
   - la présence et le bon type du champ `source_category` ;
   - les tests de non-fuite (s'assurer qu'aucun abstract ou champ interne n'apparaît).
6. Lancer `make test` puis exécuter l'export pour régénérer `static/antenne-radio/index.json`.

Vérification : Le fichier `static/antenne-radio/index.json` respecte la whitelist et ne contient aucun article datant de plus de 18 mois. Les tests passent à 100%.

Ajoute un bref handoff dans antenne_radio/codex_memoire_materielle.md :
- fichiers modifiés ;
- commandes lancées ;
- résultats réels ;
- limites restantes ;
- prochaine étape recommandée.
```

---

### Prompt 4 — Audit légal documentaire des sources RSS simples

**Périmètre :** Documentation éthique et juridique (`antenne_radio/LEGAL_AUDIT.md` et `antenne_radio/01_RESSOURCES_SUIVIES.md`).

```text
Objectif : Auditer la conformité juridique et les conditions de citation des flux RSS simples avant leur intégration technique.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repère les chemins réels des fichiers avant d’en créer de nouveaux ;
- ne lance aucune ingestion live non demandée ;
- ne crée aucun cron ;
- ne crée aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores ou chemins locaux.
- Tous les chemins de l'antenne sont à résoudre depuis le dossier réel du module antenne_radio/. Ne jamais créer de doublon à la racine si un fichier équivalent existe déjà dans antenne_radio/.

Tâches :
1. Analyser individuellement les conditions d'utilisation des sources RSS faciles suivantes :
   - Radiomorphoses
   - Radio Fañch
   - Les Radios Libres
   - La Radio du Futur
   - La Lettre Pro de la Radio
   - MeCCSA Radio & Audio Studies
   - Nieman Storyboard
   - Transom (à retester pour s'assurer de sa disponibilité)
2. Déterminer explicitement pour chaque source :
   - le droit d'indexation du titre, de la date de publication et de l'URL originale ;
   - les exigences de citation et de lien d'attribution ;
   - l'interdiction éventuelle de stocker ou republier les résumés/abstracts.
3. Consigner les verdicts, conditions, dates d'audit et URLs sources consultées dans `antenne_radio/LEGAL_AUDIT.md`.
4. Mettre à jour en miroir `antenne_radio/01_RESSOURCES_SUIVIES.md` en y indiquant le statut juridique validé pour ces sources.

Vérification : `antenne_radio/LEGAL_AUDIT.md` contient un verdict motivé pour chaque source. Aucun code n'est modifié.

Ajoute un bref handoff dans antenne_radio/codex_memoire_materielle.md :
- fichiers modifiés ;
- commandes lancées ;
- résultats réels ;
- limites restantes ;
- prochaine étape recommandée.
```

---

### Prompt 5 — Intégration technique des sources RSS simples

**Périmètre :** Configuration d'ingestion (`antenne_radio/config/sources.yaml`), script d'export (`antenne_radio/scripts/export/export_public.py`) et validation.

```text
Objectif : Intégrer techniquement les sources RSS simples déclarées conformes lors de l'audit légal.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repère les chemins réels des fichiers avant d’en créer de nouveaux ;
- ne lance aucune ingestion live non demandée ;
- ne crée aucun cron ;
- ne crée aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores ou chemins locaux.
- Tous les chemins de l'antenne sont à résoudre depuis le dossier réel du module antenne_radio/. Ne jamais créer de doublon à la racine si un fichier équivalent existe déjà dans antenne_radio/.

Tâches :
1. Ajouter les sources validées dans `antenne_radio/config/sources.yaml` avec tags et catégories configurés.
   - **Règle stricte d'activation** : N'ajouter avec `enabled: true` que les sources explicitement validées par un verdict favorable dans `antenne_radio/LEGAL_AUDIT.md`.
   - Si Nieman Storyboard ou Transom restent incertains lors de l'audit, les déclarer impérativement avec `enabled: false` ou les reporter.
2. Mettre à jour `antenne_radio/scripts/export/export_public.py` (ou le mapping d'attributions) pour associer ces sources aux identifiants d'attribution publics adéquats (`AUDITED_ATTRIBUTIONS`).
3. Lancer la suite de tests via `make test` pour valider l'intégrité de la configuration Yaml.
4. Lancer un run local contrôlé avec accès réseau via `make run` pour ingérer les nouveaux flux.
5. Vérifier `antenne_radio/data/logs/api.log` et `antenne_radio/data/logs/pipeline.log` afin de s'assurer qu'aucun avertissement ou timeout n'est levé.
6. Régénérer le JSON public via `make export-public` et vérifier l'incrément des items dans `static/antenne-radio/index.json`.

Vérification : Les nouveaux flux RSS sont correctement ingérés, normalisés et exportés dans le JSON public. `make test` passe à 100%.

Ajoute un bref handoff dans antenne_radio/codex_memoire_materielle.md :
- fichiers modifiés ;
- commandes lancées ;
- résultats réels ;
- limites restantes ;
- prochaine étape recommandée.
```

---

### Prompt 6 — Refonte du template Hugo `list.html` (No-JS & Grille Neo-Brutaliste)

**Périmètre :** Template d'affichage Hugo (`layouts/antenne-radio/list.html`).

```text
Objectif : Refondre l'affichage de l'antenne radio en remplaçant le vieux tableau par une grille de cartes neo-brutalistes premium dotée d'un fallback statique accessible sans JavaScript.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repère les chemins réels des fichiers avant d’en créer de nouveaux ;
- ne lance aucune ingestion live non demandée ;
- ne crée aucun cron ;
- ne crée aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores ou chemins locaux.
- Tous les chemins de l'antenne sont à résoudre depuis le dossier réel du module antenne_radio/. Ne jamais créer de doublon à la racine si un fichier équivalent existe déjà dans antenne_radio/.

Tâches :
1. Modifier `layouts/antenne-radio/list.html` pour créer un habillage neo-brutaliste premium (palette Catppuccin du site, bordures épaisses nettes et hard shadows franches).
2. Structurer le template avec :
   - Un en-tête dynamique affichant les compteurs de signaux et la date de dernière mise à jour.
   - Les contrôles de formulaire de filtrage (catégorie, source, langue, champ de saisie texte pour la recherche), tous équipés d'IDs uniques et descriptifs.
   - Un conteneur de grille flexible pour accueillir les cartes d'items générées dynamiquement en JS.
   - Une section dédiée aux attributions légales et éthiques claires en bas de page.
3. **Mettre en place le support No-JS (éco-conception)** : Insérer une balise `<noscript>` contenant une boucle Hugo standard (`range`) qui lit `static/antenne-radio/index.json` (au build via `readFile` / `transform.Unmarshal`) et génère sous forme purement statique et accessible les 50 premiers items pour les navigateurs n'exécutant pas JS.
4. **Optimiser les transitions CSS** :
   - L'effet de survol (hover) des cartes doit être ultra-fluide et limité aux translations ou ombres CSS.
   - **Interdiction formelle** de recourir à `transition: all`, des filtres graphiques complexes (`backdrop-filter`, `blur`, `drop-shadow`) ou `will-change` permanent. Limiter strictement la transition : `transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.2s cubic-bezier(0.4, 0, 0.2, 1)`.
5. Valider la construction avec le build Hugo global.

Vérification : Le build Hugo réussit. La page `/antenne-radio/` affiche une structure esthétique premium et le bloc `<noscript>` affiche les cartes statiques si JS est inactif.

Ajoute un bref handoff dans antenne_radio/codex_memoire_materielle.md :
- fichiers modifiés ;
- commandes lancées ;
- résultats réels ;
- limites restantes ;
- prochaine étape recommandée.
```

---

### Prompt 7 — JS Vanilla minimal pour les filtres et le rendu progressive en mémoire

**Périmètre :** Code JavaScript (`assets/js/antenne-radio.js`) et déclaration conditionnelle dans Hugo.

```text
Objectif : Implémenter le script JS vanilla autonome de filtrage multi-critère et de lazy rendering en mémoire.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repère les chemins réels des fichiers avant d’en créer de nouveaux ;
- ne lance aucune ingestion live non demandée ;
- ne crée aucun cron ;
- ne crée aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores ou chemins locaux.
- Tous les chemins de l'antenne sont à résoudre depuis le dossier réel du module antenne_radio/. Ne jamais créer de doublon à la racine si un fichier équivalent existe déjà dans antenne_radio/.

Tâches :
1. Créer le script `assets/js/antenne-radio.js` en JavaScript vanilla pur (strictement sans dépendance externe ni CDN).
2. Charger les données au démarrage : intercepter l'affichage JS, masquer le rendu HTML initial No-JS, et charger `static/antenne-radio/index.json` en mémoire.
3. Implémenter le filtrage multi-critère en mémoire (interrogation textuelle + catégorie + source + langue) en combinant les filtres via une logique "ET" stricte. Le DOM devient la cible de rendu et non la source de vérité.
4. **Gérer la pagination progressive (Lazy rendering)** :
   - Limiter l'affichage initial dans le DOM aux 50 premiers résultats correspondants.
   - **Règle stricte de pagination** : Ajouter un bouton explicite "Afficher plus de signaux" (`#load-more`). Ne pas implémenter d'infinite scroll dans cette v2.
5. **Respecter la discipline de légèreté** : Écrire un code hautement lisible, compact, bien structuré et pesant **moins de 8-12 Ko non minifié**.
6. Configurer Hugo pour que ce script soit chargé de manière **strictement conditionnelle** (uniquement sur la page `/antenne-radio/`) en l'injectant via `layouts/partials/functions/js-loader.html` ou directement dans le template de page.

Vérification : Le filtrage est instantané au clavier et au sélecteur, la pagination s'effectue sans saccade par lots de 50, et le JS n'est chargé sur aucune autre page du site.

Ajoute un bref handoff dans antenne_radio/codex_memoire_materielle.md :
- fichiers modifiés ;
- commandes lancées ;
- résultats réels ;
- limites restantes ;
- prochaine étape recommandée.
```

---

### Prompt 8 — Partage de filtres (Deep-linking) et polish UX sobre

**Périmètre :** Améliorations JS (`assets/js/antenne-radio.js`) et styles CSS associés.

```text
Objectif : Finaliser l'expérience utilisateur par l'intégration de la synchronisation d'URL (deep-linking), d'une barre de jetons actifs et d'un état vide léger et accessible, sans animations lourdes.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repère les chemins réels des fichiers avant d’en créer de nouveaux ;
- ne lance aucune ingestion live non demandée ;
- ne crée aucun cron ;
- ne crée aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores ou chemins locaux.
- Tous les chemins de l'antenne sont à résoudre depuis le dossier réel du module antenne_radio/. Ne jamais créer de doublon à la racine si un fichier équivalent existe déjà dans antenne_radio/.

Tâches :
1. **Synchronisation URL (Deep Linking)** :
   - Écrire la logique JS pour lire les paramètres d'URL (`window.location.search`) au chargement et pré-remplir les inputs et sélecteurs de filtres (ex: `?q=podcast&cat=revue&lang=fr`).
   - Mettre à jour dynamiquement l'URL à chaque modification de filtre en utilisant `history.replaceState` pour que l'état soit instantanément partageable ou mémorisable.
2. **Barre de filtres actifs (Active Filters Bar)** :
   - Créer un conteneur `#active-filters-bar` affichant dynamiquement chaque critère actif sous forme de badge cliquable doté d'une croix SVG pour suppression.
   - Ajouter un bouton de réinitialisation complète (`#clear-filters`) pour restaurer l'état initial des sélecteurs, vider l'URL et rafraîchir l'affichage en mémoire.
3. **Animations ultra-sobres & État vide léger** :
   - **Règle stricte d'état vide** : Créer un état vide simple, élégant et léger comprenant un message explicite, une petite icône SVG inline ou des formes CSS minimales, et un bouton de réinitialisation. L'animation optionnelle est autorisée uniquement si elle reste triviale et désactivable.
   - **Respect de l'accessibilité physique** : Respecter strictement la directive CSS `prefers-reduced-motion` pour toute transition ou micro-animation.
   - **Aucun squelette de chargement (No Skeletons)** : Ne pas introduire de skeletons pour préserver la légèreté.
4. **Accessibilité (A11y)** :
   - Garantir des focus visibles (:focus-visible) avec des bordures géométriques nettes pour la navigation au clavier sur les filtres et badges.
   - Ajouter un attribut `aria-live="polite"` sur le conteneur du compteur dynamique d'affichage pour les lecteurs d'écran.

Vérification : Le copier/coller d'une URL filtrée recharge fidèlement l'état initial. L'état vide s'affiche avec sobriété. L'accessibilité clavier est valide.

Ajoute un bref handoff dans antenne_radio/codex_memoire_materielle.md :
- fichiers modifiés ;
- commandes lancées ;
- résultats réels ;
- limites restantes ;
- prochaine étape recommandée.
```

---

### Prompt 9 — Run final complet, validation et handoff v2

**Périmètre :** Tests d'intégration, vérification de non-fuite et mise à jour de la documentation v2 globale.

```text
Objectif : Effectuer la recette technique complète de la v2 de l'antenne radio, s'assurer de l'absence totale de fuite d'informations sensibles et geler le périmètre avant handoff pour la v3 académique.

Avant toute modification :
- lance git status --short ;
- lis docs/AGENTS.md ;
- lis antenne_radio/codex_memoire_materielle.md ;
- repère les chemins réels des fichiers avant d’en créer de nouveaux ;
- ne lance aucune ingestion live non demandée ;
- ne crée aucun cron ;
- ne crée aucun auto-commit ;
- ne publie jamais raw, logs, abstracts, scores ou chemins locaux.
- Tous les chemins de l'antenne sont à résoudre depuis le dossier réel du module antenne_radio/. Ne jamais créer de doublon à la racine si un fichier équivalent existe déjà dans antenne_radio/.

Tâches :
1. Lancer l'ingestion et l'orchestration complète : `make test` puis `make run`.
2. Lancer l'export public via `make export-public` pour rafraîchir `static/antenne-radio/index.json`.
3. Exécuter un build Hugo final minifié complet et s'assurer qu'aucun warning n'est retourné.
4. **Vérification anti-fuite rigoureuse** : Effectuer des scans via `grep`/`ripgrep` sur `static/antenne-radio/index.json` et sur le répertoire de sortie `public/antenne-radio/` pour garantir l'absence totale des motifs interdits : `raw`, abstracts, logs, notes privées, chemins locaux, scores internes ou explications lexicales.
5. Mettre à jour la documentation d'architecture et d'utilisation :
   - `antenne_radio/README.md` (schéma public v1, commandes et variables).
   - `antenne_radio/01_RESSOURCES_SUIVIES.md` (statuts RSS v2).
   - `antenne_radio/LEGAL_AUDIT.md` (verdicts RSS confirmés).
   - `docs/CHANTIERS.md` (marquer les chantiers v2 terminés, lister les reports).
6. Mettre à jour `antenne_radio/codex_memoire_materielle.md` avec le bilan final et la section "v3 académique possible" prête à être exécutée dans un lot autonome ultérieur.

Vérification : Tout build est OK, 0 fuite détectée, tests passent à 100%. La v2 est close, stable, validée localement et prête à être publiée/mergée selon le workflow Git habituel.

Ajoute un bref handoff dans antenne_radio/codex_memoire_materielle.md :
- fichiers modifiés ;
- commandes lancées ;
- résultats réels ;
- limites restantes ;
- prochaine étape recommandée.
```

---

## Résumé des fichiers concernés par prompt (v2)

| Prompt | Fichiers principaux impactés |
|---:|---|
| 1 | `.github/workflows/tests.yml` |
| 2 | `config/_default/hugo.yaml` (ou `hugo.yaml`), `layouts/partials/sidebar.html`, `layouts/partials/mobile-nav.html` |
| 3 | `antenne_radio/scripts/export/export_public.py`, `antenne_radio/tests/test_export_public.py`, `static/antenne-radio/index.json` |
| 4 | `antenne_radio/LEGAL_AUDIT.md`, `antenne_radio/01_RESSOURCES_SUIVIES.md` |
| 5 | `antenne_radio/config/sources.yaml`, `antenne_radio/scripts/export/export_public.py`, `antenne_radio/data/normalized/db.json` |
| 6 | `layouts/antenne-radio/list.html` |
| 7 | `assets/js/antenne-radio.js`, `layouts/partials/functions/js-loader.html` (ou layout) |
| 8 | `assets/js/antenne-radio.js`, `layouts/antenne-radio/list.html` |
| 9 | `antenne_radio/README.md`, `antenne_radio/01_RESSOURCES_SUIVIES.md`, `antenne_radio/LEGAL_AUDIT.md`, `docs/CHANTIERS.md`, `antenne_radio/codex_memoire_materielle.md` |

---

## Garde-fous et règles opérationnelles v2
- **Déclenchements CI** : Uniquement via `workflow_dispatch`. Pas de mise à jour invisible ou automatique.
- **Règles Hugo** : Le build Hugo lit simplement les données compilées dans `static/antenne-radio/index.json`. Le build ne doit jamais relancer l'ingestion.
- **Limitation d'écriture** : Les scripts d'export privés (`export_obsidian.py` et `export_csl.py`) ne doivent jamais modifier `db.json` sans commande ou argument CLI explicite.
- **Idempotence** : `make test` doit être exécuté et passer avec succès avant de clore chaque prompt.

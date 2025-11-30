# System Context : Architecture Hugo Blox (Dark Mode & Clean Code)

**Dernière mise à jour consolidée : 23/11/2025**
**Stack :** Hugo Extended | Tailwind CSS v4 | Supabase | No JS | Catppuccin Theme (Dark Mode Only)

## 1. Philosophie Architecturale & Règles Globales

* **Approche :** Maintainability First. Pas de "hacks" fragiles.
* **Dark Mode Strict :** Le site est conçu exclusivement en mode sombre. Utilisation intensive de la palette Catppuccin (`text-ctp-subtext0`, `bg-ctp-surface0`, etc.).
* **Separation of Concerns :**
    * **Layouts** = Structure DOM & Logique d'affichage.
    * **Markdown** = Contenu pur ("La Chair"). **Interdiction stricte de `<div>` ou HTML brut dans le Markdown.**
    * **Front Matter** = Métadonnées de pilotage (Icones, Couleurs, Logique de tri).

---

## 2. Structure Maîtresse (Layouts)

### A. Le Squelette (`layouts/_default/baseof.html`)
Le parent de toutes les pages. Il orchestre la mise en page globale "Sidebar".
* **Mounts :**
    * `partials/sidebar.html` (Desktop, Sticky Left).
    * `partials/mobile-nav.html` (Mobile, Fixed Bottom, style "Glassmorphism").
* **Block Main :** Conteneur dynamique pour le contenu spécifique.

### B. Navigation & UX
* **Sidebar (Desktop) :** Navigation latérale gauche. Utilise `<details>`/`<summary>` pour les sous-menus (arborescence sans JS). Footer "Schrödinger" intégré.
* **Mobile Nav :** Barre fixe en bas (`bottom-0`). Accès rapides + Bouton Home.
* **Styling :** `backdrop-blur-xl` et `bg-ctp-surface0/40` pour la profondeur.

---

## 3. Typologie des Pages & Responsabilités

### A. Homepage "Hybride" (`layouts/index.html`)
* **Concept :** Architecture inversée "Layout-First".
* **Responsabilité Layout :** Contient TOUTE la structure riche (Hero, Grilles, Appels de scripts). C'est ici que vivent les widgets complexes.
* **Responsabilité Markdown (`content/_index.md`) :** Ne contient *que* le texte introductif.
* **Injection :** Le Layout appelle `{{ .Content }}` dans un conteneur prose sécurisé.
* **Composants Exclusifs :**
    * `partials/widgets/dom-card.html` : Bouton flottant (👾) et logique de bavardage aléatoire.

### B. La "Machine à Cartes" (`layouts/_default/list.html`)
Template générique unifié pour les sections standards (ex: "Ondes & Pixels").
* **Logique Duale :**
    1.  **Mode Manuel :** Si `params.items` existe dans le Front Matter, itère dessus.
    2.  **Mode Automatique :** Sinon, itère sur `.Pages`.
* **Rendu :** Appelle `partials/cards/link-card.html`.

### C. Sections Spécialisées (Custom Layouts)
* **Rhizome (`layouts/rhizome-curieux/list.html`) :**
    * **Logique :** Interface "Interne (Bulb) vs Externe (Spore)".
    * **Data Source :** Utilise `partials/functions/get-rhizome-items.html` (ETL) pour normaliser les pages Markdown et les liens externes YAML/Data.
    * **Visuel :** Utilise `partials/cards/rhizome-card.html` (Rotation aléatoire, bordures spécifiques).
* **Patafoin (`layouts/patafoin/list.html`) :**
    * **Nature :** Mini-SPA (Single Page App).
    * **Backend :** Connecté à **Supabase**.
    * **Rôle :** Gestion des topics du forum (CRUD via JS Vanilla, pas de rechargement Hugo).

---

## 4. Composants & Design System (Partials)

### A. Cartes (Atomes)
* `partials/cards/link-card.html` : Carte standard (Titre, Sous-titre, Icône). Utilisée par défaut.
* `partials/cards/rhizome-card.html` : Carte contextuelle avec entropie visuelle (rotations légères) pour la section Rhizome.

### B. Widgets & Pipeline
* `partials/css.html` : Pipeline Hugo Pipes. Compile `assets/css/main.css` via le binaire Tailwind v4 (JIT).
* **Render Hooks (`layouts/_markup/`) :**
    * `render-link.html` : **Wiki Links 2.0**. Supporte les liens relatifs (`../`), corrige les bugs de résolution des Page Bundles (index.md) et sécurise les liens externes.

---

## 5. Données & APIs Statiques

Hugo génère des fichiers JSON consommés par le JavaScript client (Hydratation).
* `home.json` (Output `Random`) : API contenant tous les permaliens pour la fonction "Article Aléatoire" (🌀).
* `landing/list.json` (Output `Almanach`) : Index des données éphémérides pour le script `PataphysicalDate.js`.

---

## 6. Standards de Contenu (Front Matter)

Pour garantir le fonctionnement de la "Machine à Cartes" et du styling :

```yaml
---
title: "Mon Titre"
date: 2025-11-23
icon: "🚀"             # Emoji obligatoire pour les cartes
color: "mauve"         # Token couleur Catppuccin (mauve, peach, teal, etc.)
description: "Court résumé pour la carte."

---

## 7. Pipeline Frontend & Stratégie CSS (Tailwind v4 Alpha)

Architecture spécifique établie pour résoudre le bug critique de **"Color Loss / CSS Purge" en Production (Netlify)**, causé par une incompatibilité entre le moteur Tailwind v4 et le pipeline de minification Hugo.

* **Symptôme Résolu :** Disparition des styles `.prose-catppuccin` (couleurs, typo) sur les articles en Prod, malgré un fonctionnement correct en Local.
* **Contrainte Technique (Minification) :**
    * Le minifieur standard de Hugo (`tdewolff`) corrompt la syntaxe native **CSS Nesting** (`& :where(...)`) utilisée par Tailwind v4.
    * **Stratégie :** Désactivation explicite du pipe `| minify` dans `layouts/partials/css.html` pour la production. On délègue l'optimisation à Tailwind et on ne garde que le Fingerprinting (`integrity`) côté Hugo.
* **Hygiène du fichier source (`assets/css/main.css`) :**
    * Règle W3C stricte appliquée pour éviter le crash du parser CSS en Prod : Les `@import` (fontes, tailwind) doivent être **absolument les premières lignes**.
    * Tout commentaire ou `@plugin` avant les imports invalide le fichier aux yeux des parseurs stricts.
* **Mécanisme de Secours (Safelist) :**
    * Maintien de `layouts/partials/debug/safelist.html` (non rendu) pour forcer le scanner JIT à détecter les classes de couleurs dynamiques, sécurisant le build contre les "faux négatifs" du scanner.

## 📦 MODULE: RHIZOME (V6 - ORBITAL PHYSICS)
**Date de mise à jour :** 26/11/2025
**Dépendances :** D3.js v7, Hugo Pipes, Partial `get-rhizome-items.html`

### 1. Philosophie : "Noyau & Cytoplasme"
L'architecture verticale a été abandonnée pour une physique orbitale concentrique (Horror Vacui).
- **Le Noyau (Roots) :** Agrégat central dense (Rayon 0px). Contenu interne (`internal`) relié par un maillage solide (Mesh).
- **L'Orbite (Spores) :** Ceinture périphérique flottante (Rayon ~400px). Liens externes (`external`) sans connexions visibles.

### 2. Architecture des Données
Les données sont normalisées par un partial avant d'être exposées en JSON local au sein de la section `rhizome-curieux`.

| Type | Source | ID | Rôle Physique |
| :--- | :--- | :--- | :--- |
| **Internal** | Pages de la section | `int-{UniqueID}` | Attracteur Central (0,0). |
| **External** | FrontMatter (`params.items`) | `ext-{index}` | Attracteur Orbital (r=400). |

### 3. Guide d'Utilisation
* **Ajout de Contenu :**
    * *Racine :* Créer un fichier Markdown dans `content/rhizome-curieux/` (ou dossier associé).
    * *Spore :* Ajouter l'URL et le titre dans le FrontMatter `items` de la page section (`_index.md`).
* **Tuning Physique :**
    * Modifier `CONFIG` dans `assets/js/rhizome-engine.js` (Rayon d'orbite, force de répulsion).

### 4. Cartographie des Fichiers (Source of Truth)
* **Logique JS :** `assets/js/rhizome-engine.js` (Moteur physique).
* **Normalisation :** `layouts/partials/functions/get-rhizome-items.html` (Typage & Couleurs).
* **Template UI :** `layouts/rhizome-curieux/list.html` (Conteneur Canvas & Stack UI).
* **Endpoint Data :** `layouts/rhizome-curieux/list.json` (Structure: `{ nodes: [], meta: {} }`).

## Patafoin forum Supabase

🛠️ ARCHITECTURE LOG: MODULE PATAFOIN (v3.2)

1. Modèle de Données (Supabase)

    Séparation Strictes :

        topics (Conteneur) : id, title, created_at.

        posts (Contenu & Hiérarchie) : id, topic_id, parent_id, content, author.

    Concept du "Root Post" : Le corps d'un sujet est techniquement le premier post (parent_id: null) associé au topic_id.

2. Logique d'Écriture (JS)

    Création Atomique : Séquence obligatoire await createTopic() ➝ await createFirstPost(topic_id, parent: null).

    Réponses : Insertion standard avec parent_id ciblant le post parent (ou le Root Post).

3. Algorithme de Lecture & Hydratation

    Problème Résolu : "Paradoxe de l'Orphelin" (les réponses au sujet principal disparaissaient).

    Stratégie de Rendu :

        Fetch topics + Fetch posts.

        Extraction du rootPost (celui sans parent) pour injecter son contenu dans l'affichage du Topic.

        Fix Critique : La fonction récursive buildHierarchy(posts, relativeRootId) prend l'ID du Root Post comme contexte pour rattacher correctement les réponses de premier niveau.

4. UI/UX (Terminal Style)

    Palette : Catppuccin Mocha (assets/css/main.css).

    Curseur : "Soft Ghost" (Underscore gris, animation lente) pour éviter la fatigue visuelle.

    Indentation : "Rainbow Depth" (couleur de ligne changeant modulo 6 selon la profondeur).

## 🔧 PIPELINE UPDATE: JS & API (27/11/2025)

**1. Gestion des Assets JS (Hugo Pipes)**
* **Source of Truth :** Tous les scripts résident désormais dans `assets/js/` (et non plus `static/`).
* **Mécanisme :** Utilisation exclusive du partial `functions/js-loader.html`.
    * *Features :* ESBuild (Target ES2020), Minification (Prod), Fingerprinting (Cache).
* **Injection :**
    * *Global :* `baseof.html` (avant `</body>`).
    * *Scoped :* Via le bloc `{{ define "scripts" }}` dans les layouts spécifiques (Rhizome, Patafoin).

**2. Architecture API (JSON)**
* **Fix Config :** `outputFormats` (RANDOMIZER, RHIZOME) correctement indentés dans `hugo.yaml`.
* **Outputs Validés :**
    * `RANDOMIZER` -> `articles-aleatoires.json` (Home).
    * `RHIZOME` -> `index.json` (Section Rhizome).

## 8. Performance Standard & Esthétique "Solid State" (Mise à jour v5 - 30/11/2025)

**Changement de Paradigme :** Abandon total du "Glassmorphism" au profit d'une UI "Solid State" (Brute/Instrument de Labo).
**Objectif :** 60FPS constants, zéro lag lors des reflows (resize sidebar), clarté visuelle maximale.

* **Règles CSS Strictes :**
    * 🚫 **INTERDICTION :** `backdrop-filter`, `blur()`, ombres diffuses complexes, mélange de couleurs Alpha (rgba) excessif.
    * ✅ **OBLIGATION :** Fonds opaques (`bg-ctp-mantle`, `bg-ctp-surface0`), Bordures nettes (`border-ctp-surface1`), Ombres portées courtes ("Hard shadows").
    * **Animations :** Exclusivement limitées aux propriétés *composite-only* : `transform` et `opacity`. Pas de transition sur `width`, `height` ou `margin` (sauf layout grid global).
* **Design System :**
    * L'esthétique repose sur la hiérarchie des couleurs Catppuccin solides et non sur la profondeur de champ.
    * Les composants doivent ressembler à des instruments physiques (solides, tactiles) plutôt qu'à des vitres flottantes.

---
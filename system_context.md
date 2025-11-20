System Context: Presque Quelque Chose

Dernière Mise à jour : 20 Novembre 2025
Architecture : Hugo Native + Tailwind CSS v4 (Hybrid Hugo Blox)
Statut : ✅ Validé & Robuste
Philosophie : "Native Pure", JIT Synchronisé, Zero-Config JS.

1. Stack Technique & Versions

Générateur : Hugo Extended (v0.128.0+ requis).

Moteur CSS : Tailwind CSS v4 (via CLI Binaire).

Framework Base : Hugo Blox (Customisé).

Package Manager : pnpm (v10.x).

Langage Template : Go Template.

2. Architecture : "Native Tailwind Integration"

Ce projet suit l'architecture Standard 2025. Il élimine totalement la dépendance à Node.js/PostCSS pour la compilation des styles en production.

2.1 Le Pipeline JIT (Boucle Critique)

L'architecture repose sur une synchronisation précise pour éviter les "Race Conditions" :

Génération : Hugo compile le HTML et écrit les classes utilisées dans hugo_stats.json.

Détection : Le fichier hugo_stats.json est monté virtuellement dans assets/watching/.

Compilation : Tailwind (via la directive @source dans le CSS) détecte le changement et régénère les styles instantanément.

3. Règles d'Or (Do's & Don'ts)

🟢 OBLIGATOIRE (Do's)

Point d'entrée unique : Tout le CSS part de assets/css/main.css.

Imports CSS : Les styles personnalisés doivent être gérés via @import ou @plugin CSS, jamais via SASS/SCSS.

Hugo Stats : Le fichier hugo_stats.json est la source de vérité absolue.

Classes Complètes : Toujours écrire les noms de classes en entier dans le HTML (ex: bg-red-500). Jamais de concaténation dynamique (bg-{{ $color }}).

🔴 INTERDIT (Don'ts)

Pas de PostCSS Legacy : Ne jamais réintroduire postcss.config.js ou resources.PostCSS.

Pas de dossier Static : Le CSS source ne doit jamais être dans static/. Il doit vivre dans assets/ pour être traité par Hugo Pipes.

Pas de tailwind.config.js : La configuration v4 se fait exclusivement en CSS (@theme).

4. Structure & Responsabilités

Vue Arborescente

.
├── assets/
│   ├── css/
│   │   └── main.css           <-- SOURCE DE VÉRITÉ (@import "tailwindcss", @theme)
│   └── watching/              <-- Dossier virtuel (Mount) pour la synchro JIT
├── config/
│   └── _default/
│       └── hugo.yaml          <-- Config Build (writeStats: true)
├── layouts/
│   ├── _default/
│   │   └── baseof.html        <-- Layout Maître (Appelle css.html)
│   └── partials/
│       └── css.html           <-- Pipeline Hugo Pipes (css.TailwindCSS)
├── hugo_stats.json            <-- Artefact de build (Ignoré par Git)
└── package.json               <-- Sert uniquement à installer le binaire CLI


5. Configuration Critique

A. Montage des Modules (hugo.yaml)

build:
  writeStats: true # INDISPENSABLE

module:
  mounts:
    - source: assets
      target: assets
    - source: hugo_stats.json
      target: assets/watching/hugo_stats.json  # Le "Hack" officiel pour le JIT


B. Configuration CSS (main.css)

C'est ici que réside le Design System "Pastel".

@import "tailwindcss";

/* Sources surveillées par le moteur JIT */
@source "../../layouts/**/*.html";
@source "../../content/**/*.md";
@source "../watching/hugo_stats.json";

@theme {
  /* Palette Pastel Custom */
  --color-pastel-bg:   #fdfbf7;
  --color-pastel-text: #334155;
  --color-pastel-a:    #8b5cf6;
  /* ... */
}


6. Workflow de Développement

Commandes

Lancer le serveur :
pnpm dev
(Alias pour hugo server --disableFastRender)
Note : --disableFastRender assure le rafraîchissement correct du CSS lors des modifications de structure.

Construire pour la Prod :
pnpm build
(Alias pour hugo --minify)

Dépannage (Troubleshooting)

Styles cassés ? Vérifiez que hugo_stats.json existe à la racine. Si non, vérifiez hugo.yaml.

Erreur de build ? Assurez-vous que vous n'avez pas de node_modules orphelins contenant d'anciennes versions de PostCSS qui entreraient en conflit.

Design System non appliqué ? Vérifiez que la classe .prose-pastel est bien présente sur le conteneur <article> dans baseof.html.

7. Git Ignore

Ces fichiers ne doivent jamais être versionnés :

hugo_stats.json

resources/

public/

node_modules/

.hugo_build.lock

Architecture auditée et validée le 20/11/2025.

---
Mise à Jour : 20 Novembre 2025 (Update 2)
Objet : Refonte Homepage & Architecture Hybride
Statut : ✅ En Production
---

8. Architecture Spécifique : Homepage "Hybride"

Problème Résolu :
L'injection de widgets HTML complexes (Compteurs, Grilles) directement dans le Markdown (`content/_index.md`) causait des conflits de rendu (Goldmark transformant le HTML en blocs de code) et rendait la maintenance illisible.

Solution : Le Modèle "Layout-First"
Pour la page d'accueil uniquement, l'architecture est inversée :
- Layout (`layouts/index.html`) : Contient toute la structure structurelle (Hero, Grille, appels de scripts). C'est le "Squelette".
- Content (`content/_index.md`) : Ne contient que le texte éditorial (Intro). C'est la "Chair".
- Injection : Le Layout appelle `{{ .Content }}` à un endroit précis et sécurisé.

9. Standards de Composants (Design System)

A. Widgets & Partials
- Règle : Tout composant interactif (JS + HTML) doit être un Partial, pas un Shortcode, s'il est utilisé dans un layout dur.
- Emplacement : `layouts/partials/widgets/` (ex: `compteur.html`).
- Style : Utilisation de `bg-ctp-surface0/40` + `backdrop-blur-md` pour l'effet de profondeur Catppuccin.

B. Header "Bold"
- Typographie : Logo en `text-3xl font-black`.
- Navigation : Style "Pill" (`rounded-full`) au survol pour une affordance moderne.
- Verre : `backdrop-blur-xl` obligatoire pour la lisibilité sur le scroll.

C. Surcharges CSS "Brutales" (JIT)
Dans certains contextes (comme le Hero), nous devons forcer le contraste contre les réglages par défaut de `.prose`.
Méthode validée : Sélecteurs arbitraires Tailwind.
Exemple : `[&>p]:text-ctp-subtext0` force la couleur de tous les paragraphes enfants directs, ignorant la cascade CSS standard.

10. Arborescence Mise à Jour

layouts/
├── index.html                  <-- Structure Maître Homepage
└── partials/
    ├── header.html             <-- Version "Bold & Chunky"
    └── widgets/
        └── compteur.html       <-- Composant isolé (ex-Shortcode)

---
Mise à Jour : 20 Novembre 2025 (Update 3)
Objet : Harmonisation des Sections & Réparation Wiki Links
Statut : ✅ Validé
---

11. Standardisation des Listes (Architecture Hybride)

A. Le Template Maître (`layouts/_default/list.html`)
Une "Machine à Cartes" unifiée qui remplace les layouts spécifiques du thème. Elle gère deux modes :
- Mode Manuel : Itère sur `params.items` défini dans le Front Matter (ex: Rhizome Curieux).
- Mode Automatique : Itère sur `.Pages` si aucun item n'est défini (ex: Ondes & Pixels).
- Design DRY : Tout le visuel des cartes est isolé dans `partials/cards/link-card.html`.

B. Nettoyage du Markdown (Clean Code)
- Suppression totale des blocs `<div>` HTML brut dans les fichiers `content/**/*.md`.
- Adoption de métadonnées standardisées dans le Front Matter pour piloter l'affichage :
  - `icon`: Emoji représentant l'entrée.
  - `color`: Nom du token couleur Catppuccin (ex: "mauve", "peach", "teal") pour la thématisation des bordures et survols.

12. Moteur de Liens Internes (Wiki Links 2.0)

Refonte du Render Hook `layouts/_markup/render-link.html` :
- Correction du bug de résolution sur les Page Bundles (conflits `index.md`).
- Support natif des liens relatifs (ex: `../mon-article`).
- Sécurisation du code (remplacement de `.IsFragment` par `strings.HasPrefix`).

13. Décision Stratégique : Pivot Navigation (À venir)
- Constat : Le Header horizontal limite la représentation de la profondeur du site ("Rhizome").
- Décision : Transition validée vers une **Sidebar Latérale (Navigation Gauche)**.
- Contrainte technique : Utilisation de `<details>`/`<summary>` pour une arborescence sans JavaScript.


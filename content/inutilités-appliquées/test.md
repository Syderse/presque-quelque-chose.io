---
title: "ÉTALON V2 : RAPPORT DE CALIBRAGE DES COULEURS ET POLICES"
date: 2025-11-15
summary: "Ceci est le test v2 pour vérifier la solution radicale. il teste à la fois les variables css (pour les composants) et les classes tailwind (pour le contenu)."
---

### 1. L'ADN de votre projet (La Stack)

Ce n'est pas un site Hugo "classique". Votre projet est une combinaison de technologies modernes, ce qui le rend puissant mais aussi complexe à déboguer :

- **Il est piloté par Hugo Modules** : Ce n'est pas un thème Git standard. Le style et les fonctionnalités (comme `blox-tailwind`) sont gérés par le système de modules de Hugo. Nous l'avons confirmé en utilisant la commande `hugo mod vendor` pour forcer la création du dossier `_vendor`.
    
- **Il exige Hugo "Extended"** : Le thème utilise des fonctions avancées de traitement d'image (`.Process` pour créer des `.webp`). Cela a causé nos premiers "crashs", résolus par l'installation manuelle de la version **`+extended`** de Hugo.
    
- **Il utilise Tailwind v4** : C'est la découverte la plus récente. Contrairement à Tailwind v3, cette version est conçue pour être pilotée _directement par Hugo_ lors de l'exécution de `hugo server`. Il n'y a pas de script `pnpm dev` séparé pour Tailwind.
    

---

### 2. Le diagnostic du problème actuel

Vos styles (polices et couleurs) ne s'appliquent pas.

Le "pont" entre vos fichiers de configuration (où vous exprimez vos choix de design) et le fichier CSS final (ce que le navigateur lit) est rompu.

Voici les pièces de ce pont, dans l'ordre :

1. **Votre intention (les sources)** :
    
    - `config/_default/params.yaml` (pour les polices Google `Playfair Display`, etc.)
        
    - `assets/css/themes/custom.css` (pour vos couleurs 'Pataphysiques)
        
2. **Le "cerveau" de Tailwind (l'intermédiaire)** :
    
    - `tailwind.config.js` (Ce fichier que nous avons créé).
        
3. **Le "traducteur" (le plugin)** :
    
    - Le fichier `plugin.js` de Hugo Blox (que nous avons placé dans `_vendor` puis tenté d'appeler depuis `tailwind.config.js`).
        

**Le point de défaillance actuel** est que le `tailwind.config.js` ne parvient pas à charger le plugin "traducteur" depuis le dossier `_vendor`. La chaîne est brisée à cet endroit précis.

Cette chasse aux dépendances rappelle d'ailleurs le célèbre problème des "sept ponts de Königsberg" : une balade n'est possible que si un chemin existe.

---

### 3. Les commandes vitales (Votre boîte à outils)

Pour faire fonctionner ce projet spécifique, trois commandes sont essentielles :

- **L'installation (une seule fois)** : `pnpm install` _(Installe les dépendances JavaScript, comme Tailwind lui-même)._
    
- **L'installation des modules Hugo (une seule fois)** : `hugo mod vendor` _(Copie les thèmes/plugins "cachés" dans le dossier `_vendor` pour que `tailwind.config.js` puisse les trouver)._
    
- **Le lancement du serveur (au quotidien)** : `hugo server -D --baseURL "/" --bind "0.0.0.0"` _(C'est la commande la plus robuste. Le `pnpm dev` de votre projet n'est pas suffisant car il ne gère pas le problème de `baseURL` dans Codespaces)._

***cat config/_default/params.yaml assets/css/themes/custom.css tailwind.config.js config/_default/module.yaml***

### 4. Comment fonctionnent les couleurs dans notre cas

## 📋 Mémo Interne : Débogage Thème Hugo Blox (La Solution Radicale v3.1)

Date : 15 novembre 2025

Auteur : Assistant création site Hugo Blox

Sujet : Échec de l'application du thème custom.css (couleurs/polices) malgré des fichiers de configuration valides.

---

### 1. Diagnostic de l'Échec

Le "pont" standard de Hugo Blox est défaillant.

- **Le Pont Standard :** `params.yaml` (polices) + `custom.css` (`@theme`) -> `tailwind.config.js` (via `withHugoBlox`) -> CSS final.
    
- **Symptômes :**
    
    1. Les polices de `params.yaml` ne s'appliquent pas.
        
    2. Les couleurs de `@theme` dans `custom.css` ne s'appliquent pas.
        
    3. Le fond de la page reste blanc (le défaut), les composants sont bleus (le défaut).
        
    4. Des erreurs `Unknown at rule @theme` sont levées, prouvant que `custom.css` est lu comme du CSS normal et non traité par le plugin.
        
- **Cause Probable :** Le plugin `withHugoBlox` échoue silencieusement. Cause suspectée : corruption de fichier (ex: "espaces insécables") ou échec d'initialisation.
    

### 2. La Solution Radicale v3.1 (L'Unification)

**Principe :** Abandonner totalement le pont hanté (`withHugoBlox`, `@theme`, `params.yaml` pour les polices) et centraliser 100% de la configuration du design (polices _et_ couleurs) dans un seul fichier : `tailwind.config.js`.

> Ce fichier devient l'unique source de vérité, générant à la fois les **classes utilitaires** (ex: `bg-primary-500`) et les **variables CSS** (ex: `var(--color-primary-500)`) nécessaires au thème.

---

### 3. Procédure Étape par Étape

#### Étape 1 : Nettoyer `config/_default/params.yaml`

Le fichier est vidé de toute responsabilité de design.

- **Supprimer** l'intégralité de la section `fonts:`.
    
- **Conserver** `appearance: { color: custom }` pour s'assurer que `custom.css` est bien chargé.
    

#### Étape 2 : Simplifier `assets/css/themes/custom.css`

Ce fichier ne sert plus qu'à importer les polices et à appliquer des patchs.

- **Supprimer** tous les blocs `@theme { ... }`.
    
- **Supprimer** tous les blocs `:root { ... }` et `[data-theme='dark'] { ... }` (qui définissent les variables de couleur).
    
- **Ajouter** l'importation manuelle des Google Fonts en haut du fichier.
    
    CSS
    
    ```
    @import url('https://fonts.googleapis.com/css2?family=...&display=swap');
    ```
    
- **Conserver** uniquement les patchs CSS 'pataphysiques' (ex: `h1 { text-transform: lowercase; }`).
    

#### Étape 3 : Centraliser dans `tailwind.config.js` (Le Cœur)

C'est ici que toute la logique réside.

1. **Importer le plugin Tailwind de base :**
    
    JavaScript
    
    ```
    const plugin = require('tailwindcss/plugin');
    ```
    
2. **Définir les palettes** comme des constantes JavaScript (sans guillemets dans les noms de constantes) :
    
    JavaScript
    
    ```
    const pataphysiqueColors = {
      background: '#fbf5e9',
      primary: { 50: '...', 100: '...' /* etc. */ },
      secondary: { 50: '...', 100: '...' /* etc. */ }
    };
    
    const pataphysiqueDarkColors = {
      background: '#3a3a3a',
      primary: pataphysiqueColors.primary, // Réutiliser si inchangé
      secondary: { 50: '...', 100: '...' /* etc. */ }
    };
    ```
    
3. **Configurer `module.exports` :**
    
    JavaScript
    
    ```
    module.exports = {
      content: [
        './layouts/**/*.html',
        './content/**/*.{md,html}',
        './hugo_stats.json',
      ],
    
      theme: {
        extend: {
          // 3a. Définir les polices pour les classes Tailwind
          fontFamily: {
            heading: ['Playfair Display', 'serif'],
            body: ['EB Garamond', 'serif'],
            code: ['Special Elite', 'monospace'],
          },
          // 3b. Définir les couleurs pour les classes Tailwind
          colors: pataphysiqueColors,
        },
      },
    
      // 3c. LE PLUGIN UNIFICATEUR
      plugins: [
        plugin(function ({ addBase, theme }) {
          // Fonction pour "aplatir" l'objet de couleurs
          function extractColorVariables(colorObject, colorGroup = '') {
            return Object.keys(colorObject).reduce((vars, colorKey) => {
              const value = colorObject[colorKey];
              const newKey = colorGroup ? `${colorGroup}-${colorKey}` : colorKey;
              if (typeof value === 'string') {
                vars[`--color-${newKey}`] = value;
              } else if (typeof value === 'object') {
                Object.assign(vars, extractColorVariables(value, newKey));
              }
              return vars;
            }, {});
          }
    
          // Générer les variables CSS pour le Mode Clair
          addBase({
            ':root': extractColorVariables(theme('colors')),
          });
    
          // Générer les variables CSS pour le Mode Sombre
          addBase({
            "[data-theme='dark']": extractColorVariables(pataphysiqueDarkColors),
          });
        }),
      ],
    };
    ```
    

### 4. Résultat

Cette configuration résout la "scission 'pataphysique". `tailwind.config.js` génère les variables (`:root`) que les composants du thème (comme les boutons et le fond de page) utilisent, _et_ il génère les classes (`bg-primary-500`) que le contenu markdown personnalisé utilise.

**Rituel obligatoire :** `rm -rf resources` après application.
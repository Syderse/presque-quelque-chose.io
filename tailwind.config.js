/*
  SOLUTION RADICALE v4.0 - LA CORRUPTION DU PLUGIN
  Nous cessons de nous battre avec custom.css et injectons
  nos couleurs 'Obsidian' directement dans le plugin @tailwindcss/typography.
*/

// 1. Importer les 'plugins' de base
const plugin = require('tailwindcss/plugin');
const typography = require('@tailwindcss/typography'); // <-- AJOUTÉ

// 2. Définir nos couleurs 'pataphysiques (inchangé)
const pataphysiqueColors = {
  // Fonds & Bordures (Mode Clair)
  background: '#fbf5e9',
  'dark-background': '#3a3a3a',
  border: '#d3c8b4',

  // Palette Primaire (Laiton)
  primary: {
    50: '#fbf8f3',
    100: '#f6f0e4',
    200: '#ebe0c6',
    300: '#dfcda2',
    400: '#cfb57f',
    500: '#c09f61',
    600: '#b08f56',
    700: '#957548',
    800: '#7d5f3f',
    900: '#684f37',
    950: '#3b2c1d',
  },

  // Palette Secondaire (Rouge sang séché)
  secondary: {
    50: '#f9f6f6',
    100: '#f3ecec',
    200: '#e6d8d8',
    300: '#d6baba',
    400: '#c29494',
    500: '#a96a6a',
    600: '#924b4b',
    700: '#7f3939',
    800: '#7a2a2a',
    900: '#612626',
    950: '#341010',
  },
};

// 3. Définir nos couleurs pour le mode sombre (inchangé)
const pataphysiqueDarkColors = {
  background: '#3a3a3a',
  'dark-background': '#fbf5e9',
  border: '#5a5a5a',
  primary: pataphysiqueColors.primary,
  secondary: {
    50: '#fefafa',
    100: '#fcf4f4',
    200: '#fae8e8',
    300: '#f7d6d6',
    400: '#f1b8b8',
    500: '#e08f8f',
    600: '#d17272',
    700: '#b35757',
    800: '#944747',
    900: '#7d4040',
    950: '#431e1e',
  },
};


// 4. La configuration principale
module.exports = {
  content: [
    './layouts/**/*.html',
    './content/**/*.{md,html}',
    './hugo_stats.json',
  ],

  theme: {
    extend: {
      // --- CÂBLAGE MANUEL DES POLICES ---
      fontFamily: {
        heading: ['Playfair Display', 'serif'],
        body: ['EB Garamond', 'serif'],
        code: ['Special Elite', 'monospace'],
      },
      // --- CÂBLAGE MANUEL DES COULEURS (pour les classes tailwind) ---
      colors: pataphysiqueColors,
      
      // =================================================================
      // --- DÉBUT DE LA CORRUPTION 'OBSIDIAN' (v4.0) ---
      // =================================================================
      // On dit au plugin de typographie quelles couleurs utiliser
      // pour les éléments .prose (le markdown)
      typography: ({ theme }) => ({
        DEFAULT: {
          css: {
            // GRAS (Orange)
            '--tw-prose-bold': '#fd971f',
            // ITALIQUE (Vert)
            '--tw-prose-italic': '#a6e22e',
            // GRAS & ITALIQUE (Violet)
            // Note : le plugin ne gère pas strong+em, on force
            'strong em': { color: '#e879f9' },
            'em strong': { color: '#e879f9' },
            // LIENS (Bleu)
            '--tw-prose-links': '#80bfff',
            // CODE INLINE (Rose)
            '--tw-prose-code': '#f92672',
            // On s'assure que les couleurs sombres sont héritées
            // (le plugin utilise des variables --tw-prose-invert-...)
            '--tw-prose-invert-bold': '#fd971f',
            '--tw-prose-invert-italic': '#a6e22e',
            '--tw-prose-invert-links': '#80bfff',
            '--tw-prose-invert-code': '#f92672',
          },
        },
      }),
      // =================================================================
      // --- FIN DE LA CORRUPTION 'OBSIDIAN' ---
      // =================================================================
    },
  },

  // 5. LE PLUGIN UNIFICATEUR (couleurs) ET LE PLUGIN TYPO (corrompu)
  plugins: [
    // Plugin pour les variables CSS (inchangé)
    plugin(function ({ addBase, theme }) {
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
      addBase({
        ':root': extractColorVariables(theme('colors')),
      });
      addBase({
        "[data-theme='dark']": extractColorVariables(pataphysiqueDarkColors),
      });
    }),
    
    // Plugin de typographie (maintenant activé et configuré)
    typography, // <-- AJOUTÉ
  ],
};
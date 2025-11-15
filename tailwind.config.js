/*
  SOLUTION RADICALE v3.1 (Restaurée)
  Toute la corruption v4.0 (le plugin 'typography') a été
  retirée. Ce fichier ne gère que les polices et les
  variables de couleur de base.
*/

// 1. Importer le 'plugin' de base de tailwind
const plugin = require('tailwindcss/plugin');

// 2. Définir nos couleurs 'pataphysiques
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

// 3. Définir nos couleurs pour le mode sombre
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
    },
  },

  // 5. LE PLUGIN UNIFICATEUR (UNIQUEMENT POUR LES VARIABLES CSS)
  plugins: [
    plugin(function ({ addBase, theme }) {
      // Fonction pour aplatir les objets de couleur (ex: primary.50 -> --color-primary-50)
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

      // Générer les variables pour le mode clair
      addBase({
        ':root': extractColorVariables(theme('colors')),
      });

      // Générer les variables pour le mode sombre
      addBase({
        "[data-theme='dark']": extractColorVariables(pataphysiqueDarkColors),
      });
    }),
    
    // Le plugin 'typography' (v4.0) a été retiré. C'ÉTAIT LE CONFLIT.
  ],
};
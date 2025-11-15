/*
 * SOLUTION RADICALE v3.2 (Corrigée)
 * 1. Ré-introduction du plugin 'typography'
 * 2. Configuration de 'typography' pour utiliser nos couleurs 'pataphysiques.
 */

// 1. Importer les 'plugins'
const plugin = require('tailwindcss/plugin');
const typography = require('@tailwindcss/typography'); // <-- RÉ-ACTIVÉ

// 2. Définir nos couleurs 'pataphysiques (INCHANGÉ)
const pataphysiqueColors = {
  // Fonds & Bordures (Mode Clair)
  background: '#fbf5e9',
  'dark-background': '#3a3a3a',
  border: '#d3c8b4',

  // Palette Primaire (Laiton)
  primary: { 50: '#fbf8f3', 100: '#f6f0e4', 200: '#ebe0c6', 300: '#dfcda2', 400: '#cfb57f', 500: '#c09f61', 600: '#b08f56', 700: '#957548', 800: '#7d5f3f', 900: '#684f37', 950: '#3b2c1d' },

  // Palette Secondaire (Rouge sang séché)
  secondary: { 50: '#f9f6f6', 100: '#f3ecec', 200: '#e6d8d8', 300: '#d6baba', 400: '#c29494', 500: '#a96a6a', 600: '#924b4b', 700: '#7f3939', 800: '#7a2a2a', 900: '#612626', 950: '#341010' },
};

// 3. Définir nos couleurs pour le mode sombre (INCHANGÉ)
const pataphysiqueDarkColors = {
  background: '#3a3a3a',
  'dark-background': '#fbf5e9',
  border: '#5a5a5a',
  primary: pataphysiqueColors.primary,
  secondary: { 50: '#fefafa', 100: '#fcf4f4', 200: '#fae8e8', 300: '#f7d6d6', 400: '#f1b8b8', 500: '#e08f8f', 600: '#d17272', 700: '#b35757', 800: '#944747', 900: '#7d4040', 950: '#431e1e' },
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
      // --- CÂBLAGE MANUEL DES POLICES (INCHANGÉ) ---
      fontFamily: {
        heading: ['Playfair Display', 'serif'],
        body: ['EB Garamond', 'serif'],
        code: ['Special Elite', 'monospace'],
      },
      
      // --- CÂBLAGE MANUEL DES COULEURS (INCHANGÉ) ---
      colors: pataphysiqueColors,

      // --- NOUVEAU BLOC : INSTRUCTION POUR .PROSE ---
      typography: (theme) => ({
        DEFAULT: {
          css: {
            // Appliquer la police du corps par défaut
            '--tw-prose-body': theme('colors.primary.900'),
            '--tw-prose-headings': theme('colors.primary.900'), // Couleur de repli si le dégradé échoue
            '--tw-prose-lead': theme('colors.primary.700'),
            '--tw-prose-links': theme('colors.secondary.700'),
            '--tw-prose-bold': theme('colors.primary.900'),

            // ✅ Objectif : Italique en vert
            '--tw-prose-italic': '#008000', // Vert naturel
            em: {
              color: 'var(--tw-prose-italic)',
              'font-style': 'italic',
            },
            
            // ✅ Objectif : Citations en orange
            '--tw-prose-quotes': '#E67E22', // Texte de la citation
            '--tw-prose-quote-borders': '#fd7e14', // Bordure orange
            blockquote: {
              'border-left-color': 'var(--tw-prose-quote-borders)',
              'background-color': 'rgba(253, 126, 20, 0.05)',
              'color': 'var(--tw-prose-quotes)',
            },

            // ✅ Objectif : Blocs de code en orange
            '--tw-prose-code': theme('colors.secondary.700'), // Couleur du code inline
            '--tw-prose-pre-code': theme('colors.secondary.700'), // Couleur du texte dans le bloc
            '--tw-prose-pre-bg': 'rgba(253, 126, 20, 0.05)', // Fond du bloc
            pre: {
              'background-color': 'var(--tw-prose-pre-bg)',
              'border': '1px solid #fd7e14',
              'border-radius': '5px',
            },

            // Styles pour le mode sombre
            '--tw-prose-invert-body': theme('colors.primary.100'),
            '--tw-prose-invert-headings': theme('colors.primary.100'),
            '--tw-prose-invert-lead': theme('colors.primary.300'),
            '--tw-prose-invert-links': theme('colors.secondary.300'),
            '--tw-prose-invert-bold': theme('colors.primary.100'),
            
            // ✅ Italique vert (mode sombre)
            '--tw-prose-invert-italic': '#32CD32', // Vert citron
            
            // ✅ Citations orange (mode sombre)
            '--tw-prose-invert-quotes': '#E67E22',
            '--tw-prose-invert-quote-borders': '#fd7e14',
            
            // ✅ Blocs de code orange (mode sombre)
            '--tw-prose-invert-code': theme('colors.secondary.300'),
            '--tw-prose-invert-pre-code': theme('colors.secondary.300'),
            '--tw-prose-invert-pre-bg': 'rgba(253, 126, 20, 0.1)',
          },
        },
      }),
      // --- FIN DU BLOC TYPOGRAPHY ---
    },
  },

  // 5. LE PLUGIN UNIFICATEUR (INCHANGÉ + AJOUT TYPOGRAPHY)
  plugins: [
    // Plugin pour les variables CSS (INCHANGÉ)
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

    // ✅ LE PLUGIN .PROSE (RÉ-ACTIVÉ)
    typography,
  ],
};
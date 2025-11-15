/** @type {import('tailwindcss').Config} */

/*
  SOLUTION RADICALE - ÉTAPE 3 : LE CÂBLAGE MANUEL
  Nous n'utilisons plus le plugin withHugoBlox.
  Toutes les polices et couleurs sont définies ici.
*/

module.exports = {
  // Configure les chemins que Tailwind doit surveiller pour savoir
  // quelles classes CSS générer.
  content: [
    './layouts/**/*.html',
    './content/**/*.{md,html}',
    './hugo_stats.json',
  ],

  theme: {
    extend: {
      // --- CÂBLAGE MANUEL DES POLICES ---
      // (ce que fonts: ... dans params.yaml aurait dû faire)
      fontFamily: {
        // On ajoute 'serif' et 'monospace' comme fallbacks
        heading: ['Playfair Display', 'serif'],
        body: ['EB Garamond', 'serif'],
        code: ['Special Elite', 'monospace'],
      },

      // --- CÂBLAGE MANUEL DES COULEURS ---
      // (ce que @theme {...} dans custom.css aurait dû faire)
      colors: {
        // Fonds & Bordures (Mode Clair)
        background: '#fbf5e9',
        'dark-background': '#3a3a3a', // Sera utilisé par les classes 'dark:bg-dark-background'
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
      },
    },
  },

  // Le plugin "withHugoBlox" est volontairement omis.
  plugins: [],
};
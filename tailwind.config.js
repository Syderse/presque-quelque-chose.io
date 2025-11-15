/** @type {import('tailwindcss').Config} */

// 1. on restaure le "traducteur" (le plugin)
const { withHugoBlox } = require('./_vendor/github.com/hugoblox/hugo-blox-builder/modules/blox-tailwind/v0/content/tailwind/plugin.js');

// 2. on utilise le plugin "withHugoBlox"
module.exports = withHugoBlox({
  
  // 3. on indique à tailwind quels fichiers surveiller.
  //    NOUVELLE ACTION : On ajoute custom.css ici pour forcer sa détection.
  content: [
    './layouts/**/*.html',
    './content/**/*.{md,html}',
    './hugo_stats.json',
    './assets/css/themes/custom.css', // <-- ajout 'pataphysique
    './config/_default/params.yaml', // <-- ajout 'pataphysique pour les polices
  ],
});
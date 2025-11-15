/** @type {import('tailwindcss').Config} */

// 1. on restaure le "traducteur" (le plugin)
//    (c'est le chemin que `hugo mod vendor` a créé)
const { withHugoBlox } = require('./_vendor/github.com/hugoblox/hugo-blox-builder/modules/blox-tailwind/v0/content/tailwind/plugin.js');

// 2. on utilise le plugin "withHugoBlox" pour envelopper la configuration.
//    c'est lui qui va lire ton `params.yaml` (pour les polices)
//    et ton `assets/css/themes/custom.css` (pour les couleurs).
module.exports = withHugoBlox({
  
  // 3. on indique juste à tailwind quels *autres* fichiers surveiller.
  //    (le plugin s'occupe déjà de surveiller les fichiers du thème)
  content: [
    './layouts/**/*.html',
    './content/**/*.{md,html}',
    './hugo_stats.json',
  ],
});
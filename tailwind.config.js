/** @type {import('tailwindcss').Config} */

// Importer le plugin Hugo Blox Tailwind
// NOTE : Le chemin pointe maintenant vers le dossier '_vendor' !
const { withHugoBlox } = require('./_vendor/github.com/hugoblox/hugo-blox-builder/modules/blox-tailwind/v0/content/tailwind/plugin.js');

module.exports = withHugoBlox({
  // Configure les chemins que Tailwind doit surveiller
  content: [
    './layouts/**/*.html',
    './content/**/*.{md,html}',
    './hugo_stats.json',
  ],
});
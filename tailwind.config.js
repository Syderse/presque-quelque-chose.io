// const plugin = require('./_vendor/github.com/HugoBlox/hugo-blox-builder/modules/blox-tailwind/plugin') // <- ligne supprimée

module.exports = {
  content: [
    './hugo_stats.json',
    './layouts/**/*.html',
    './content/**/*.md',
    './_vendor/github.com/HugoBlox/hugo-blox-builder/modules/blox-tailwind/layouts/**/*.html',
    './_vendor/github.com/HugoBlox/hugo-blox-builder/modules/blox-tailwind/blox/**/*.html',
    './_vendor/github.com/HugoBlox/hugo-blox-builder/modules/blox-tailwind/assets/js/hb-header-blur.js',
  ],
  darkMode: ['class', '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        primary: 'var(--hb-color-primary)',
        secondary: 'var(--hb-color-secondary)',
        neutral: 'var(--hb-color-neutral)',
        background: 'var(--hb-color-background)',
        darkBackground: 'var(--hb-color-dark-background)',
      },
      fontFamily: {
        sans: ['var(--font-family-sans)', 'sans-serif'],
        serif: ['var(--font-family-serif)', 'serif'],
        mono: ['var(--font-family-mono)', 'monospace'],
      },
      lineHeight: {
        normal: '1.6',
      },
      letterSpacing: {
        'tighter': '-.06em',
        'tight': '-.03em',
        'normal': '0',
        'wide': '.03em',
        'wider': '.06em',
        'widest': '.09em',
      },
      fontSize: {
        'xs': '.8rem',
        'sm': '.9rem',
        'base': '1rem',
        'lg': '1.1rem',
        'xl': '1.2rem',
        '2xl': '1.5rem',
        '3xl': '1.8rem',
        '4xl': '2.2rem',
        '5xl': '2.6rem',
        '6xl': '3rem',
      },
    },
  },
  // plugins: [plugin], // <- ligne supprimée
}
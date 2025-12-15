# System Context: Architecture Hugo Blox

**Version:** 6.1 (Performance Optimized)
**Last Audit:** 2025-12-06
**Stack:** Hugo Extended (Go) | Tailwind CSS v4 (JIT) | Supabase | ESBuild

---

## 1. Philosophie & Esthétique :

- **Core Principle:** "Audit before Action." Stability > Features.
- **Visual Identity:** High Contrast, Warm, Density and Maximalism.
  - **Theme:** Main theme : Catppuccin Mocha.
- **Performance:** Target 60FPS. Transitions limited to `transform` and `opacity`.

---

## 2. Infrastructure & Configuration (`hugo.yaml`)

- **Build Strategy:**
  - `writeStats: true` (Required for Tailwind JIT).
  - `security.enableInlineShortcodes: true`.
- **Module Mounts:**
  - Standard mounts (`assets`, `layouts`, `content`, `static`).
  - **Critical Fix:** `hugo_stats.json` is _excluded_ from mounts to prevent Netlify "Cold Build" errors.
- **Custom Output Formats (Static API):**
  - `RANDOMIZER` -> `articles-aleatoires.json` (Used by Sidebar/Home).
  - `ALMANACH` -> `index.json` (Ephemeris data).
  - `RHIZOME` -> `index.json` (D3.js Node Data).
- **Taxonomies:** `tags`, `categories`, `authors` enabled.

---

## 3. Frontend Architecture (Tailwind v4 & CSS)

### A. The Pipeline (`layouts/partials/css.html`)

- **Engine:** Native Hugo `css.TailwindCSS`.
- **Production Fix (Critical):**
  - The `| minify` pipe is **DISABLED** in production.
  - _Reason:_ Hugo's standard minifier breaks Tailwind v4's native CSS nesting syntax (`& :where(...)`), causing "Color Loss" in production.
  - _Optimization:_ We rely on Tailwind's internal optimizer + Hugo `fingerprint`.

### B. Source of Truth (`assets/css/main.css`)

- **Order of Operations:**
  1.  `@import` Fonts (Google Fonts — **single consolidated request** with `display=swap`).
  2.  `@import "tailwindcss";`
  3.  `@plugin "@tailwindcss/typography";`
  4.  `@source` directives (Files scanned by JIT).
- **Font Optimization (`baseof.html`):**
  - `<link rel="preconnect">` for `fonts.googleapis.com` and `fonts.gstatic.com`.
- **Layering:**
  - **`@layer base`:** Catppuccin Variables (`--ctp-mauve`, etc.) & Typography Reset.
  - **`@layer components`:**
    - `.prose-catppuccin`: Custom typography with gradient headings.
    - `.bento-card`: The core UI unit with Hard Borders & Shadows.
- **Styling Rules:**
  - **Z-Index:** Handled via relative positioning and hard shadows.
  - **Hover Effects:** `translate(-2px, -2px)` + Shadow deepening.
  - **Color Visibility Rule:**
    - Interactive elements (buttons, links, tags, navigation) **MUST display their accent color by default**, not only on hover.
    - ❌ **Forbidden:** `text-ctp-subtext0 hover:text-ctp-mauve` (color reveals on hover).
    - ✅ **Correct:** `text-ctp-mauve` (color always visible) + hover effects limited to `shadow`, `translate`, `bg-*` changes.
    - _Rationale:_ Hover-only colors hurt discoverability, accessibility (touch devices), and overall visual coherence.
  - **Performance Rule (60fps):**
    - Avoid GPU-heavy CSS effects that cause frame drops:
    - ❌ **Forbidden:** `backdrop-filter: blur()`, `filter: blur()` — extremely expensive, especially on large elements.
    - ❌ **Avoid:** Multiple `box-shadow` with `color-mix()` calculations, `scale()` in animations, `transition: all`.
    - ❌ **Limit:** `filter` chains to **max 2 operations** per element (e.g., `sepia() brightness()`).
    - ✅ **Correct:** Solid translucent backgrounds (`rgba()`), single simplified shadows, `transform: translateX/Y` + `opacity` only.
    - ✅ **Optimize:** Use `transform: translateZ(0)` + `backface-visibility: hidden` to force GPU compositing.
    - ✅ **Images:** Use `fetchpriority="high"` on hero/LCP images, `loading="lazy"` + `decoding="async"` elsewhere.
    - _Rationale:_ Blur effects require per-pixel sampling of underlying content — catastrophic for performance.

---

## 4. Layout System (The Skeleton)

### A. App Shell (`layouts/_default/baseof.html`)

A Z-Index based Layered Architecture:

1.  **Layer 0 (Main):** The scrolling content area (`<main>`).
2.  **Layer 1 (Backdrop):** `div#sidebar-backdrop` (Click-to-close on mobile).
3.  **Layer 2 (Sidebar):** `aside#sidebar-panel` (Off-canvas on mobile, Sticky on desktop).
4.  **Layer 3 (Toggle):** `header` containing the Burger Menu (Always on top).

### B. Sidebar (`layouts/partials/sidebar.html`)

- **Nature:** "Dumb Component" (Visuals only, logic is in `baseof`).
- **Design:** Fixed width (`280px`), `bg-ctp-mantle`.
- **Logic:**
  - **Cyclic Colors:** Menu items cycle through 6 Catppuccin colors using `mod` logic.
  - **Footer:** Contains the "Manual" link and the "Randomizer" trigger.

### C. Homepage (`layouts/index.html`)

- **Architecture:** Layout-First.
- **Grid:** Bento Grid System (CSS Grid).
- **Components:**
  - `dom-card.html` (Interactive Chat).
  - `identity-card.html` (Profile).
  - `latest-posts.html` (Feed).
  - `almanach-card.html` (Time data).

---

## 5. Modules & JavaScript Engines

**Location:** `assets/js/` loaded via `partials/functions/js-loader.html`.

### A. Rhizome (Orbital Physics)

- **File:** `rhizome-engine.js` + `layouts/rhizome-curieux/list.html`.
- **Tech:** D3.js v7 + Canvas.
- **Physics:**
  - **Nucleus (Internal):** Radius 0, tightly connected mesh.
  - **Orbit (External):** Radius 400, floating satellites.
- **Data Source:** `index.json` generated by `layouts/partials/functions/get-rhizome-items.html`.

### B. Patafoin (Forum)

- **File:** `patafoin.js` + `layouts/patafoin/list.html`.
- **Tech:** Supabase JS Client (Vanilla).
- **Credentials (Sécurisé):**
  - **Local:** Variables dans `.env.local` (gitignored) : `HUGO_SUPABASE_URL`, `HUGO_SUPABASE_KEY`.
  - **Production:** Variables Netlify (Site Settings > Environment Variables).
  - **Injection:** `layouts/patafoin/list.html` utilise `getenv` avec fallback sur `Site.Params`.
- **Logic:**
  - **Topics:** Parent container.
  - **Root Post:** The first post of a topic (`parent_id: null`).
  - **Recursive Rendering:** Hierarchy built via `parent_id`.

### C. Ondes & Pixels (`layouts/ondes-pixels/`)

- **File:** `list.html` + `partials/cards/wave-card.html`.
- **Design:** Immersive dark space with ambient gradient orbs, wave-offset cards.
- **Components:**
  - `.wave-card`: Base card with cozy borders and hover lift.
  - `.wave-card-ondes`: Organic leaf-like rounded corners (audio content).
  - `.wave-card-pixels`: Sharp digital edges (video/text content).
- **Performance:** Static ambient lights (no animation), GPU-accelerated transforms only.

---

## 6. Development Protocols

### Creating Content

- **Standard Post:** `hugo new ondes-pixels/mon-sujet/index.md` (Leaf Bundle).
- **Rhizome Node:**
  - _Internal:_ Create MD file in `content/rhizome-curieux/`.
  - _External:_ Add to `params.items` in `content/rhizome-curieux/_index.md`.

### Deployment (Netlify)

1.  **Build Command:** `hugo --gc --minify` (Note: CSS is excluded from minify internally).
2.  **Environment:** Requires `HUGO_VERSION` set to matching local version (Extended).
3.  **Environment Variables (Secrets):**
    - `HUGO_SUPABASE_URL` : URL du projet Supabase.
    - `HUGO_SUPABASE_KEY` : Clé `anon` Supabase (publique mais hors Git).
4.  **Cache Headers (`netlify.toml`):**
    - CSS/JS/Fonts: `max-age=31536000, immutable` (1 year).
    - Media: `max-age=2592000` (30 days).

### Troubleshooting

- **CSS broken in Prod?** Check `layouts/partials/css.html` to ensure `minify` is NOT applied to the Tailwind pipe.
- **Sidebar not opening?** Check `baseof.html` JS script for class toggling (`-translate-x-full`).
- **Supabase Error?** Vérifier que `.env.local` existe avec `HUGO_SUPABASE_URL` et `HUGO_SUPABASE_KEY`. Le script `pnpm dev` charge automatiquement ces variables.

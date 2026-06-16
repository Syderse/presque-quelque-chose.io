# Refonte « TYPEHEAVY » — Plan maître

Conversion radicale de l'UI de `presque-quelque-chose` vers un site **clair, ultra-typographique, system-fonts, quasi sans JS, qui se charge plus vite que son ombre et se rend pareil partout** — dans l'esprit de [bestmotherfucking.website](https://bestmotherfucking.website), mais dans l'esprit seulement ça veut pas dire que mon site doit nécessairement ressembler à celui-ci dans la forme, attention.

Ce dossier contient une **série de petits prompts atomiques** à coller un par un dans Claude Opus 4.8, dans l'ordre, sur une branche dédiée. Chaque prompt est sûr, vérifiable, et **ne perd aucun contenu**.

---

## 1. L'esprit (le manifeste, verrouillé)

- **Contrastes francs.** Texte quasi-noir sur fond clair. *Quit fucking around with grey text* : aucun gris baveux, jamais.
- **Aucune fonte distante.** *Remote fonts are wasting your time and mine.* Fontes système uniquement.
- **Léger et rapide.** Tient sur n'importe quel écran, se charge instantanément.
- **Même rendu partout.** Pas d'effets fragiles, pas de dépendances exotiques.
- **Rien ne doit gêner le texte.** Le texte est le héros. Tout le reste se tait.
- **Simplicité, mais maîtrise absolue des bases.** Peu d'éléments, parfaitement réglés.
- **TYPEHEAVY.** La typographie *est* le design.

## 2. Décisions verrouillées

| Question | Choix |
|---|---|
| Palette | **Fond clair, texte quasi-noir**, haut contraste, zéro gris |
| Corps de texte | **Serif système** (Charter/Georgia/Times…) |
| CSS & build | **Refonte totale : un seul CSS écrit à la main, sans Tailwind ni Hugo Blox** |
| Accueil | **Index typographique pur** |
| **Exception DOM** | **DOM est sacré et reconverti fidèlement** : on garde son histoire de bouton (compteur 000→999, monologue de `dom-story.json`, pierre tombale finale), version minimale et type-heavy. |

## 3. Règles d'or (à respecter à CHAQUE prompt)

1. **Le contenu est sacré.** On ne touche JAMAIS à `content/**/*.md`, `data/`, `static/data/`, `static/antenne-radio/index.json`, `static/media/`. On refond l'UI (layouts, CSS, JS, build), pas les textes. Tout shortcode déjà utilisé dans le contenu (`{{< sidenote >}}`, `{{< relref >}}`, embeds) doit continuer à fonctionner.
2. **Aucune fonte distante.** Pas de `fonts.googleapis.com`, pas de `@import url(...)`. Stacks système seulement.
3. **Haut contraste, pas de gris.** Pour différencier un texte secondaire : taille, graisse, italique, petites capitales, filets — **jamais** une couleur grise délavée.
4. **On garde les URLs, endpoints et la discipline existante.** Sorties JSON `ALMANACH` / `RANDOMIZER` / `RHIZOME`, RSS, redirects SEO, URLs accentuées (`/blog_coree/`), whitelist de l'antenne radio, CSP Netlify. On adapte la CSP quand on retire des domaines, on ne la casse pas.
5. **On mesure avant/après** dès qu'on touche au build, au CSS, aux assets (voir §6).
6. **On vérifie le build à chaque prompt** avec le Hugo épinglé du projet : `pnpm exec hugo --gc --minify`. Jamais `hugo` global.
7. **Un commit par prompt**, message court et clair. On travaille sur la branche `refonte-typeheavy`.
8. **Le projet Python `antenne_radio/` est hors périmètre.** Seul change le rendu de son JSON déjà exporté.

## 4. Palette & typo cibles (référence pour tous les prompts)

Tokens de départ (ajustables, mais c'est la cible). Ils vivent dans `assets/css/site.css` (le futur fichier unique).

```css
:root {
  /* Palette — clair, haut contraste, zéro gris baveux */
  --bg:           #fbfaf7; /* papier chaud */
  --fg:           #14110d; /* quasi-noir : le texte */
  --fg-strong:    #000000; /* titres / accents forts */
  --link:         #9a1f1b; /* rouge profond, lisible sur clair */
  --link-visited: #5a2a86; /* violet profond */
  --accent:       #1a4d8f; /* bleu profond : liens internes / marqueurs */
  --rule:         #14110d; /* filets = couleur du texte (jamais gris) */
  --mark:         #fff2a8; /* surlignage */
  --code-bg:      #f0ede6;

  /* Typographie — 100% système */
  --serif: Charter, "Bitstream Charter", "Sitka Text", "Iowan Old Style",
           "Palatino Linotype", Palatino, Cambria, Georgia,
           "Times New Roman", Times, serif;
  --mono:  ui-monospace, "SF Mono", SFMono-Regular, Menlo, Consolas,
           "Liberation Mono", monospace;

  --measure: 66ch;       /* largeur de lecture */
  --base: clamp(1.05rem, 0.95rem + 0.5vw, 1.2rem);
  --lh: 1.55;
}
```

- **Corps & titres en serif** ; **mono réservé** aux métadonnées, labels, kickers, code.
- **Texte secondaire** = même `--fg`, différencié par la taille/graisse/petites capitales, pas par une couleur pâle.
- **Liens soulignés.** Internes = `--accent`, externes = `--link`, visités = `--link-visited`. Liens cassés signalés mais lisibles.

## 5. Passerelles : ce que devient chaque idée existante

| Idée | Verdict | Forme minimale |
|---|---|---|
| Textes, carnets, recherches (tout `content/`) | **Intact** | Rendus en serif, pleine lisibilité |
| Sidenotes Tufte | **Gardé** | CSS pur, marges desktop / inline mobile, zéro JS |
| Liens wiki internes | **Gardé** | Soulignés, marqueur discret interne/cassé |
| Article aléatoire | **Gardé** | Lien + `/articles-aleatoires.json` |
| Recherche Pagefind | **Gardé** | Page `/recherche` dédiée, UI chargée là seulement |
| Partage / CTA Patafoin / related / prev-next | **Gardé, allégé** | Liens sobres, JS presse-papier minuscule |
| Embeds ondes & pixels | **Gardé, allégé** | Façade *click-to-load* (lien → iframe à la demande) |
| **DOM (le bouton)** | **Gardé, reconverti** | Bouton sobre + compteur texte 000→999 + monologue `dom-story.json` + pierre tombale ; ~40 lignes de JS |
| Almanach pataphysique | **Transformé** | Une ligne de date pataphysique + saint ; page `/almanach` = entrées en texte |
| Rhizome D3 | **Transformé** | Liste imbriquée lisible par défaut ; graphe en option *au clic* |
| Antenne radio | **Transformé** | Liste/table HTML statique (le JSON est déjà lu au build) |
| Forum Patafoin | **Gardé, isolé** | Supabase chargé seulement sur `/patafoin` |
| Carte d'identité RPG | **Transformé** | Ligne « à propos » + niveau (jours de vie) en une phrase + liens texte |
| Télémétrie système | **Coupé / réduit** | Au mieux une ligne discrète en pied |
| Tableau de bord bento, sidebar overlay, néo-brutalisme, Catppuccin, 6 fontes | **Retiré** | Remplacé par le socle type-heavy |

## 6. Mesure de baseline (à lancer au P01, puis à comparer au P25)

```sh
du -sh .git static _vendor public 2>/dev/null
pnpm exec hugo --gc --minify --cleanDestinationDir >/dev/null 2>&1
ls -la public/css/ 2>/dev/null            # poids CSS généré
find public -name '*.js' -exec du -ch {} + | tail -1   # poids JS total
ls public/almanach/index.json public/articles-aleatoires.json public/rhizome-curieux/index.json 2>/dev/null
test ! -f public/almanach/index.html && echo "OK: pas de almanach/index.html"
```

Objectif après refonte : **un seul petit CSS**, **JS quasi nul** (sauf DOM + Patafoin isolé + façades embeds), **zéro requête de fonte distante**, mêmes endpoints JSON présents.

## 7. Index ordonné des prompts

Phase 1 — Socle & coquille — `01_socle_et_coquille.md`
- **P01** Branche + baseline mesurée + garde-fous
- **P02** `site.css` : tokens + reset + base typographique (le cœur)
- **P03** Brancher `site.css` via Hugo Pipes (à côté de Tailwind pour la migration)
- **P04** `baseof.html` : coquille sémantique en flux normal (fin du dashboard plein écran)
- **P05** En-tête + navigation texte (remplace sidebar overlay + mobile-nav)
- **P06** Pied de page minimal

Phase 2 — Lecture (cœur type-heavy) — `02_lecture.md`
- **P07** `single.html` : article minimal (fin de la TOC overlay)
- **P08** Styles de prose dans `site.css` (titres, liens, citations, listes, code, tables)
- **P09** Sidenotes en CSS pur (sans `sidenote-adjuster.js`)
- **P10** Liens internes / wiki / cassés
- **P11** `article-footer.html` allégé (partage, CTA Patafoin, related, prev/next)

Phase 3 — Accueil & listes — `03_accueil_et_listes.md`
- **P12** Accueil : index typographique pur
- **P13** Gabarit de liste unifié (solutions-imaginaires, ondes-pixels, recherches…)
- **P14** Tags / thésaurus
- **P14b** 404 minimale

Phase 4 — Passerelles — `04_passerelles.md`
- **P15** DOM reconverti (le clou du spectacle)
- **P16** Almanach : ligne pataphysique + page entrées
- **P17** Rhizome : liste par défaut, graphe en option
- **P18** Antenne radio : liste/table statique
- **P19** Embeds ondes & pixels : façades click-to-load
- **P20** Forum Patafoin isolé
- **P21** « À propos » (ex carte d'identité)

Phase 5 — Démontage, sécurité, vérif, doc — `05_demontage_et_verif.md`
- **P22** Retrait de Tailwind + Hugo Blox + ancien `main.css`
- **P23** Nettoyage JS, fontes, images
- **P24** Netlify / CSP / Pagefind / (GA optionnel)
- **P25** Build, mesures, comparaison baseline, contrôle contraste & multi-navigateur
- **P26** Mise à jour `AGENTS.md` / `HISTORIQUE.md` / `CHANTIERS.md`

## 8. Comment s'en servir

1. Lance **P01** : il crée la branche et fige la baseline.
2. Colle ensuite chaque **« Prompt à coller »** dans Claude Opus 4.8, dans l'ordre, une session ou une à la suite de l'autre.
3. Après chaque prompt : vérifie le rendu (`pnpm dev`), build (`pnpm exec hugo --gc --minify`), commit.
4. Tu peux t'arrêter à n'importe quelle phase : le site reste fonctionnel entre deux prompts (Tailwind n'est retiré qu'au P22, une fois tous les gabarits migrés).

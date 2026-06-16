# Phase 2 — Lecture, le cœur type-heavy (P07 → P11)

L'expérience de lecture est ce qui compte le plus : *rien ne doit gêner le texte*. On garde sidenotes et liens wiki, mais en CSS pur. Lis `00_PLAN.md` d'abord.

---

## P07 — `single.html` : article minimal

**But.** Réduire la page article à l'essentiel lisible. Fin de la TOC en overlay (avec son JS).
**Fichiers.** `layouts/_default/single.html`. (Garde `article-footer.html` pour le P11.)

**Prompt à coller :**

> Réécris `layouts/_default/single.html` en page article minimale et type-heavy, dans la colonne `.measure`.
> - **Supprime** tout le système TOC overlay : backdrop, `#toc-panel`, `reader-plan-shell`, le bouton « Plan » et le `<script>` de pilotage. À la place, SI `.TableOfContents` existe, propose une table des matières **statique** repliable en haut de l'article via `<details><summary>Plan</summary>…</details>` (HTML natif, zéro JS). Nettoie toujours les placeholders `HAHAHUGOSHORTCODE…HBHB` comme avant.
> - Garde un fil d'Ariane texte simple (accueil › section › titre), sobre.
> - `<h1>` du titre en serif ; sous le titre, une ligne de métadonnées en `--mono` discret (date, tags en liens vers `/tags/...`) — différenciée par la taille/mono, **pas** par du gris.
> - `<article class="measure article-prose">{{ .Content }}</article>` — **ne touche pas** à `.Content`. Les styles de prose arrivent au P08.
> - Garde l'appel à `{{ partial "article-footer.html" . }}` (sauf si `.Params.hide_footer`).
> - **Retire** le `<script>` `sidenote-adjuster.js` : les sidenotes passeront en CSS pur au P09.
> - Aucune classe Tailwind, aucune classe `ctp-*`, aucune fonte distante.
> Vérifie le build sur un article qui a une TOC et des sidenotes (ex. `content/solutions-imaginaires/blog_corée/jour_1/`). Ne touche pas à `content/`. Commit : `refonte: single article minimal`.

**Vérif.** Article lisible, plan repliable natif, fil d'Ariane présent, `.Content` intact, build vert.

---

## P08 — Styles de prose dans `site.css`

**But.** Régler finement la prose : c'est là que vit le « TYPEHEAVY ».
**Fichiers.** `assets/css/site.css` (section `COMPOSANTS`, sous-bloc `.article-prose`).

**Prompt à coller :**

> Dans `assets/css/site.css`, ajoute les styles de prose sous `.article-prose` (la prose des articles). Objectif : confort de lecture maximal, contraste franc, zéro gris.
> - Largeur de lecture héritée de `.measure` (~66ch). Interlignage `1.6`–`1.7` pour les paragraphes.
> - Hiérarchie de titres claire en serif (`h2`,`h3`,`h4` dans la prose), marges hautes généreuses, graisse forte. Pas de couleurs néon : noir/`--fg-strong`, éventuellement l'`--accent` avec parcimonie.
> - Paragraphes, listes (`ul`,`ol`), citations (`blockquote` avec filet `--rule` à gauche et léger retrait, italique optionnelle), `hr` discret.
> - **Liens de prose** : soulignés, `--link` (externes) / `--accent` (internes, voir P10) / `--link-visited`. Le hover épaissit le trait, **ne pâlit pas**.
> - `code` inline et blocs `pre` en `--mono` sur `--code-bg`, scroll horizontal propre.
> - Images : `figure`/`figcaption` ; la légende se distingue par la taille/italique/mono, **pas** par un gris.
> - Tables : filets `--rule`, en-têtes en petites capitales.
> - `abbr`, `mark`, `sup`/`sub` propres.
> Respecte la règle anti-gris partout. Vérifie sur un article dense (blog corée). Ne touche pas à `content/`. Commit : `refonte: styles de prose`.

**Vérif.** Un article long est agréable à lire, hiérarchie nette, aucun texte gris.

---

## P09 — Sidenotes en CSS pur (sans `sidenote-adjuster.js`)

**But.** Conserver les sidenotes Tufte (notes + commentaires), mais en CSS pur : marge sur grand écran, inline sur mobile, zéro JS.
**Fichiers.** `layouts/shortcodes/sidenote.html`, `assets/css/site.css`. **Ne touche pas au contenu** : la syntaxe `{{< sidenote >}}` / `{{< sidenote variant="comment" >}}` doit rester identique.

**Prompt à coller :**

> Reconvertis les sidenotes en version **CSS pure**, sans `sidenote-adjuster.js`, en gardant exactement la même syntaxe de shortcode dans le contenu (`{{< sidenote >}}…{{< /sidenote >}}` et la variante `variant="comment"`, plus les libellés `label`/`caption`/`author` et `sidenote_comment_label`). Lis l'actuel `layouts/shortcodes/sidenote.html` pour préserver toute la logique de variantes.
> - Mécanique sans JS : un appel numéroté en exposant dans le texte ; la note s'affiche **en marge** sur écran large via CSS (positionnement par `float`/marge négative ou colonne dédiée), et **en bloc inline** juste après le paragraphe sur écran étroit. Tu peux garder la technique checkbox/`:checked` (label + input caché) pour le repli/dépli mobile, mais **sans dépendance JS** et sans classes Tailwind.
> - Deux variantes visuelles distinctes : `note` (érudite, sobre) et `comment` (voix de commentaire, ex. les remarques d'A.) — différenciées par un filet/italique/petite capitale de libellé, pas par un gris.
> - Numérotation automatique via compteurs CSS si possible (`counter-reset`/`counter-increment`) pour ne pas dépendre de l'ordinal Hugo, ou conserve l'ordinal existant si plus simple.
> - Le marqueur et la note restent lisibles (contraste franc), alignés sur la colonne de lecture `.measure`.
> - **Supprime** la balise `<script>` `sidenote-adjuster.js` partout où elle est incluse (déjà retirée du single au P07 ; vérifie qu'il n'en reste pas ailleurs). Le fichier JS sera supprimé au P23.
> Teste sur `content/solutions-imaginaires/blog_corée/jour_1/` (beaucoup de sidenotes des deux variantes). Vérifie desktop ET mobile (largeur réduite). Ne modifie aucun fichier de `content/`. Commit : `refonte: sidenotes CSS pur`.

**Vérif.** Les notes de marge s'affichent sans JS sur desktop, en bloc sur mobile ; les deux variantes restent distinctes ; aucun texte de contenu modifié.

---

## P10 — Liens internes / wiki / cassés

**But.** Garder la navigation « de idée en idée » : liens internes distincts des externes, liens cassés signalés — mais en haut contraste.
**Fichiers.** `layouts/_markup/render-link.html`, `assets/css/site.css`.

**Prompt à coller :**

> Revois le render hook `layouts/_markup/render-link.html` et les styles associés pour distinguer, de façon lisible et sobre :
> - **liens internes** (vers une page du site) : couleur `--accent`, soulignés, éventuellement un petit marqueur discret (ex. `›` ou un trait), classe `internal-link`.
> - **liens externes** : couleur `--link`, soulignés. Tu peux ajouter `rel="noopener"` et un repère externe discret (ex. `↗`) en pseudo-élément.
> - **liens cassés** (cible interne introuvable) : signalés sans agresser — souligné ondulé ou couleur `--link` + repère, mais **toujours lisible** (pas de rouge néon clignotant). Préserve le comportement de détection actuel s'il existe.
> Aucune couleur grise, aucune classe Tailwind. Mets les styles dans `site.css`. Teste sur un article riche en liens (blog corée, qui mélange `relref` internes et liens Wikipédia externes). Ne touche pas à `content/`. Commit : `refonte: liens internes/externes/cassés`.

**Vérif.** Internes et externes visuellement distincts, contraste franc, `relref` toujours fonctionnels.

---

## P11 — `article-footer.html` allégé

**But.** Garder partage, CTA Patafoin, articles liés et prev/next — version sobre.
**Fichiers.** `layouts/partials/article-footer.html`, `layouts/partials/cards/related-article-card.html`, `assets/css/site.css`.

**Prompt à coller :**

> Réécris `layouts/partials/article-footer.html` en version minimale type-heavy (retire tout le néo-brutalisme : ombres dures, bordures épaisses, classes `ctp-*`/Tailwind).
> - Bloc méta sobre : date de publication, nombre de caractères, version Git si dispo — en `--mono` discret, différencié par la taille pas par le gris.
> - **Bouton Partager** : garde le petit script presse-papier (copie `window.location.href`) ; remplace la grosse infobulle stylée par un retour minimal (changement de libellé « lien copié » pendant 1 s, ou un petit texte). JS minuscule et inline, sans dépendance.
> - **CTA Patafoin** : garde le lien `/patafoin/?sujet={{ .Title | urlquery }}` (le préremplissage du sujet est important), version texte/lien sobre.
> - **Articles liés** : garde la logique (`.Site.RegularPages.Related` puis repli même section) mais rends-les en **liste de liens** simple ; réécris `related-article-card.html` en version texte (titre + date), sans carte décorée.
> - **Prev/next** : deux liens texte (« précédent » / « suivant ») avec les titres.
> Styles dans `site.css`. Aucune fonte distante, aucun gris. Vérifie le build. Ne touche pas à `content/`. Commit : `refonte: footer d'article allégé`.

**Vérif.** Partage fonctionne, CTA Patafoin préremplit le sujet, related + prev/next en liens texte, build vert.

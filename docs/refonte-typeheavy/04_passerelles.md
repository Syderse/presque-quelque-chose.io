# Phase 4 — Passerelles : les idées qui survivent (P15 → P21)

Ici on reconvertit les fonctionnalités signature en versions minimales et fidèles. **DOM (P15) est le clou** : on ne perd rien de son histoire. Lis `00_PLAN.md` d'abord.

---

## P15 — DOM reconverti (le clou du spectacle) ⭐

**But.** Sauver DOM intégralement — son histoire de bouton — en version manifeste : un bouton sobre qui, clic après clic (000→999), déroule le monologue de `static/data/dom-story.json`, persiste le compteur, et finit sur une pierre tombale. ~40 lignes de JS, zéro Tailwind, zéro Catppuccin, fontes système, haut contraste.
**Fichiers.** Créer `assets/js/dom.js` (nouveau, minimal) ; un partial `layouts/partials/dom.html` ; brancher dans `layouts/index.html` (slot prévu au P12) ou sur une page `/dom`. **`static/data/dom-story.json` est SACRÉ : ne le modifie pas.** L'ancien `assets/js/dom-engine.js` et `layouts/partials/widgets/dom-card.html` seront supprimés au P23.

**Prompt à coller :**

> DOM est un élément auquel je tiens énormément : c'est un bouton récalcitrant qui, clic après clic, raconte sa vie d'élément du DOM en 999 répliques, jusqu'à une pierre tombale au clic 999. Lis `static/data/dom-story.json` (999 lignes, **à préserver tel quel**), l'ancien `assets/js/dom-engine.js` et `layouts/partials/widgets/dom-card.html` pour comprendre la mécanique d'origine (compteur, révélation de la réplique suivante, persistance, pierre tombale « Ici repose DOM. Il a bien cliqué. », option admin de réglage du compteur).
>
> Reconvertis DOM fidèlement, mais dans l'esprit manifeste (clair, sobre, type-heavy, fontes système, haut contraste, **aucune** dépendance, pas de Tailwind ni de classes `ctp-*`, pas d'effets GPU/glitch lourds) :
> 1. **Partial** `layouts/partials/dom.html` : un petit bloc sémantique — un `<button>` au texte initial (ex. « ne pas cliquer » ou « INITIALISER », au choix, sobre), un compteur en texte (`000 / 999`) en `--mono`, et une zone de texte (`<p>`/`<blockquote>`) où s'affiche la réplique courante en serif. Pas de HUD néon, pas de grille, pas d'emoji obligatoire (tu peux garder un sobre `👾` système si tu veux, c'est une glyphe système — mais discret).
> 2. **JS** `assets/js/dom.js`, minimal (~40–60 lignes, vanilla, sans dépendance) :
>    - `fetch('/data/dom-story.json')` une fois ; au clic, incrémente le compteur, affiche la réplique d'index courant, met à jour `000/999`.
>    - **Persistance** du compteur via `localStorage` (réutilise une clé proche de l'ancienne pour ne pas casser l'état des visiteurs si possible).
>    - **Pierre tombale** au clic 999 : remplace le bloc par l'épitaphe « Ici repose DOM. Il a bien cliqué. » + « Connection terminated. », en texte sobre. Désactive ensuite le bouton.
>    - Garde-fou : si le JSON n'est pas chargé, le bouton ne casse rien.
>    - (Optionnel, si simple) conserve un mini-mode admin pour fixer le compteur — mais **sans** mot de passe théâtral ni couches z-index : par ex. un paramètre d'URL `?dom=NNN` ou une petite invite `prompt()`. Si ça alourdit, laisse tomber : la priorité absolue est l'histoire et la pierre tombale.
>    - Aucune animation infinie, aucun `backdrop-filter`, aucun `will-change` permanent. Au plus une transition d'opacité courte sur le changement de réplique.
> 3. **Style** dans `assets/css/site.css` (section COMPOSANTS, `.dom-*`) : haut contraste, fontes système, le texte de la réplique bien lisible en serif. **Pas de gris.**
> 4. **Branche-le** : dans `layouts/index.html`, au slot DOM prévu (bas de l'accueil), en élément discret mais présent — fidèle à l'idée d'un bouton qu'on n'est pas censé cliquer mais qui se met à parler. Charge `dom.js` uniquement là (via le bloc `scripts` ou un `js-loader`).
>
> Ne modifie pas `static/data/dom-story.json`. Vérifie : premier clic affiche la réplique 1, le compteur persiste après rechargement, l'enchaînement fonctionne, et (en forçant le compteur près de 999) la pierre tombale s'affiche. Commit : `refonte: DOM reconverti, minimal et fidèle`.

**Vérif.** DOM cliquable, révèle les répliques, compteur persistant, pierre tombale à 999, aucune dépendance, contenu de l'histoire intact.

---

## P16 — Almanach : ligne pataphysique + page entrées

**But.** Garder le calendrier pataphysique en une **ligne de texte** (date + saint du jour) et une page `/almanach` qui liste les entrées de journal en texte. Garder l'endpoint JSON `ALMANACH` et `data/almanach.yaml`.
**Fichiers.** `assets/js/PataphysicalDate.js` (conservé, c'est une lib offline autonome), un petit script de branchement, `layouts/index.html` (slot almanach), éventuellement une page/section `almanach` HTML. **Ne touche pas** à `data/almanach.yaml`, `content/almanach/_index.md`, ni à `layouts/almanach/list.almanach.json`.

**Prompt à coller :**

> Reconvertis l'almanach en version texte minimale, sans la carte animée.
> 1. **Ligne pataphysique** sur l'accueil : un petit script branche, dans `#almanach-line` (slot prévu au P12), la date pataphysique du jour + le saint, calculés par `assets/js/PataphysicalDate.js` (lib autonome, offline — conserve-la). Sortie en une phrase sobre (ex. « Nous sommes le [jour] [mois] [année] E.P. — fête de [saint]. »). Charge le script uniquement sur l'accueil. Gère proprement l'absence de JS (la ligne reste vide, sans casser).
> 2. **Page almanach lisible** : si utile, une page HTML qui liste les entrées de `data/almanach.yaml` (ou via l'endpoint `/almanach/index.json`) en **texte** : chaque entrée en paragraphe. Réutilise la logique de lecture existante sans dénaturer le contenu. **Ne remets pas** `ALMANACH` dans `outputs.section` ; l'endpoint `public/almanach/index.json` doit continuer d'exister et `public/almanach/index.html` ne doit pas exister.
> 3. Retire la dépendance à `assets/js/almanach.js` (le gros contrôleur de « deck ») si la version texte suffit ; sinon garde-en le strict minimum. Ce nettoyage final se fait au P23.
> Aucune fonte distante, zéro gris, pas de Tailwind. Styles dans `site.css`. Vérifie que l'endpoint JSON almanach existe toujours après build. Ne touche pas à `data/` ni `content/`. Commit : `refonte: almanach en ligne de texte`.

**Vérif.** Ligne pataphysique affichée sur l'accueil ; endpoint `/almanach/index.json` toujours présent ; pas de `almanach/index.html`.

---

## P17 — Rhizome : liste par défaut, graphe en option

**But.** Rendre le rhizome lisible sans JS (liste imbriquée racines/spores), avec le graphe D3 disponible **au clic** seulement.
**Fichiers.** `layouts/rhizome-curieux/list.html`, `assets/css/site.css`. Conserver `layouts/rhizome-curieux/list.rhizome.json` (endpoint `RHIZOME`), `layouts/partials/functions/get-rhizome-items.html`, et `assets/js/rhizome-engine.js` (chargé seulement à la demande).

**Prompt à coller :**

> Réécris `layouts/rhizome-curieux/list.html` pour rendre le rhizome **lisible par défaut, sans JS**, en réutilisant `layouts/partials/functions/get-rhizome-items.html` (mêmes données : racines internes = mes pages/notes, spores = liens externes).
> - **Liste imbriquée** : les racines (notes internes du rhizome, avec leur petit texte) en section, puis les spores (liens externes) regroupées et listées en liens. Garde les icônes/emoji système éventuels mais discrets. Conserve la description de section (`_index.md`).
> - **Graphe en option** : garde le graphe D3 comme *amélioration progressive*, chargé **seulement au clic** sur un bouton « voir le graphe ». Ne charge `d3` + `rhizome-engine.js` que dans ce cas (pas au chargement de page). Pour rester self-contained et compatible CSP « self », **héberge d3 en local** (`static/vendor/d3.min.js`) plutôt que via le CDN jsdelivr ; adapte le `<script>` en conséquence. Si tu préfères, le graphe peut vivre sur une sous-page `/rhizome-curieux/graphe/` plutôt qu'en overlay. Demande moi-même auparavant si je souhaite supprimer le graphe et le D3. 
> - Retire le style néo-brutaliste (bordures épaisses, ombres dures, `ctp-*`) ; passe au socle `site.css`.
> - Conserve `outputs: [HTML, RHIZOME]` et l'endpoint `/rhizome-curieux/index.json`.
> Aucune fonte distante, zéro gris. Vérifie que la liste s'affiche sans JS et que le graphe se charge au clic. Ne touche pas à `content/`. Commit : `refonte: rhizome en liste (+ graphe optionnel)`.

**Vérif.** `/rhizome-curieux/` lisible sans JS ; bouton « voir le graphe » charge D3 à la demande ; endpoint JSON intact.

---

## P18 — Antenne radio : liste/table statique

**But.** Rendre la veille en liste/table HTML statique (le JSON est déjà lu au build), sans le moteur JS de filtres ni le néo-brutalisme.
**Fichiers.** `layouts/antenne-radio/list.html`, `assets/css/site.css`. `assets/js/antenne-radio.js` sera retiré au P23. **Ne touche pas** à `static/antenne-radio/index.json` ni à la whitelist.

**Prompt à coller :**

> Réécris `layouts/antenne-radio/list.html` en liste/table statique sobre. Le fichier lit déjà `static/antenne-radio/index.json` au build (`readFile | transform.Unmarshal`) — garde cette lecture build-time.
> - Garde l'intro/avertissement (mise à jour manuelle, index minimal whitelisté) et la date de génération.
> - Rends les items en **table sémantique** ou liste : source, titre (lien vers l'origine), date, langue, DOI (lien) quand présent — strictement les champs déjà exposés (respecte la whitelist, n'ajoute aucun champ).
> - **Supprime** le moteur de filtres JS (`antenne-radio.js`) et le style néo-brutaliste (`border: 4px`, ombres `12px 12px`, mono partout). Si tu veux un filtre, fais-en un minimal **sans dépendance** (un `<input>` qui masque/affiche des lignes en JS vanilla de ~15 lignes) — sinon, pas de filtre, la liste statique suffit.
> - Conserve un `<noscript>`/repli propre : tout doit être lisible sans JS.
> Passe au socle `site.css`, zéro gris, zéro fonte distante. Vérifie le rendu. Ne touche pas au JSON ni au projet `antenne_radio/`. Commit : `refonte: antenne radio en liste statique`.

**Vérif.** La veille s'affiche entièrement sans JS, champs limités à la whitelist, lisible.

---

## P19 — Embeds ondes & pixels : façades click-to-load

**But.** Garder tous les contenus audio/vidéo mais sans charger les iframes lourdes au chargement : une façade cliquable qui injecte l'iframe à la demande.
**Fichiers.** Créer un shortcode `layouts/shortcodes/embed.html` (ou `video.html`/`podcast.html`), `assets/css/site.css`, un mini-script. **Important :** le contenu d'`ondes-pixels` utilise actuellement des `<iframe>`/`<script>` directement dans le markdown (YouTube, Spotify, RedCircle/podcache). On veut les alléger **sans réécrire le contenu si possible**.

**Prompt à coller :**

> Allège les embeds d'`ondes & pixels` pour qu'ils ne pèsent rien tant qu'on ne clique pas, sans perdre de contenu.
> 1. Inspecte les pages de `content/ondes-pixels/` pour voir les formes d'embed utilisées (iframes YouTube, embed Spotify, lecteur RedCircle/podcache via `<script>`).
> 2. Crée un shortcode `embed` (`layouts/shortcodes/embed.html`) qui produit une **façade click-to-load** : un bloc cliquable (titre + type : vidéo/podcast) qui, **au clic**, injecte l'iframe réelle (vanilla JS, ~15 lignes, sans dépendance, fonction réutilisable). Paramètres : `type` (youtube/spotify/redcircle), `id`/`src`, `title`.
> 3. Style sobre de la façade dans `site.css` (cadre, ratio 16:9 pour la vidéo), haut contraste, zéro gris. Lazy par défaut (`loading="lazy"` une fois l'iframe injectée).
> 4. **Migration du contenu : tolérée et minimale.** Tu PEUX remplacer dans `content/ondes-pixels/**` les blocs d'iframe bruts par le shortcode `embed` équivalent, **à condition de ne perdre aucune URL ni aucun média** (même vidéo, même podcast). Si un cas est trop spécifique (le script RedCircle), garde-le tel quel plutôt que de risquer une perte. Montre-moi un diff de contenu avant de committer cette partie.
> 5. Garde la CSP `frame-src` actuelle (YouTube, Spotify, Acast, podcache, redcircle) ; ne l'élargis pas.
> Vérifie qu'une page ondes-pixels se charge sans iframe, et que le clic charge bien le média. Commit séparé pour le code (`refonte: shortcode embed click-to-load`) et, si tu migres du contenu, un commit distinct (`contenu: embeds via shortcode (sans perte)`).

**Vérif.** Page ondes-pixels légère au chargement, média chargé au clic, aucune URL/média perdu, CSP inchangée.

---

## P20 — Forum Patafoin isolé

**But.** Garder le forum Supabase fonctionnel mais ne charger Supabase + son JS QUE sur `/patafoin`. Restyler au socle.
**Fichiers.** `layouts/patafoin/list.html`, `assets/js/patafoin.js`, `assets/css/site.css`. Garde les params Supabase (`hugo.yaml`, `.env.local`) et le préremplissage `?sujet=`.

**Prompt à coller :**

> Réécris `layouts/patafoin/list.html` en version type-heavy sobre, en gardant le forum **pleinement fonctionnel** mais **isolé** :
> - Charge le client Supabase (UMD) et `assets/js/patafoin.js` **uniquement sur cette page** (pas globalement). Idéalement héberge le bundle Supabase en local (`static/vendor/`) pour rester compatible CSP « self » ; sinon garde la source actuelle et veille à la CSP.
> - Conserve toute la logique : lecture des topics/posts, création de sujet, réponses, et le **préremplissage du sujet** via le paramètre `?sujet=` (utilisé par le CTA d'article).
> - Remplace le style Catppuccin/néo-brutaliste par le socle `site.css` : formulaire et fils de discussion lisibles, contraste franc, zéro gris, fontes système.
> - Repli propre sans JS / si Supabase indisponible : un message clair, pas une page cassée.
> Vérifie le rendu (sans clés, le forum doit au moins s'afficher proprement). Ne touche pas à `content/`. Commit : `refonte: forum patafoin isolé et sobre`.

**Vérif.** `/patafoin` s'affiche sobre ; Supabase chargé seulement là ; `?sujet=` toujours pris en compte.

---

## P21 — « À propos » (ex carte d'identité RPG)

**But.** Remplacer la carte d'identité RPG par une présentation texte : une ligne « à propos » + le clin d'œil du niveau (jours de vie) + liens sociaux texte.
**Fichiers.** `layouts/index.html` (ou une page `/about`), `assets/css/site.css`. `assets/js/daily-exp.js` et `layouts/partials/widgets/identity-card.html` seront retirés au P23. L'avatar `static/media/avatar-explorer.jpg` peut être gardé (vrai asset) ou non.

**Prompt à coller :**

> Reconvertis la carte d'identité RPG en présentation texte sobre (sur l'accueil ou une courte page `/about`, au choix le plus simple) :
> - Une ou deux phrases « à propos » : qui je suis (Mathieu Allag, doctorant en études radiophoniques, venu de l'histoire de l'art et du cinéma), ce qu'est ce site.
> - Le clin d'œil du **niveau** : au lieu d'une barre d'XP animée, une seule phrase calculée — « niveau [N] » où N = jours depuis `site.Params.author.birthdate` (calcul Hugo build-time, pas de JS ; reprends la formule de `identity-card.html`). Ton joueur, mais texte.
> - **Liens sociaux en texte** : YouTube, Instagram, Patafoin, Manuel — liens soulignés, libellés clairs (résous au passage le TODO de CHANTIERS sur les libellés de destination, mais en texte simple, sans tooltip JS).
> - Avatar : optionnel. Si tu le gardes, une seule `<img>` sobre, `loading="lazy"`, sans cadre néon. Sinon, pas d'image.
> Retire la dépendance `daily-exp.js` (calcul désormais build-time). Zéro gris, zéro fonte distante, pas de Tailwind. Styles dans `site.css`. Vérifie le build. Ne touche pas à `content/`. Commit : `refonte: à propos en texte (ex carte identité)`.

**Vérif.** Présentation texte lisible, niveau calculé au build, liens sociaux clairs, plus de `daily-exp.js` requis.

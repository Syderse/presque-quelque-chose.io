# Phase 3 — Accueil & listes (P12 → P14b)

L'accueil devient un index typographique pur (DOM est traité à part, au P15). Les listes de section deviennent des listes lisibles. Lis `00_PLAN.md` d'abord.

---

## P12 — Accueil : index typographique pur

**But.** Remplacer le tableau de bord bento par un index sobre : qui je suis, les sections, les derniers textes, une ligne almanach, l'aléatoire. (DOM sera ajouté au P15.)
**Fichiers.** `layouts/index.html`. Les widgets (`dom-card`, `identity-card`, `latest-posts`, `almanach-card`, `system-header`, `manifesto-card`) ne sont plus inclus ici ; on ne les supprime pas encore (P23).

**Prompt à coller :**

> Lis `CLAUDE.md` d'abord. et `00_PLAN.md`.
> Réécris `layouts/index.html` en **index typographique pur**, dans la colonne de lecture (`.measure` ou une largeur un peu plus large mais sobre). Plus de grille bento, plus de widgets `ctp-*`, plus de plein écran.
> - **Titre** du site `presque-quelque-chose` + **accroche** : « Explorations éclectiques, inoccupations impersonnelles et science du particulier. » (depuis `site.Params.description`).
> - **Courte intro** (2–3 phrases) dans le ton du site, présentant le lieu comme un cabinet de curiosités. Tu peux réutiliser/condenser le `content/_index.md` existant si pertinent (sans le dénaturer).
> - **Les sections** : une liste de liens vers chaque section (`.Site.Menus.main`) avec, pour chacune, une phrase de description (réutilise les `description` des `_index.md` de section). Type-heavy : titres de section en serif, description en dessous.
> - **Derniers textes** : une liste des N dernières pages de contenu publiées (toutes sections de lecture confondues, ex. `solutions-imaginaires`, `ondes-pixels`, `recherches`, `rhizome-curieux`), titre + date, triées par date décroissante. Exclure les pages `draft`.
> - **Ligne almanach** : un emplacement pour la date pataphysique du jour (sera rempli au P16) — prévois le conteneur (ex. `<p id="almanach-line">`).
> - **Lien « au hasard »** appelant `randomArticle()`.
> - Prévois aussi un emplacement discret en bas pour **DOM** (sera branché au P15) — par ex. un commentaire `{{/* DOM ici (P15) */}}` ou un `<section id="dom-slot">`.
> - Garde le `{{ define "scripts" }}` mais vide pour l'instant (les scripts almanach/DOM arrivent aux P15/P16).
> Aucune fonte distante, aucun gris, aucune classe Tailwind. Styles dans `site.css`. Vérifie le build. Ne touche pas à `content/`. Commit : `refonte: accueil index typographique`.

**Vérif.** Accueil = texte + listes de liens lisibles, sections et derniers textes présents, build vert.

---

## P13 — Gabarit de liste unifié

**But.** Une liste lisible pour toutes les sections de lecture, en remplaçant les gabarits décorés (jardin de feuilles de solutions-imaginaires, wave cards d'ondes-pixels, table technique de recherches).
**Fichiers.** Créer `layouts/_default/list.html`. Adapter/retirer `layouts/solutions-imaginaires/list.html`, `layouts/ondes-pixels/list.html`, `layouts/recherches/list.html`. (Laisse `rhizome-curieux` et `antenne-radio` pour les P17/P18, et les sorties JSON `list.almanach.json`/`list.rhizome.json` intactes.)

**Prompt à coller :**

> Lis `CLAUDE.md` d'abord. et `00_PLAN.md`.
> Crée un gabarit de liste unifié `layouts/_default/list.html`, type-heavy et sobre, et fais-en hériter les sections de lecture.
> - En haut : titre de la section + le `.Content` du `_index.md` s'il existe (intro de section) — **ne pas** le dénaturer.
> - Liste des entrées : pour chaque page, **titre en lien** (serif), **date** et éventuellement **description** courte, en dessous. Tri par `weight` puis `date` selon la section (respecte l'ordre éditorial actuel — certaines pages n'ont pas de `date` mais un `weight`).
> - **Sous-dossiers** : `solutions-imaginaires` contient des dossiers (adramatiques, blog_corée, cyclo, feuilletons, jeux). Rends-les comme des **regroupements** (un intertitre par dossier, puis ses entrées), pour garder la structure éditoriale lisible. Réutilise la logique de `.Sections`/`.RegularPages` de l'actuel `layouts/solutions-imaginaires/list.html` mais en sortie texte.
> - Remplace les gabarits décorés : supprime le jardin de feuilles de `solutions-imaginaires/list.html`, les wave cards d'`ondes-pixels/list.html`, la table néo-brutaliste de `recherches/list.html` — au profit du gabarit unifié (ou d'overrides minimes qui héritent du défaut). Pour `ondes-pixels`, garde l'accès aux contenus (les embeds sont gérés au P19) ; pour `recherches`, garde les champs utiles (date, description, tags) en texte.
> - Aucune carte décorée, aucune image décorative, aucune classe Tailwind/`ctp-*`. Styles dans `site.css`.
> Vérifie le rendu de chaque section de liste. Ne touche pas à `content/`. Commit : `refonte: gabarit de liste unifié`.

**Vérif.** Chaque section liste ses entrées en texte lisible, l'ordre éditorial est respecté, les sous-dossiers de solutions-imaginaires sont regroupés.

---

## P14 — Tags / thésaurus

**But.** Index des tags et pages de tag en listes sobres.
**Fichiers.** `layouts/_default/taxonomy.html`, `layouts/_default/terms.html`, `assets/css/site.css`. Adapter `layouts/partials/ui/tag-chip.html`.

**Prompt à coller :**

> Lis `CLAUDE.md` d'abord. et `00_PLAN.md`.
> Réécris `layouts/_default/terms.html` (l'index « thésaurus » de tous les tags) et `layouts/_default/taxonomy.html` (la page d'un tag donné) en version texte.
> - `terms.html` : liste alphabétique des tags, chacun en lien, avec son nombre d'entrées (le compte se distingue par la taille/mono, pas par le gris). Garde le titre « thésaurus » et la description existante.
> - `taxonomy.html` : pour un tag, la liste des contenus associés (titre + date + section), en liens texte.
> - Simplifie `layouts/partials/ui/tag-chip.html` en un simple lien de tag souligné (plus de « chip » coloré). Mets à jour son usage si besoin.
> Aucune couleur grise, aucune classe Tailwind. Styles dans `site.css`. Vérifie `/tags/` et une page de tag. Ne touche pas à `content/`. Commit : `refonte: tags/thésaurus en texte`.

**Vérif.** `/tags/` liste les tags ; une page de tag liste ses contenus ; tout est lisible et sans gris.

---

## P14b — 404 minimale

**But.** Restyler la 404 existante (déjà lightweight) au socle `site.css`.
**Fichiers.** `layouts/404.html`.

**Prompt à coller :**

> Lis `CLAUDE.md` d'abord. et `00_PLAN.md`.
> Adapte `layouts/404.html` au nouveau socle : retire les classes Tailwind/`ctp-*`, garde un message sobre « Page introuvable » + quelques liens de secours (accueil, sections principales, recherche, au hasard). Type-heavy, contraste franc, zéro gris, zéro fonte distante. Styles éventuels dans `site.css`. Vérifie le rendu. Commit : `refonte: 404 minimale`.

**Vérif.** La 404 s'affiche proprement avec des liens de secours.

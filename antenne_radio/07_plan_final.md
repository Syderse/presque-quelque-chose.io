# 07 — Plan final : finalisation propre de l'Antenne radio

**Statut :** plan d'exécution, V3 gelée comme point de départ.
**Objectif global :** terminer l'antenne de veille en études radiophoniques pour qu'elle soit (1) **exhaustive** sur les revues du champ, (2) dotée d'un **scoring/filtre abouti** qui écarte le bruit sans perdre les articles intéressants, (3) **zéro-intervention** sauf une commande hebdomadaire lancée à la main, (4) pourvue d'une **interface aboutie et partageable** à des collègues du domaine.

**Décisions prises avec l'auteur (2026-05-24) :**
- Contrat public **enrichi** : ajout de `authors` + `container_title` (nom de revue) + `item_type`, **pour les sources bibliographiques uniquement** (Crossref / OpenAlex / HAL). Les sources éditoriales/journalistiques (blogs RSS) restent au contrat minimal. Conforme à la recommandation du `LEGAL_AUDIT.md`.
- Publication hebdomadaire : commande unique qui **génère + affiche les compteurs + rappelle le `git push` à lancer soi-même**. **Pas d'auto-commit** (doctrine `antenne_radio`).
- **Désactivation de source bruyante** : désactiver la source *La lettre de la radio & du podcast* (`la_lettre_pro`) car elle génère beaucoup trop de bruit dans la base.

---

## Invariants communs à TOUS les prompts

À mettre en tête de chaque prompt, sans réauditer le projet à chaque fois (la mémoire assure la continuité) :

1. **Avant de commencer** : `git status --short`, puis lire `antenne_radio/memoire_materielle.md` (dernier bilan en bas) et ce fichier `07_plan_final.md`. Ne pas relire tout `docs/AGENTS.md` ni `LEGAL_AUDIT.md` en entier — s'y référer seulement en cas de doute.
2. **Interdits absolus** : aucun cron, aucun auto-commit/push, aucune publication de `raw`, `abstract`, logs, scores, `keywords_matched`, chemins locaux ou secrets. Whitelist publique = allowlist stricte (tout champ non listé est interdit).
3. **Secrets** : `CROSSREF_MAILTO` / `OPENALEX_MAILTO` lus uniquement depuis `.env.local` (hors Git), jamais écrits dans le dépôt ni les logs.
4. **Discipline** : petits changements testés et réversibles ; ne jamais masquer un test échoué ; lancer `make test` après toute modif de code ; respecter la philosophie *lightweight* du site (CSS sobre, pas d'animation lourde, pas d'asset inutile).
5. **À la fin de chaque prompt** : ajouter un bilan contextuel daté en bas de `antenne_radio/memoire_materielle.md` (objectif, fichiers modifiés, commandes lancées, compteurs réels, scan anti-fuite, limites, prochaine étape) pour que le prompt suivant reprenne sans réaudit.

---

## Prompt 1 — Couverture exhaustive des revues + scoring abouti

**But :** rendre la veille exhaustive sur le champ et fiabiliser le tri automatique, pour qu'aucune curation manuelle ne soit nécessaire ensuite.

**Contexte (depuis la mémoire) :** sources actives = RSS×9 (après désactivation définitive de *La lettre de la radio & du podcast*), HAL, Crossref (`journal_radio_audio_media`, `radio_journal`, `sound_studies_journal`, `resonance_journal`), OpenAlex (profils + venue JSS). Scoring lexical : poids `radio_core/radio_free=3`, `sound_studies/podcast=2`, `negative_noise=-6`, `technical_radio_noise=-2` ; seuils `to_read≥6`, `candidate≥2`. Dédup DOI inter-sources opérationnelle.

**Tâches :**
1. **Désactiver définitivement la source *La lettre de la radio & du podcast*** (`la_lettre_pro`) : s'assurer qu'elle est marquée inactive (`enabled: false`) dans `config/sources.yaml`, et mettre à jour la documentation (`01_RESSOURCES_SUIVIES.md`, `memoire_materielle.md`) ainsi que les tests correspondants (ex. `test_config.py`).
2. **Compléter la cartographie des revues** du champ et adjacentes, en réutilisant les méthodes déjà éprouvées (Crossref par ISSN, venues OpenAlex par ISSN, profils OpenAlex par mots-clés). Vérifier chaque ISSN avant ajout. Seed à valider/compléter (ne pas dupliquer l'existant) :
   - Études radio/audio : *RadioDoc Review*, *Interference: A Journal of Audio Culture*, *SoundEffects* (open access), *The Senses and Society*, *Organised Sound*, *Twentieth-Century Music*.
   - Médias/communication adjacents (publient régulièrement sur radio/podcast/son) : *Popular Communication*, *Convergence*, *Media, Culture & Society*, *Participations*, *Critical Studies in Television*, *VIEW Journal of European Television History and Culture*, *Feminist Media Studies*.
   - Francophone : *Réseaux*, *Questions de communication*, *Études de communication*, *Communication & langages*, *Volume!*, *Transposition*, *Sociétés & Représentations*. 
   - Réseaux sans flux stable (IAMCR MAR, ECREA Radio & Sound) : **rester hors pipeline** (veille humaine), comme acté en V3.
3. **Stratégie anti-bruit par source** : les revues **mono-thématiques** (radio/son/podcast) → ingestion par revue entière (Crossref/OpenAlex venue). Les revues **généralistes adjacentes** → **profils OpenAlex filtrés par mots-clés** (jamais la revue entière), pour ne pas inonder la base d'articles hors-sujet.
4. **Ajouter les attributions publiques** correspondantes dans `export_public.py` (`AUDITED_ATTRIBUTIONS` + `ATTRIBUTION_BY_SOURCE_NAME`) pour chaque nouvelle source, sans toucher la whitelist.
5. **Scoring abouti** (`scoring.yaml`, `keywords.yaml`, et si besoin `scoring.py`) :
   - Enrichir les listes de mots-clés (FR+EN) pour couvrir les nouveaux champs sans gonfler les faux positifs.
   - Ajouter un **plancher de confiance par source** : un article issu d'une revue cœur du champ (familles `academic_watch`/venues whitelistées) ne doit **jamais** tomber sous `candidate` même si son titre est laconique — tout en gardant la domination des poids négatifs techniques pour le vrai bruit RF/médical.
   - Conserver des seuils explicables ; documenter tout changement de poids dans `scoring.yaml`.
6. **Tests** (`test_config.py`, `test_scoring.py`, `test_export_public.py`) : nouvelles sources verrouillées, plancher de confiance vérifié, bruit technique toujours `ignored`, article interdisciplinaire pertinent jamais perdu, attributions présentes.
7. **Run contrôlé unique** avec `.env.local` : `make run` puis `make export-public`. Relever compteurs réels (`db.json`, export public, dédup DOI = 0 doublon) et **scan anti-fuite**.

**Validation :** `make test` 100 % ; compteurs cohérents ; 0 clé interdite dans `static/antenne-radio/index.json`.

**Fin :** consigner le bilan dans `memoire_materielle.md` (liste finale des revues actives, nouveaux poids/seuils, compteurs, dédup, scan anti-fuite).

---

## Prompt 2 — Contrat public enrichi (auteurs + revue + type) + anti-fuite

**But :** rendre l'index public réellement utile à des chercheurs (notices citables) sans rien céder sur la confidentialité.

**Contexte (depuis la mémoire) :** whitelist actuelle stricte = `id, title, url, doi, published_at, source_name, source_type, language, source_family, attribution_id`. Décision : ajouter `authors`, `container_title`, `item_type` pour les **sources bibliographiques uniquement**.

**Tâches :**
1. **Étendre `PUBLIC_ITEM_KEYS`** dans `export_public.py` avec `authors`, `container_title`, `item_type`.
2. **Règle bibliographique vs éditoriale** : peupler ces champs uniquement quand `source_family ∈ {crossref, openalex, hal}` (notices bibliographiques). Pour les RSS éditoriaux/journalistiques, ces champs restent **absents ou vides** (le `LEGAL_AUDIT` limite ces sources à titre+url+date+source).
   - `authors` : depuis `item.authors` (déjà privé en base), liste de noms simples, **avec regex anti-fuite e-mail** (nettoyage des adresses accidentellement capturées, cf. audit).
   - `container_title` : nom de la revue (depuis le nom de source canonique / champ revue privé), pas la plateforme.
   - `item_type` : dérivé de `source_type` (journal_article, book, chapter, thesis…).
3. **Modèle** : si `container_title` n'existe pas encore dans `RadioWatchItem`/normalisation, l'ajouter en champ privé renseigné par les normaliseurs Crossref/OpenAlex/HAL (sans casser la dédup).
4. **Anti-fuite renforcé** : `FORBIDDEN_PUBLIC_KEYS` et `_assert_no_forbidden_keys` continuent de bloquer `abstract`, `raw`, scores, `keywords_matched`, etc. Vérifier que `authors` ne réintroduit aucune donnée sensible.
5. **Tests** (`test_export_public.py`) : whitelist = exactement les 13 clés ; sources éditoriales sans `authors`/`container_title` ; bibliographiques avec ; anti-fuite e-mail ; aucune clé interdite ; item OpenAlex/Crossref public sans score ni abstract.
6. **Doc** : mettre à jour la section « Contrat public de données » de `LEGAL_AUDIT.md` (nouveaux champs autorisés + justification + restriction aux sources bibliographiques).
7. **Régénérer** `make export-public` et **scanner** l'index + le HTML buildé.

**Validation :** `make test` 100 % ; index régénéré conforme ; scan anti-fuite 0 clé interdite, 0 e-mail, 0 chemin local.

**Fin :** consigner le bilan dans `memoire_materielle.md` (nouvelles clés, règle biblio/éditoriale, compteurs, résultat scan).

---

## Prompt 3 — Interface Hugo aboutie et partageable

**But :** une page `/antenne-radio/` claire, dense et pratique, prête à être partagée à des collègues, dans le respect *lightweight*.

**Contexte (depuis la mémoire) :** `layouts/antenne-radio/list.html` (cartes néo-brutalistes, lecture build-time du JSON, fallback `<noscript>` 50 items) + `assets/js/antenne-radio.js` (recherche, filtres source_type/source/langue, deep-linking `q/cat/src/lang`, pagination par 50). Catppuccin Mocha.

**Tâches :**
1. **Afficher les nouveaux champs** : auteurs, revue (`container_title`), type bibliographique sur chaque carte, proprement et lisiblement, avec dégradation gracieuse quand le champ est vide (sources éditoriales).
2. **Tri** : ajouter un contrôle de tri (date décroissante par défaut, date croissante, titre A→Z). Ne jamais exposer le score interne.
3. **Filtre par période** : filtre par année/fenêtre (cohérent avec la rétention 18 mois), synchronisé au deep-linking.
4. **Bloc « À propos / contact / retrait »** (exigence Go-Live du `LEGAL_AUDIT`) : finalité académique et non commerciale, absence de revendication de PI sur les notices, adresse de contact pour toute demande de retrait, mention des attributions/sources.
5. **Lightweight** : pas de `transition-all`, pas de `will-change` permanent, pas de gros filtres/flous ; transitions limitées à `transform`/couleurs/bordures ; JS chargé seulement sur cette page (`js-loader.html`).
6. **Accessibilité & mobile** : labels ARIA sur contrôles, focus géré, test viewport 390×844 sans débordement horizontal, fallback `<noscript>` toujours valide.

**Validation :** `pnpm run build` OK ; rendu desktop + mobile vérifié ; HTML final sans JSON sensible embarqué.

**Fin :** consigner le bilan dans `memoire_materielle.md` (champs affichés, contrôles ajoutés, résultat build, points UX restants).

---

## Prompt 4 — Routine hebdo zéro-intervention + rétention + recette finale + gel

**But :** réduire la veille à **une seule commande hebdomadaire** lancée à la main, borner la base à 18 mois, puis figer le projet.

**Contexte (depuis la mémoire) :** `make run` (récolte) et `make export-public` existent ; build via `pnpm run build` à la racine ; déploiement Netlify sur `git push`. Pruning 18 mois jamais implémenté.

**Tâches :**
1. **Commande hebdo unique** `make weekly` (dans `antenne_radio/Makefile`) :
   - charge `.env.local`, lance la récolte, l'export public, puis (optionnel) un build local de vérification ;
   - affiche un **récapitulatif** : compteurs `db.json` (par statut), nombre d'items publics, nb de sources, 0 doublon DOI ;
   - lance un **scan anti-fuite rapide** sur l'index public et échoue bruyamment si une clé interdite/e-mail apparaît ;
   - **n'effectue aucun commit/push** : termine en imprimant les commandes `git` exactes à lancer soi-même pour publier (geste conscient).
2. **Rétention 18 mois** (principe d'impermanence) : élaguer de `db.json` les items dont la date dépasse 18 mois, **sauf `status == exported`** (ne jamais écraser une décision humaine de curation). Implémenter dans le pipeline avec tests dédiés (un item récent conservé, un ancien non-exporté élagué, un ancien `exported` conservé).
3. **Documentation** : section « Routine hebdomadaire » dans `README.md` (une commande, lecture des compteurs, push manuel) ; mettre à jour `01_RESSOURCES_SUIVIES.md` (sources finales, statuts) et la note de clôture de `LEGAL_AUDIT.md`.
4. **Recette finale complète** avec `.env.local` : `make test` → `make weekly` → push manuel → vérifier le build Netlify. Relever tous les compteurs réels et refaire un **scan anti-fuite exhaustif** (index statique + HTML buildé : 0 clé interdite, 0 e-mail, 0 chemin local, faux positifs documentés).
5. **Gel** : marquer le projet terminé dans `memoire_materielle.md` et `docs/CHANTIERS.md`.

**Validation :** `make test` 100 % ; `make weekly` reproductible et lisible ; rétention testée ; scan final propre ; build OK.

**Fin :** consigner le bilan final dans `memoire_materielle.md` (commande hebdo, règle de rétention, compteurs finaux, scan, état « projet finalisé »).

---

## Note sur le nombre de prompts

Quatre prompts séquentiels, chacun autonome et testable, reliés par le bilan en fin de `memoire_materielle.md` :

1. **Données & scoring** (exhaustivité + anti-bruit) →
2. **Contrat public enrichi** (notices citables + anti-fuite) →
3. **Interface** (affichage des nouveaux champs + UX + à-propos) →
4. **Routine hebdo + rétention + recette finale + gel**.

L'ordre est contraint : l'interface (3) a besoin des champs publics (2), qui ont besoin des données complètes (1) ; la recette finale (4) clôt l'ensemble. Fusionner davantage mêlerait des changements à risque (contrat juridique + refonte UI dans un même prompt), au détriment de la propreté et de la réversibilité exigées par la doctrine.

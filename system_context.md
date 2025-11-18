SYSTEM CONTEXT & ARCHITECTURE

Projet : Presque Quelque Chose

Dernière mise à jour : 18 Novembre 2025
Statut : En développement actif
Type : Blog expérimental, Portfolio Hybride & Almanach 'Pataphysique

1. IDENTITÉ & VISION

Nom du projet : Presque Quelque Chose.

URL Actuelle : presque-quelque-chose.io (Hébergé sur Netlify).

URL Cible : presque-quelque-chose.com.

Concept : Un site de documentation personnelle et créative, intégrant des concepts de 'Pataphysique (calendrier, esthétique).

Esthétique Clé :

Thème sombre/clair avec couleurs spécifiques (Laiton, Sang séché, Cyan, Magenta).

Curseur personnalisé (Fourmi 🐜).

Titres et liens en dégradés animés.

Structure en "Almanach" quotidien.

2. ENVIRONNEMENT TECHNIQUE (La Machine)

Ce projet nécessite un environnement spécifique pour compiler les assets (images WebP et CSS Tailwind v4).

Machine : Apple Silicon (M1/M2/M3 - arm64).

Système : macOS.

Moteur (Vital) : Hugo Extended v0.152.2+ (La version "Extended" est OBLIGATOIRE).

Langage : Go 1.25.4 (Gère les modules Hugo).

Runtime JS : Node.js v25.2.1.

Package Manager : pnpm v10.14.0 (Utilisé pour la rapidité et l'économie d'espace).

Git : v2.39.5.

3. ARCHITECTURE LOGICIELLE (Le Moteur)

Stack

Base : Hugo Blox (Template "Blog Starter").

CSS Framework : Tailwind CSS v4 (Configuration avancée).

Modules : Gérés via hugo.yaml et go.mod.

La "Solution Radicale v3.2" (Gestion du Style)

Le site utilise une configuration Tailwind v4 forcée manuellement pour contourner les limitations du thème standard.

Fichier maître : tailwind.config.js.

Mécanisme : Le plugin @tailwindcss/typography est câblé manuellement dans la config JS pour appliquer les couleurs 'Pataphysiques à la prose (italiques verts, citations oranges, etc.).

Overrides CSS :

Les styles globaux et animations (dégradés, curseur fourmi) sont définis dans <style> à l'intérieur de layouts/baseof.html.

C'est un override critique : ne pas supprimer ce bloc <style> sans précaution.

Structure des Dossiers Clés

content/ : Tout le contenu rédactionnel (Markdown).

almanach/ : Entrées journalières (une page par jour).

solutions-imaginaires/ : Contenu créatif et fictionnel.

layouts/ : Les fichiers HTML qui structurent le site (contient les overrides critiques).

static/ : Fichiers servis tels quels (PDFs, JS pur).

js/PataphysicalDate.js : Script du calendrier.

_vendor/ : Dossier généré par hugo mod vendor (contient le code du thème téléchargé).

4. SCRIPTS & FONCTIONNALITÉS "MAISON"

A. Le Calendrier 'Pataphysique

Fichiers : static/js/PataphysicalDate.js et static/data/pataphysique_custom.json.

Fonction : Convertit la date grégorienne en date 'Pataphysique affichée sur le site.

État : Fonctionnel.

5. WORKFLOW DE DÉVELOPPEMENT

Dépôt & Déploiement

Repo GitHub : https://github.com/Syderse/presque-quelque-chose.io

Hébergeur : Netlify.

Mode : Continuous Deployment (CD). Chaque git push sur la branche main déclenche une mise à jour du site.

Commandes Quotidiennes (Terminal)

Lancer le site en local :

hugo server -D


(Note : Pas besoin de npm run dev avec cette config Tailwind v4, Hugo gère tout).

Mettre à jour les dépendances (si besoin) :

pnpm install
hugo mod get -u
hugo mod tidy

6. DOCUMENTATION DES COULEURS (Charte)

Les couleurs sont définies en dur dans tailwind.config.js et layouts/baseof.html.

Primaire (Laiton) : Gamme #c09f61 (Gold/Bronze).

Secondaire (Sang) : Gamme #a96a6a (Rouge sombre).

Italique : #008000 (Vert naturel).

Citations : #E67E22 (Orange).

Animations : Cycle Magenta (#CC00CC) -> Cyan (#00CCCC).

7. Gestion de mes conversations avec toi (Gemini)

Quand je dis "initie le prompt de réamorçage", produis un prompt suivant ce modèle : Bonjour Gemini.

Notre session de travail actuelle arrive à son terme. Pour garantir une reprise efficace lors de notre prochaine conversation, ta mission est de générer un "prompt de réamorçage" complet et structuré.

Ce prompt me servira à démarrer une nouvelle conversation avec toi, en te fournissant immédiatement tout le contexte nécessaire.

Pour cela, tu vas analyser et synthétiser l'intégralité de notre conversation actuelle.

Le prompt que tu vas générer doit impérativement suivre la structure suivante, en remplissant chaque section avec les informations pertinentes issues de nos échanges :

1. Objectif Global :

    Résume en une phrase le but final de mon projet (par exemple, "Mettre en place une section d'articles similaires fonctionnelle").

2. Le Problème Spécifique Actuel :

    Décris le point de blocage exact où nous nous sommes arrêtés.

3. Résumé des Tentatives et Apprentissages :

    Liste de manière chronologique les différentes approches que nous avons testées.

    Pour chaque tentative, mentionne le code que nous avons utilisé et le résultat obtenu (succès partiel, erreur, etc.).

    Ceci est crucial pour ne pas refaire les mêmes erreurs.

4. Contexte Technique Établi :

    Rappelle les informations techniques confirmées : version de Hugo, nom du thème, structure des fichiers, etc.

5. État Actuel des Fichiers Clés :

    Présente la version la plus récente et pertinente des fichiers sur lesquels nous travaillions (par exemple, layouts/_default/single.html, layouts/partials/related.html, config.toml, etc.). Affiche le code complet de ces fichiers dans leur état actuel.

6. Prochaine Étape / Demande Claire :

    Formule la question ou la demande précise pour la nouvelle conversation. Que devons-nous faire ou résoudre au début de la prochaine session ?

L'objectif final est que je puisse simplement copier-coller l'intégralité de ta réponse pour lancer notre prochaine session de travail de manière fluide et sans perte de temps.

Génère maintenant ce prompt de réamorçage.

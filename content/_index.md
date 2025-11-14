---
title: 'home'
date: 2023-10-24
type: landing
sections:
  - block: resume-biography
    content:
      username: admin
    design:
      spacing:
        padding: [0, 0, 0, 0]
      biography:
        style: 'text-align: justify; font-size: 0.8em;'
      avatar:
        size: medium
        shape: circle
  # --- INDEX EN GRILLE ---
  - block: markdown
    id: index
    content:
      title: "" # Pas de titre pour ce bloc
      subtitle: ""
      text: |
        <style>
          .section-index-grid {
            display: grid;
            /* Crée des colonnes automatiques (min 150px, max 1fr) */
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1.5rem;
            text-align: center;
          }
          .section-index-grid a {
            display: block;
            padding: 1.5rem 1rem;
            border: 1px solid var(--tw-prose-borders);
            border-radius: 0.5rem;
            transition: all 0.2s ease-in-out;
            text-decoration: none;
            font-weight: 500;
          }
          .section-index-grid a:hover {
            background-color: var(--tw-prose-invert-bg);
            color: var(--tw-prose-invert-body);
            border-color: var(--tw-prose-invert-borders);
            transform: translateY(-2px);
          }
        </style>
        
        <div class="section-index-grid">
          <a href="/#inutilites-appliquees">inutilités appliquées</a>
          <a href="/#solutions-imaginaires">solutions imaginaires</a>
          <a href="/#parcours">parcours académique</a>
          <a href="/#ondes-et-pixels">ondes & pixels</a>
          <a href="/#agenda-inoccupations">l'agenda</a>
        </div>
  # --- feed 1: inutilités ---
  - block: collection
    id: inutilites-appliquees
    content:
      title: "inutilités appliquées"
      filters:
        folders:
          - non-fiction  # corrigé
    design:
      view: card
      spacing:
        padding: ['3rem', 0, '6rem', 0]

  # --- feed 2: fiction ---
  - block: collection
    id: solutions-imaginaires
    content:
      title: "solutions imaginaires"
      subtitle: "scènes, poèmes, chansons et autres clinamens"
      filters:
        folders:
          - fiction
    design:
      view: card 
      spacing:
        padding: ['3rem', 0, '6rem', 0]

  # --- feed 3: académique ---
  - block: collection
    id: parcours
    content:
      title: "parcours académique"
      subtitle: "recherches en histoire de l'art, cinéma et radio"
      filters:
        folders:
          - parcours
    design:
      view: citation 
      spacing:
        padding: ['3rem', 0, '6rem', 0]

  # --- feed 4: media ---
  - block: collection
    id: ondes-et-pixels
    content:
      title: "ondes & pixels"
      subtitle: "podcasts, vidéos et expérimentations audiovisuelles"
      filters:
        folders:
          - media
    design:
      view: card  # <-- corrigé (showcase n'existe pas)
      spacing:
        padding: ['3rem', 0, '6rem', 0]

  # --- feed 5: agenda ---
  - block: collection
    id: agenda-inoccupations
    content:
      title: "l'agenda des inoccupations"
      subtitle: "recensement des flâneries et non-rendez-vous à venir"
      filters:
        folders:
          - agenda
    design:
      view: date-title-summary # <-- corrigé (compact n'existe pas)
      spacing:
        padding: ['3rem', 0, '6rem', 0]
---
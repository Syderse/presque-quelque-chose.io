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
    id: almanach-inoccupations
    content:
      title: "l'agenda des inoccupations"
      subtitle: "recensement des flâneries et non-rendez-vous à venir"
      filters:
        folders:
          - almanach
    design:
      view: date-title-summary # <-- corrigé (compact n'existe pas)
      spacing:
        padding: ['3rem', 0, '6rem', 0]
---
---
title: 'Home'
date: 2023-10-24
type: landing
sections:
  - block: resume-biography
    content:
      # The user's folder name in content/authors/
      username: admin
    design:
      spacing:
        padding: [0, 0, 0, 0]
      biography:
        style: 'text-align: justify; font-size: 0.8em;'
      # Avatar customization
      avatar:
        size: medium  # Options: small (150px), medium (200px, default), large (320px), xl (400px), xxl (500px)
        shape: circle # Options: circle (default), square, rounded
  
  - block: collection
    id: inutilités-appliquées  # Un ID si vous voulez un lien de menu /#cabinet-des-merveilles
    content:
      title: "inutilités appliquées"
      filters:
        folders:
          - non-fiction  
    design:
      # Amusez-vous à changer 'card' !
      # Essayez 'showcase', 'compact', 'list', ou même 'citation'
      view: card
      spacing:
        padding: ['3rem', 0, '6rem', 0]
  - block: collection
    id: solutions-imaginaires
    content:
      title: "solutions imaginaires"
      subtitle: "Scènes, poèmes, chansons et autres clinamens"
      filters:
        folders:
          - fiction  # <-- Le dossier à créer
    design:
      view: card # 'card' est bien, 'list' serait plus sobre.
      spacing:
        padding: ['3rem', 0, '6rem', 0]
  - block: collection
    id: parcours
    content:
      title: "phynance intellectuelle"
      subtitle: "Recherches en histoire de l'art, cinéma et radio"
      filters:
        folders:
          - parcours # <-- Le dossier à créer
    design:
      view: citation # <-- Une vue parfaite pour l'académique
      spacing:
        padding: ['3rem', 0, '6rem', 0]
  - block: collection
    id: ondes-et-pixels
    content:
      title: "ondes & pixels"
      subtitle: "Podcasts, vidéos et expérimentations audiovisuelles"
      filters:
        folders:
          - media # <-- Le dossier à créer
    design:
      view: showcase # <-- Très visuel, parfait pour des vignettes
      spacing:
        padding: ['3rem', 0, '6rem', 0]
  - block: collection
    id: agenda-inoccupations
    content:
      title: "Inoccupations impersonnelles"
      subtitle: "Recensement des flâneries et non-rendez-vous à venir"
      filters:
        folders:
          - agenda # <-- Le dossier à créer
    design:
      view: compact # <-- Style compact, comme un vrai agenda
      spacing:
        padding: ['3rem', 0, '6rem', 0]
---
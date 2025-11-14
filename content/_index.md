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
    id: cabinet-des-merveilles  # Un ID si vous voulez un lien de menu /#cabinet-des-merveilles
    content:
      title: "Le Cabinet des Merveilles"
      subtitle: "Explorations 'pataphysiques et autres singularités"
      filters:
        folders:
          - post  
    design:
      # Amusez-vous à changer 'card' !
      # Essayez 'showcase', 'compact', 'list', ou même 'citation'
      view: card
      spacing:
        padding: ['3rem', 0, '6rem', 0]
---
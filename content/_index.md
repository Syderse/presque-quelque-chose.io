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
  - block: collection
    id: almanach
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
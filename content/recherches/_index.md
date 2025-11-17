---
title: Mes Recherches
date: 2025-06-15
type: landing

sections:
  - block: collection
    id: publications
    content:
      title: Publications
      filters:
        # Ce bloc va chercher tout ce qui est dans le dossier "publication"
        folders:
          - publication
        exclude_featured: false
    design:
      # "card" affiche une belle carte avec l'image.
      # Si tu n'as pas d'image, remplace "card" par "compact".
      view: card
      columns: '2'
---
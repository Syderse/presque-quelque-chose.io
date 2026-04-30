---
title: "Almanach API"
type: "almanach"
# C'est la ligne critique : on interdit le HTML ici.
outputs: ["ALMANACH"] 
build:
  render: always      # On veut générer le fichier (JSON)
  list: never         # On ne veut pas que cette "page" apparaisse dans les listes d'articles
  publishResources: false
---

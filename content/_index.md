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

  #
  # <--- NOUVEAU BLOC : LE MANIFESTE --->
  #
  - block: markdown
    id: manifeste
    content:
      title: "ceci n'est (presque) pas un site"
      text: |
        > _"la 'pataphysique est la science des solutions imaginaires, qui accorde symboliquement aux linéaments les propriétés des objets décrits par leur virtualité."_ 
        >
        > — alfred jarry
        
        <br>
        
        **bienvenue.** cet espace est un laboratoire pour les exceptions, un catalogue d'inoccupations, et une humble tentative de défier le minimalisme ambiant.
    design:
      # On centre le texte pour un effet "manifeste"
      css_style: 'text-align: center;'
      spacing:
        padding: ["2rem", 0, "1rem", 0] # Un peu d'air

  #
  # <--- NOUVEAU BLOC : LES PRINCIPES --->
  #
  - block: features
    id: principes
    content:
      title: "quelques principes directeurs"
      items:
        - name: 'la spirale'
          description: 'pour la récurrence et le vertige.'
          icon: '🌀' 
          icon_pack: 'emoji' # On dit à Hugo Blox que c'est un emoji
        - name: 'la fourmi'
          description: 'pour le travail méticuleux et absurde.'
          icon: '🐜'
          icon_pack: 'emoji'
        - name: 'l''alambic'
          description: 'pour distiller l''exception en règle.'
          icon: '⚗️'
          icon_pack: 'emoji'
    design:
      columns: '3'
      # On force les minuscules, car ce bloc n'est pas "prose"
      css_style: 'text-transform: lowercase;'
      spacing:
        padding: ["1rem", 0, "2rem", 0] # Un peu d'air


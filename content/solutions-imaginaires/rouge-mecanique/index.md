---
title: bulbe rouge
description: test visuel
color: red
---

ce bulbe a le malheur d'être le premier. le seul de son genre pour l'instant. mais il sert désormais de **pierre angulaire** {{< sidenote "Structure" >}}Une fondation instable est souvent la meilleure garantie d'une croissance organique imprévisible, typique de l'architecture Rhizome.{{< /sidenote >}} pour vérifier la solidité de l'édifice. voici le protocole de test complet de la *charte graphique catppuccin*.

## niveau 2 : la structure du terrier {{< sidenote "Layout" >}}La profondeur sémantique ne doit jamais compromettre la lisibilité. Vérifier l'alignement vertical sur mobile.{{< /sidenote >}}

l'architecture doit supporter des niveaux de titres profonds sans perdre le fil.

### niveau 3 : les détails techniques

voici un paragraphe standard pour tester le corps de texte. il doit être lisible, avec un contraste suffisant (`text-ctp-text`) {{< sidenote "Accessibilité" >}}Le ratio de contraste sur le fond ctp-base doit être validé WCAG AA au minimum.{{< /sidenote >}} et une hauteur de ligne confortable (line-height 1.8). nous testons ici le **gras (bold)** pour l'emphase forte (couleur peach), l'*italique (em)* pour la nuance (couleur green) {{< sidenote "Typo" >}}L'italique doit utiliser la variante Display de la police si disponible pour maximiser l'impact visuel.{{< /sidenote >}}, et parfois ***les deux combinés*** pour crier en silence. n'oublions pas le ~~texte barré~~ pour les erreurs passées et le [lien hypertexte standard](/) qui doit être souligné et réagir au survol.

#### niveau 4 : plus profond dans le code

les développeurs ont besoin de voir du code. le `code en ligne` {{< sidenote "Micro-IX" >}}Le survol du code en ligne doit déclencher un changement de fond subtil (ctp-surface0).{{< /sidenote >}} doit ressembler à une petite puce (chip) avec une bordure et une ombre légère, comme défini dans le css.

{{< sidenote "Syntaxe" >}}Ce bloc JavaScript teste le rendu des commentaires et des mots-clés réservés avec la palette Mocha.{{< /sidenote >}}

j'aime {{< sidenote >}}test de la nouvelle fonction sn{{< /sidenote >}}
{{< sidenote >}}Contenu{{< /sidenote >}}

```javascript
// bloc de code : javascript
// vérification de la coloration syntaxique
const rhizome = {
  etat: "connecté",
  noeuds: 42,
  init: function() {
    console.log("le système est opérationnel");
  }
};

---
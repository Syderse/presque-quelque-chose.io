---
title: "Cartes créatures"
weight: 70
tags:
  - jeu de rôle
  - scénario
hide_footer: true
full_width: false
---

<style>
/* Fiches imprimables : feuille A4, rendu sobre et autonome. Aucune dépendance
   au thème global ; uniquement des variables locales. */
.rpg-print-sheets {
  --sheet-bg: #fff;
  --sheet-ink: var(--fg);
  --sheet-muted: var(--fg);
  --sheet-line: var(--rule);
  --sheet-soft: var(--code-bg);
  --sheet-accent: var(--fg-strong);
  color: var(--sheet-ink);
  max-width: 210mm;
  margin: 0 auto 4rem;
}
/* Sur écran, les fiches débordent la colonne de lecture (66ch). */
main:has(.rpg-print-sheets),
.article-prose:has(.rpg-print-sheets) {
  max-width: min(210mm, calc(100vw - 2rem));
  width: 100%;
}
.rpg-print-sheets :where(p, li, blockquote) {
  text-align: start;
  text-align-last: auto;
}
.rpg-print-sheets :where(th, td) {
  border-color: var(--sheet-line);
}
.rpg-print-sheets :where(thead th) {
  background-color: var(--sheet-soft);
}
.rpg-print-intro {
  text-align: center;
  margin: 0 auto 1.5rem;
  color: var(--sheet-ink);
}
.rpg-print-intro h1,
.rpg-print-intro p {
  margin: 0;
}
.rpg-sheet-page {
  box-sizing: border-box;
  min-height: 270mm;
  margin: 0 auto 1.5rem;
  padding: 12mm;
  break-after: auto;
  page-break-after: auto;
  border: 1px solid var(--sheet-line);
  background: var(--sheet-bg);
  box-shadow: 6px 6px 0 var(--sheet-line);
}
.rpg-sheet-page:last-child {
  break-after: auto;
  page-break-after: auto;
}
.rpg-sheet-page h2,
.rpg-sheet-page h3,
.rpg-sheet-page p,
.rpg-sheet-page table,
.rpg-sheet-page ul,
.rpg-sheet-page ol {
  color: var(--sheet-ink);
}
.rpg-sheet-title {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 1rem;
  border-top: 3px solid var(--sheet-line);
  border-bottom: 1px solid var(--sheet-line);
  padding: 0.35rem 0 0.3rem;
  margin-bottom: 0.75rem;
}
.rpg-sheet-title h2 {
  color: var(--sheet-accent) !important;
  margin: 0;
  font-size: 1.55rem;
  line-height: 1;
}
.rpg-sheet-title span {
  color: var(--sheet-muted) !important;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.creature-card {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  font-size: 11pt;
  line-height: 1.34;
}
.creature-card .creature-description {
  font-size: 10.5pt;
  margin: 0;
}
.creature-card table,
.character-sheet table {
  width: 100%;
  border-collapse: collapse;
  margin: 0;
  font-size: 0.9em;
}
.creature-card th,
.creature-card td,
.character-sheet th,
.character-sheet td {
  border: 1px solid var(--sheet-line);
  padding: 0.28rem 0.35rem;
  text-align: center;
}
.rpg-box {
  border: 1px solid var(--sheet-line);
  background: color-mix(in srgb, var(--sheet-soft) 84%, transparent);
  padding: 0.55rem 0.65rem;
}
.rpg-box h3 {
  color: var(--sheet-accent) !important;
  margin: 0 0 0.35rem;
  padding-bottom: 0.18rem;
  border-bottom: 1px solid var(--sheet-line);
  font-size: 0.95rem;
  text-transform: uppercase;
}
.rpg-box p {
  margin: 0.22rem 0;
}
@media print {
  @page { size: A4 portrait; margin: 10mm; }

  html,
  body {
    width: 190mm !important;
    max-width: 190mm !important;
    height: auto !important;
    min-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: visible !important;
    background: #fff !important;
    color: #111 !important;
  }

  /* Tout le chrome du site disparaît à l'impression. */
  body:has(.rpg-print-sheets) .site-header,
  body:has(.rpg-print-sheets) .site-footer,
  body:has(.rpg-print-sheets) .breadcrumb,
  body:has(.rpg-print-sheets) .article-header,
  body:has(.rpg-print-sheets) .article-toc,
  body:has(.rpg-print-sheets) .toc-btn,
  body:has(.rpg-print-sheets) .toc-float-panel,
  body:has(.rpg-print-sheets) .article-attachment {
    display: none !important;
  }

  body:has(.rpg-print-sheets) main,
  body:has(.rpg-print-sheets) .article-prose {
    position: static !important;
    display: block !important;
    box-sizing: border-box !important;
    width: 190mm !important;
    max-width: 190mm !important;
    min-width: 0 !important;
    height: auto !important;
    min-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: visible !important;
    transform: none !important;
    animation: none !important;
    opacity: 1 !important;
    background: #fff !important;
    color: #111 !important;
  }

  .rpg-print-sheets {
    --sheet-bg: #fff !important;
    --sheet-ink: #111 !important;
    --sheet-muted: #444 !important;
    --sheet-line: #222 !important;
    --sheet-soft: #fff !important;
    --sheet-accent: #111 !important;
    width: 190mm !important;
    max-width: 190mm !important;
    margin: 0 !important;
  }
  .rpg-print-intro {
    display: none !important;
  }
  .rpg-sheet-page {
    box-sizing: border-box;
    width: 190mm;
    min-height: 0;
    height: 270mm;
    margin: 0 !important;
    padding: 0 !important;
    border: 0 !important;
    box-shadow: none !important;
    background: #fff !important;
    overflow: hidden;
  }
  .rpg-box {
    break-inside: avoid;
    page-break-inside: avoid;
  }
  .rpg-print-sheets :where(h1, h2, h3, h4, h5, h6, p, li, table, th, td, strong, b, em, i) {
    color: #111 !important;
  }
  .rpg-print-sheets :where(thead th) {
    background: #fff !important;
  }
  .rpg-sheet-page + .rpg-sheet-page {
    break-before: page;
  }
}
</style>
<div class="rpg-print-sheets creature-sheets">

<div class="rpg-print-intro">

# BESTIAIRE

</div>

<section class="rpg-sheet-page creature-card">

<div class="rpg-sheet-title">

## BISON-CREUSET

<span>créature</span>

</div>

<p class="creature-description">Herbivore grégaire aux allures de bison, dont la peau évoque une croûte de sédiments cuits. De longues fissures parcourent ses flancs ; par endroits, une lueur sourde pulse sous la carapace. De petites créatures glabres, morphologiquement proches de l'adulte, circulent entre ses replis et déposent au sol des sphères aux reflets changeants.</p>

| PV | FOR | RES |
| --- | --- | --- |
| 22 | 4 | 4 |


<div class="rpg-box">

### Combat

**Comportement :** Passif par défaut. Charge si blessé. Ou si cri d'alterte d'un petit.

**Attaques :** Charge électrique (arc statique, zone) • Piétinement massif (personne touchée malus jet -2 prochain tour.)

**Défenses :** Cuirasse chitine+roche (immunité armes légères) • Chaleur corporelle intense (immunisé au feu)

</div>


<div class="rpg-box">

### Loot

**Sphère galvanique** : batterie bio, connexion possible à l'Anguille-câble, lampe brute, surcharge magnétique. Chauffe si mal isolée. À récupérer sur une sphère déposée par un petit associé au bison-creuset.

</div>


</section>

<section class="rpg-sheet-page creature-card">

<div class="rpg-sheet-title">

## PAGURE GÉANT

<span>créature</span>

</div>

<p class="creature-description">Formation calcaire ambulante de la taille d'un véhicule, portée par une douzaine de pattes trapues qui disparaissent sous la masse. L'ensemble progresse avec une lenteur imperturbable, broyant sans distinction tout ce qui se trouve sur sa trajectoire. Aucun stimulus extérieur observé n'a jamais provoqué le moindre écart de route.</p>

| PV | FOR | RES | AGI | Régén |
| --- | --- | --- | --- | --- |
| 9999 | 10 | 10 | 0 | Récupération complète si on ne lui retire pas 80% de PV en un coup |


<div class="rpg-box">

### Combat

**Comportement :** Pacifique mais implacable.

**Attaques :** Gifle Molle (1 PV, repousse 2m) • Piétinement inexorable • Mode furieux (×2 vitesse après fusée)

**Défenses :** Carapace indestructible • Régén instantanée • Imperturbabilité totale

</div>


<div class="rpg-box">

### Loot

**Plaque chitine-béton** : plaque rigide, renfort de base ou support de montage. Extrêmement lourd.

</div>


</section>

<section class="rpg-sheet-page creature-card">

<div class="rpg-sheet-title">

## TISSEUR CHIRURGICAL

<span>créature</span>

</div>

<p class="creature-description">Arthropode décharné évoquant une araignée de mer, locomotion assurée par huit pattes-aiguilles d'os articulé. L'abdomen translucide contient un liquide soyeux en perpétuel mouvement. Le spécimen manifeste une obsession remarquable pour la symétrie : déplacements, toiles et gestes répètent des motifs parfaitement géométriques, ponctués d'un cliquetis rapide et mécanique.</p>

| PV | FOR | RES |
| --- | --- | --- |
| 9 | 3 | 1 |


<div class="rpg-box">

### Combat

**Comportement :** Neutre sauf si quelqu'un saigne ou si ouverture détectée → frénésie de réparation.

**Attaques :** Suture d'urgence (+1d4 PV mais 1d6 dégâts douleur + -DEX) • Bâillon (coud lèvres) • Cocon de stase (immobilise, FOR 15)

**Défenses :** Extrêmement agile • Esquive instinctive

</div>


<div class="rpg-box">

### Loot

**Bobine bio-fil** : suture auto-réussie ou corde ultra-fine. Condition : tuer ou capturer.

**Aiguilles articulées** : pointes perforantes, crochetage fin. Condition : tuer ou capturer.

**Glande à soie** : réserve de fil organique. Condition : capturer vivant, piège ou gel.

**Arc-Suture** : récupéré directement sur l'araignée-suture. Arme à distance, +3 AGI. Peut tirer sur les alliés pour les soigner de 1d3 ; sur échec, le tir blesse de 1 DMG brut.

</div>


</section>

<section class="rpg-sheet-page creature-card">

<div class="rpg-sheet-title">

## CRABE-FOREUR-CAFARD

<span>créature</span>

</div>

<p class="creature-description">Prédateur blindé et surbaissé, hybridant des traits de crustacé et de blattoptère. Les mandibules antérieures tournent sur elles-mêmes comme des mèches de foreuse ; une queue segmentée se dresse à l'arrière, terminée par un dard courbe. L'animal sécrète une bave épaisse qui ronge la matière organique au contact.</p>

| PV | FOR | RES |
| --- | --- | --- |
| 16 | 3 | 5 |


<div class="rpg-box">

### Combat

**Comportement :** Fonce et perce, tente coincer dans angles.

**Attaques :** Aspiration sang (regagne 2 PV) • Dard foreur (abîme armure) • Jet bile acide (flaques : jet d'AGI à réussir lors de l'attaque pour éviter de mettre pieds dedans) • Queue scorpion (paralyse 2 tours mais une seule fois par combat)

**Défenses :** Carapace supérieure invulnérable • Attaquer face+dos simultanément

</div>


<div class="rpg-box">

### Loot

**Carapace dorsale** : plaque lourde, base de cuirasse ou renfort robot. Très lourd.

**Dard foreur** : outil de forage, perce carapace et matériaux mous. Toxine instable.

**Mandibules** : cisailles, coupe métal/câbles. Bruyantes.

**Glandes acides** : 3 grenades corrosives. Fuite si mal stockée.

</div>


</section>

<section class="rpg-sheet-page creature-card">

<div class="rpg-sheet-title">

## VÉLOCIRAPTOR SOLAIRE

<span>créature</span>

</div>

<p class="creature-description">Bipède nerveux de gabarit moyen dont le thorax arbore deux défenses d'ivoire courbes. La queue se déploie en éventail d'écailles chromées que l'animal oriente avec précision, captant et redirigeant la lumière ambiante. Observé exclusivement en groupe ; aucun spécimen isolé n'a jamais été recensé.</p>

| PV | FOR | RES | Nombre |
| --- | --- | --- | --- |
| 8 | 2 | 2 | 4 (mini-meute) |


<div class="rpg-box">

### Combat

**Comportement :** N'attaquent JAMAIS seuls. Encerclent pour isoler.

**Attaques :** Serres acérées (Ignore 2 RES) • Convergence solaire (ULTI : déclenche si 3+ raptors vivants et cible encerclée) : tous orientent simultanément leurs queues-miroirs vers une cible unique, formant un point de focalisation solaire. La cible fait un jet de RES vs 14. Échec : 1d10 dégâts + aveuglée 1 tour (ferme les yeux). Réussite : 1d6 dégâts + éblouie 1 tour seulement)

**Défenses :** Éblouissement (queue flash, -3 jet dés attaque)

</div>


<div class="rpg-box">

### Loot

**Défenses d'ivoire** : tuteur croissance végétale accélérée. Produit arbre-cadavre si plantées dans cadavre.

**Plumes-miroirs** : bouclier réfléchissant, flash défensif. Se ternissent à l'humidité.

**Capsule mortuaire / capsule maudite** : leurre, attire la meute, éclate en jus pestilentiel. Les créatures ciblent celui éclaboussé.

</div>


</section>

<section class="rpg-sheet-page creature-card">

<div class="rpg-sheet-title">

## COCCISABRE

<span>créature</span>

</div>

<p class="creature-description">Coupole chitineuse rouge-orangé, si immobile qu'on la prendrait pour une concrétion minérale. Au-dessus d'elle flottent des boules de duvet blanc, en lévitation dans un champ de charges statiques, pareilles à des graines de pissenlit figées dans l'air.</p>

| PV | FOR | RES |
| --- | --- | --- |
| 18 | 5 | 4 |


<div class="rpg-box">

### Combat

**Comportement :** Piège immobile. Attaque si champ de mines déclenché. RP mouvements très lents ?

**Attaques :** Champ mines duveteuses (contact = colle + neurotoxine : T1 -50% dépl, T2 rigidité, T3 paralysie) • Exécution (one-shot paralysés ou survie à 2PV)

**Défenses :** Carapace couverture totale (sauf ventre/ailes si ouverte)

</div>


<div class="rpg-box">

### Loot

**Glande à toxine** : 10 doses poison, paralysie progressive. Condition : tuer la coccisabre.

**Poudre styptique** : stoppe un saignement immédiatement. Cinq doses.

**Plaques de carapace coccisabre** : matériau ultra-léger, base de protection. Condition : tuer ou apaiser la coccisabre.

**Dent-sabre brute** : récupérée directement sur la coccisabre. Arme lourde. Ignore 3 RES. +1 FOR -2 AGI.

</div>


</section>

<section class="rpg-sheet-page creature-card">

<div class="rpg-sheet-title">

## PATRIARCHE-COMPOSTEUR

<span>créature</span>

</div>

<p class="creature-description">Montagne ambulante de bois humide, de mousse et de champignons stratifiés, si vaste qu'on la confond d'abord avec le relief. L'organisme se déplace avec une lenteur géologique, indifférent à tout, brisant les formations rocheuses sur son passage comme des brindilles. Autour de lui, la végétation prospère de manière anormale, comme nourrie par sa seule présence.</p>

| PV | FOR | RES | AGI |
| --- | --- | --- | --- |
| 99999 | Peut one shot un Pagure géant contrairement à vous | 9999 | 0 |


<div class="rpg-box">

### Combat

**Comportement :** Pacifisme dédaigneux total. Ignore tout. Continue sa route.

**Attaques :** Soupir des âges (perte tour + envie de rentrer) • Pichenette (500 dégâts, cadavre expédié au biome voisin)

**Défenses :** Frapper = arme digérée par 3m de mousse • Immunité totale

</div>

</section>

<section class="rpg-sheet-page creature-card">

<div class="rpg-sheet-title">

## PIE-LLARD

<span>créature</span>

</div>

<p class="creature-description">Oiseau-insecte de taille moyenne dont le plumage est entièrement constitué de débris métalliques récupérés : vis, boulons, fragments de coque. Une glande sous-jugulaire bleutée pulse à intervalles réguliers, générant de petits arcs électriques visibles entre les plumes. L'espèce manifeste une attirance compulsive pour tout objet manufacturé, qu'elle intègre méthodiquement à son plumage.</p>

| PV | FOR | RES |
| --- | --- | --- |
| 19 | 4 | 2 |


<div class="rpg-box">

### Combat

**Comportement :** Ne cible pas PV mais le métal des joueurs.

**Attaques :** Vol à l'arraché (FOR joueur vs 16, échec = objet volé+ajouté armure) • impulsion finale (arrache TOUT métal 10m)

**Défenses :** Champ répulsif (attaques métal déviées) • Blindage adaptatif (+RES par objet volé)

</div>


<div class="rpg-box">

### Loot

**Glande de flux** : attire le métal ou désarme, test DEX. Perturbe supports magnétiques.

**Tout métal volé** : récupération des objets perdus. Tri à faire.

</div>


</section>

<section class="rpg-sheet-page creature-card">

<div class="rpg-sheet-title">

## ÉCHO-ÉCHO

<span>créature</span>

</div>

<p class="creature-description">Silhouette humanoïde aux contours perpétuellement flous, comme agitée par une vibration interne. Le spécimen ne possède aucun trait facial ; une parabole organique concave occupe l'emplacement du visage, encadrée d'une peau fine et tendue comme une membrane de tambour. L'animal est manifestement aveugle, mais réagit au moindre son avec une précision déconcertante.</p>

| PV | FOR | RES |
| --- | --- | --- |
| 14 | 5 | 2 |


<div class="rpg-box">

### Combat

**Comportement :** Attaque source bruit la plus forte. **RP :** Joueurs doivent CHUCHOTER IRL.

**Attaques :** Saut de phase (instantané vers cible bruyante : étourdissement 1 tour + sonnée : ne peut plus chuchoter jusqu'à fin combat) • Lame sonique (cri qui liquéfie organes, ignore armure)

**Défenses :** Flou cinétique (seuil réussite attaque dés plus haut tant que pas étourdie)

</div>


<div class="rpg-box">

### Loot

**Syrinx mimétique** : projette voix ou sons à 30m, leurres parfaits. Condition : écho-écho tué ou piégé.

**Membrane tympanique** : capteurs sonores ultra-sensibles. Condition : prélèvement délicat.

</div>


</section>

<section class="rpg-sheet-page creature-card">

<div class="rpg-sheet-title">

## OREN

<span>créature</span>

</div>

<p class="creature-description">C'est bien vide par ici. Hmm.</p>

| PV | FOR | RES |
| --- | --- | --- |
| 17 | 3 | 1 |


<div class="rpg-box">

### Combat

**Attaques :** Lianes immobilisantes (1 tour entravé) • Fouet-liane (épines +2 PERFO, longue portée)

**Défenses :** Armure de plantes (RES + 3) • Régénération fongique (contact sol : regagne 1d6 PV + les personnes qui attaquent pendant la canalisation sont empoisonnées)

</div>


<div class="rpg-box">

### Loot

**Graines corrompues** : possède l'écureuil-coffre, corrompt l'inventaire organique. Peut contaminer un PJ.

**Lianes épineuses** : cordage résistant, entrave à distance. Conducteur électrique.

**Filaments fongiques** : fil fin pour tissage, filet ou suture d'urgence. Infection si peau ouverte.

**Résine phosphorescente** : balise visuelle, marquage de chemin, lumière faible. Attire ce qui suit la lumière.

**Écureuil-coffre-zeppelin** : +3 slots d'inventaire organique, allège une charge ou permet un grand saut. Caractère imprévisible.

**Fiole de catalyseur** : double l'effet d'une substance. Réaction violente si test INT raté.

**Onguents d'Oren** : soins efficaces, +1d6 PV. Contamination.

**Fragments mycélium** : développer résistance à l'infection, soigner un parasité. Manipulation délicate. Condition : seulement si combat avec Oren.

</div>


</section>

<section class="rpg-sheet-page creature-card">

<div class="rpg-sheet-title">

## CRAPAUD-HALLUCINOGÈNE

<span>créature</span>

</div>

<p class="creature-description">Masse bulbeuse et luisante, tapie dans les recoins humides où la lumière pénètre à peine. Sa peau sécrète un film irisé qui s'évapore lentement, formant un halo tremblant autour de l'animal. Les spécimens observés restent parfaitement immobiles pendant des heures, avec la patience d'un piège à mâchoires végétal.</p>

| PV | FOR | RES |
| --- | --- | --- |
| 11 | 3 | 2 |


<div class="rpg-box">

### Combat

**Comportement :** Patient. Attaque si proie hallucinée ou acculé.

**Attaques :** Brume psychotrope (passif) • Bile acide (à distance + état empoisonné) • Bond gluant (atteint cible même si repliée + entrave 1 tour) • Langue harponnée (attire la cible à lui ; celle-ci doit tirer les dés pour déterminer ce qu'elle heurte en chemin)

**Défenses :** Peau spongieuse (+ 3 RES contre attaque feu) • Camouflage parfait (difficile à repérer : malus T1 pour l'atteindre) • Immunité toxines

</div>


<div class="rpg-box">

### Loot

**Glandes hallucinogènes** : grenade fumigène, déni de zone pendant 3 tours. Dangereux sans protection.

**Peau visqueuse** : imperméable/isolant.

</div>


</section>

<section class="rpg-sheet-page creature-card">

<div class="rpg-sheet-title">

## BISON-CUIRASSÉ

<span>créature</span>

</div>

<p class="creature-description">Herbivore massif dont le corps est couvert d'écailles osseuses imbriquées, évoquant une armure médiévale taillée pour un animal de trait. Chaque pas fait trembler le sol ; devant lui, la végétation la plus dense s'écarte d'elle-même, comme répondant à un signal chimique. L'animal broute avec une placidité souveraine, indifférent à la plupart des prédateurs du biome.</p>

| PV | FOR | RES |
| --- | --- | --- |
| 25 | 5 | 5 |


<div class="rpg-box">

### Combat

**Comportement :** Pacifique. Si blessé/harcelé : charge défensive massive.

**Attaques :** Charge terrestre (piétinement) • Coup de corne (projette) • Piétinement panique (si encerclé : dégâts de zone)

**Défenses :** Cuirasse (immunité armes légères) • Masse (impossible à déplacer)

</div>


<div class="rpg-box">

### Loot

**Écaille de bison-cuirassé** : clé végétale qui ouvre la muraille noire. Passage bref, fermeture progressive.

</div>


</section>

<section class="rpg-sheet-page creature-card">

<div class="rpg-sheet-title">

## GARDIEN-LÉMURIEN

<span>créature</span>

</div>

<p class="creature-description">Minuscule humanoïde d'une cinquantaine de centimètres, aux yeux démesurés de lémurien, dont les veines d'un vert luminescent courent sous la fourrure jusqu'à disparaître dans la paroi végétale. Le spécimen observe les intrus avec une curiosité non dissimulée, inclinant la tête de gauche à droite. Plusieurs témoignages concordent : après son passage, les chemins ne mènent plus tout à fait où ils menaient.</p>

| PV | FOR | RES |
| --- | --- | --- |
| 1 | 1 | -1 |


<div class="rpg-box">

### Combat

**Comportement :** Évite combat. Manipule environnement : fermer passage, ouvrir fissures, fuir. Petit jeu de mime.

**Attaques :** Manipulation muraille (se referme jet de sprint pour sortir à temps) • Cri d'alarme (je pense que vous allez vous attirer des ennuis...)

**Défenses :** on comprend bien en lisant les stats que cette pauvre petite créature n'a pas de défense. veuillez continuer à lire la suite.

</div>

</section>

<section class="rpg-sheet-page creature-card">

<div class="rpg-sheet-title">

## DORMEUR

<span>créature</span>

</div>

<p class="creature-description">Au fond de la cavité gît une masse blanche titanesque, recroquevillée sur elle-même, parcourue d'un réseau de veines bioluminescentes éteintes. Le spécimen mesure près de quinze mètres. L'air autour de lui est parfaitement immobile, comme si l'atmosphère elle-même retenait son souffle.</p>

| PV | FOR | RES |
| --- | --- | --- |
| 25 | 4 | 4 |


<div class="rpg-box">

### Combat

**Comportement :** Sommeil profond. Éveil si perturbation majeure (vibrations, sang, contact). Réveil : 30s → veines s'allument → FUYEZ.

**Attaques :** Jaillissement titanesque • Tentacules rasoir (3 PERFO et longue portée) • Cri ultrasonique (étourdit 3 tours, brise verre)

**Défenses :** Carapace céramique multicouche • Taille (immunité armes légères)

</div>


<div class="rpg-box">

### Loot

**Pétales de fleurs-hélices** : parachute, plané court, frein de chute. Usage unique, fragile.

**Tige vrillée** : ressort organique, lanceur léger. Se détend d'un coup si mal nouée.

**Glande de stase** : sédatif massif, K.O. instantané. Manipulation très dangereuse.

</div>


</section>

<section class="rpg-sheet-page creature-card">

<div class="rpg-sheet-title">

## HOLLOW

<span>créature</span>

</div>

<p class="creature-description">Humanoïde de deux mètres à la peau lisse, ornée de motifs organiques noirs et blancs évoquant un test de Rorschach. Aucun trait facial : la surface du visage est réfléchissante et bombée comme de la porcelaine polie. L'entité se déplace sans produire le moindre son, tête légèrement inclinée, et ne semble jamais préoccupée par sa propre sécurité.</p>

| PV | FOR | RES | VOL |
| --- | --- | --- | --- |
| 18 | 2 | 2 | 5 (volonté) |


<div class="rpg-box">

### Combat

**Comportement :** Contrôle à distance. Ne se bat jamais directement. Utilise ses esclaves mentaux.

**Attaques :** Emprise mentale (qui fait le meilleur lancer) • Marionnettes Humaines (esclaves attaquent à sa place)

**Défenses :** • Télékinésie défensive (dévie projectiles)

</div>


<div class="rpg-box">

### Loot

**Fragment psychique** : peut apaiser ou soigner un parasité. Condition : Hollow vaincu.

</div>


</section>

</div>

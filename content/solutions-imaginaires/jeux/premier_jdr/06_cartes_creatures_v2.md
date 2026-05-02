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
body:has(.rpg-print-sheets) main {
  background: var(--ctp-base) !important;
}
body:has(.rpg-print-sheets) .animate-fade-in-up > header {
  border-bottom-color: var(--ctp-surface0) !important;
}
body:has(.rpg-print-sheets) .animate-fade-in-up > header h1 {
  color: var(--ctp-peach) !important;
}
body:has(.rpg-print-sheets) .breadcrumb a,
body:has(.rpg-print-sheets) .breadcrumb-separator,
body:has(.rpg-print-sheets) .breadcrumb-current {
  color: var(--ctp-subtext0) !important;
}
.article-prose:has(.rpg-print-sheets) {
  max-width: min(210mm, calc(100vw - 2rem));
  width: 100%;
}
.rpg-print-sheets {
  --sheet-bg: var(--ctp-mantle);
  --sheet-ink: var(--ctp-text);
  --sheet-muted: var(--ctp-subtext0);
  --sheet-line: var(--ctp-surface2);
  --sheet-soft: var(--ctp-surface0);
  --sheet-accent: var(--ctp-mauve);
  --sheet-accent-2: var(--ctp-blue);
  color: var(--sheet-ink) !important;
  max-width: 210mm;
  margin: 0 auto 4rem;
}
.rpg-print-sheets :where(h1, h2, h3, h4, h5, h6, p, li, table, th, td) {
  color: var(--sheet-ink) !important;
}
.rpg-print-sheets :where(strong, b) {
  color: var(--sheet-accent-2) !important;
}
.rpg-print-sheets :where(em, i) {
  color: var(--ctp-green) !important;
}
.rpg-print-sheets :where(p, li, blockquote) {
  text-align: start;
  text-align-last: auto;
}
.rpg-print-sheets :where(th, td) {
  border-color: var(--sheet-line) !important;
}
.rpg-print-sheets :where(thead th) {
  background-color: color-mix(in srgb, var(--sheet-soft) 72%, transparent) !important;
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
  box-shadow: 8px 8px 0 var(--ctp-crust);
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
  body,
  #app-shell,
  main,
  main > div,
  main > div > div,
  .animate-fade-in-up,
  .article-prose {
    height: auto !important;
    min-height: 0 !important;
    overflow: visible !important;
    background: #fff !important;
    color: #111 !important;
  }
  body:has(.rpg-print-sheets) main {
    background: #fff !important;
  }
  body:has(.rpg-print-sheets) .breadcrumb,
  body:has(.rpg-print-sheets) #app-shell > header,
  body:has(.rpg-print-sheets) .fixed.bottom-0,
  body:has(.rpg-print-sheets) .animate-fade-in-up > header,
  body:has(.rpg-print-sheets) #sidebar-panel,
  body:has(.rpg-print-sheets) #sidebar-backdrop,
  body:has(.rpg-print-sheets) #toc-panel,
  body:has(.rpg-print-sheets) #toc-backdrop,
  body:has(.rpg-print-sheets) .md\:hidden {
    display: none !important;
  }
  body:has(.rpg-print-sheets) {
    margin: 0 !important;
  }
  body:has(.rpg-print-sheets) .flex-grow {
    padding-top: 0 !important;
  }
  body:has(.rpg-print-sheets) main > div > div {
    max-width: none !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
  }
  body:has(.rpg-print-sheets) .article-prose {
    max-width: 190mm !important;
    width: 190mm !important;
    margin: 0 auto !important;
    padding: 0 !important;
  }
  .rpg-print-sheets {
    --sheet-bg: #fff !important;
    --sheet-ink: #111 !important;
    --sheet-muted: #444 !important;
    --sheet-line: #222 !important;
    --sheet-soft: #fff !important;
    --sheet-accent: #111 !important;
    --sheet-accent-2: #111 !important;
    max-width: 190mm !important;
    width: 190mm !important;
    margin: 0 auto !important;
  }
  .rpg-print-intro {
    display: none !important;
  }
  .rpg-sheet-page {
    width: 190mm;
    min-height: 0;
    height: 270mm;
    margin: 0 auto !important;
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

**Ovoïde galvanique** : batterie bio. lampe concussion (flash + 100 lumens 4h) ou explosion EMP.

**Plaques chitine-roche** : armures lourdes/boucliers.

**Sabots électrifiés** : armes mêlée avec dégâts électriques (malus au jet -2 à la cible touchée).

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

**Plaque chitine-béton** : bouclier lourd (très encombrant).

**Chair** : comestible, texture pneu, 15 min/bouchée.

**Algues séchées** : combustible lent ou isolant.

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

**Bobine bio-fil** : +kevlar, stérile. Médecine auto-réussie ou cordes ultra-fines.

**Aiguilles articulées** : pointes perforantes (ignore 2 de RES si composant d'une arme).

**Glande à soie** : 50m de fil très résistant si pressée.

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

**Carapace** : bouclier ou renfort robot. **Dard** : arme empoisonnée. **Mandibules** : cisailles.

**Glandes acides** : 3 munitions corrosives. **Chair ventrale** : délicieuse, donne soif.

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

**Défenses ivoire** : si réduit en poudre, permet de fabriquer/regagner des charges kit de soin.

**Plumes-miroirs** : boucliers réfléchissants (projectiles).

**Fruit maudit** : leurre explosif qui attire toute une meute si lancé/explose. Mais contre qui ? (jet de dés)

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

**Dent-sabre** : mêlée dévactatrice, tranche armures (ignore 5 RES).

**Glande toxine** : paralysant contact.

**Carapace** : défensif (trop lourd pour tout prendre).

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


<div class="rpg-box">

### Loot

**Champignons qui ont l'air précieux ?** Who knows ?

**Mousse symbiotique** : très bonne absorption.

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

**Glande de flux** : bio-magnétique, attire métal 5m ou désarme. EFFACE disques/cartes.

Tout métal volé tombe à sa mort.

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

**Syrinx mimétique** : projecteur vocal 30m = ventriloquie/leurre.

**Membrane tympanique** : capteurs sonores ultra-sensibles.

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

**Glandes hallucinogènes** : grenade fumigène.

**Peau visqueuse** : imperméable/isolant.

**Chair** : toxique crue.

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

**Écaille-clé** : ramassable sans tuer. Ouvre muraille végétale (3 utilisations).

**Plaques cuirassées** : armures/barricades.

**Cornes** : leviers/armes.

**Cuir** : sangles/harnais.

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


<div class="rpg-box">

### Loot

**Veines symbiotiques** : interface contrôle végétale (usage unique).

**Glandes résine** : colle ultra-forte (2 doses).

**Fourrure bioluminescente** : vêtements lumineux.

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

**Plaques céramiques** : armures lourdes exceptionnelles.

**Tentacule** : fouets/câbles 15m.

**Dents** : lames, harpons.

**Glande de stase** : sédatif massif (K.O. instantané).

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

**Fragment psychique** : peut soigner les parasités.

**Peau céramique** : armure légère réfléchissante + 2 RES sans malus AGI.

**Noyau neural** : si étudié, permet clarifier état robot.

</div>


</section>

</div>

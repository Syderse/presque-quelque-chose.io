---
title: "Cartes personnages"
weight: 71
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
<style>
.character-sheet {
  display: flex;
  flex-direction: column;
  gap: 0.42rem;
  font-size: 8.25pt;
  line-height: 1.16;
}
.character-sheet .rpg-sheet-title {
  margin-bottom: 0.2rem;
}
.character-sheet .rpg-sheet-title h2 {
  font-size: 1.15rem;
}
.character-top {
  display: grid;
  grid-template-columns: 1fr 0.62fr;
  gap: 0.5rem;
  align-items: start;
}
.hp-tracker {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.1rem;
  width: 100%;
  margin-top: 0.2rem;
}
.hp-box {
  display: block;
  aspect-ratio: 1 / 1;
  border: 1px solid var(--sheet-line);
  background: var(--ctp-base);
}
.character-bio {
  border: 1.4px solid var(--sheet-line);
  padding: 0.38rem 0.5rem;
  background: color-mix(in srgb, var(--sheet-soft) 70%, transparent);
}
.character-bio p {
  margin: 0.18rem 0 0;
}
.name-line {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.35rem;
  align-items: end;
  margin-bottom: 0.22rem;
}
.name-line span:last-child {
  border-bottom: 1px solid var(--sheet-line);
  min-height: 0.85rem;
}
.character-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.45rem;
  align-items: start;
}
.character-sheet .rpg-box {
  padding: 0.35rem 0.45rem;
}
.character-sheet .rpg-box h3 {
  font-size: 0.66rem;
  margin-bottom: 0.18rem;
}
.character-sheet ul {
  margin: 0;
  padding-left: 0.9rem;
}
.character-sheet li {
  margin: 0.12rem 0;
}
.character-choices {
  grid-column: 1 / -1;
}
.sheet-bottom {
  display: grid;
  grid-template-columns: 0.82fr 1.18fr;
  gap: 0.45rem;
  margin-top: auto;
}
.inventory-lines,
.notes-lines {
  margin: 0;
  padding: 0;
}
.inventory-lines li {
  display: block;
  list-style: none;
  min-height: 0.5rem;
}
.gear-lines {
  display: none;
}
.notes-lines {
  display: none;
}
@media print {
  .character-sheet {
    display: block;
    font-size: 7.55pt;
    line-height: 1.12;
    gap: 0.34rem;
  }
  .character-sheet > * + * {
    margin-top: 0.34rem;
  }
  .sheet-bottom {
    margin-top: 0.34rem !important;
  }
  .character-sheet .rpg-sheet-title h2 {
    font-size: 1.05rem;
  }
  .character-sheet .rpg-box {
    padding: 0.28rem 0.38rem;
  }
  .character-bio {
    padding: 0.3rem 0.4rem;
  }
  .hp-box {
    background: #fff !important;
  }
  .inventory-lines li {
    min-height: 0.38rem;
  }
}
</style>
<div class="rpg-print-sheets character-sheets">

<div class="rpg-print-intro">

# FICHES PERSONNAGES

</div>

<section class="rpg-sheet-page character-sheet">

<div class="rpg-sheet-title">

## NATURALISTE

<span>personnage</span>

</div>

<div class="character-top">

<div class="rpg-box">

### Statistiques

| PV | FOR | RES | SAV | PER | AGI |
| --- | --- | --- | --- | --- | --- |
| 9 | 1 | 2 | 4 | 5 | 2 |

</div>

<div class="rpg-box">

### Tracker PV

<div class="hp-tracker" aria-label="9 points de vie"><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span></div>

</div>

</div>

<div class="character-bio">

<div class="name-line"><strong>Nom :</strong><span></span></div>

<p>Tout a commencé à huit ans, le jour où un papillon a croisé son chemin. Iel l'a suivi — évidemment, qui ne l'aurait pas fait ? Le papillon l'a mené·e jusqu'à une grotte humide au fond de laquelle quelque chose palpitait doucement. Iel s'est approché·e. Et puis plus rien. Vingt-quatre heures plus tard, iel est ressorti·e d'un cocon, couvert·e d'une substance étrangement apaisante. Ses parents, qui avaient déjà commencé à porter le deuil, n'en sont pas revenu·es. Iel non plus, d'une certaine manière : quelque chose avait changé, là-dedans. On lui a interdit d'y retourner. Iel y retournait quand même, discrètement, la nuit, dessinait les organismes, prélevait des échantillons. À seize ans, major de promo en biologie. À dix-neuf, en s'inspirant de la structure des cocons, iel concevait des armures de protection spatiale pour son père soldat et les commercialisait, avec un succès inattendu. Iel devint le·a plus riche PDG d'entreprise biotechnologique de la galaxie. Obsédé·e par la prochaine planète inexplorée, le prochain spécimen improbable, iel a initié la mission de reconnaissance dans laquelle sont embarqués tous les personnages. Iel est convaincu·e que chaque espèce, même la plus hideuse, cache un trésor utile à l'humanité. Il suffit juste de savoir regarder.</p>

</div>

<div class="character-grid">

<div class="rpg-box">

### Compétences passives

- **Lecture biologique** — *Identifie auto si créature/plante est comestible, toxique ou utile. Le MJ donne au moins une info.*
- **Symbiose intuitive** — *Les créatures ne l'attaquent pas au premier tour (sauf provocation directe). Iel ne sera jamais le·a premier·ère à être ciblé·e.*

</div>

<div class="rpg-box">

### Combat

- **Maître·esse des herbes et potions** — *Peut concocter des brevages offensifs ou défensifs qui donnent +2 RES ou FOR le temps d'un combat à un allié.*

</div>

<div class="rpg-box">

### Faiblesse

Essaye toujours de capturer plutôt qu'achever. **-5 pour porter le coup fatal.** Si iel achève quand même : -1 à tous les jets pendant toute la durée du biome en cours.

</div>

<div class="rpg-box character-choices">

### Compétences au choix — Choisis 2 parmi 5

- [ ] **Phéromones de pacification** — *1×/biome, force un ennemi biologique à passer son tour.*
- [ ] **Collecteur·rice expert·e** — *Une fois par biome, peut fabriquer un kit de soin à partir d'échantillons organiques. Le kit rend 1d6PV.*
- [ ] **Masta' Beast Masta'** — *Apprivoise une petite créature compagnon (attaque 1d6, peut distraire un ennemi ou absorber un coup).*
- [ ] **Décodeur de patterns** — *À partir du second tour de combat, iel obtient une nouvelle information sur la créature.*
- [ ] **Toxicologue** — *Immunité aux poisons et aux gazs toxiques.*

</div>

</div>

<div class="sheet-bottom">

<div class="rpg-box">

### Inventaire (7 emplacements)

<ol class="inventory-lines" aria-label="Inventaire, sept emplacements">
  <li><span>1.</span></li>
  <li><span>2.</span></li>
  <li><span>3.</span></li>
  <li><span>4.</span></li>
  <li><span>5.</span></li>
  <li><span>6.</span></li>
  <li><span>7.</span></li>
</ol>

<div class="gear-lines"><strong>Arme et armure :</strong><span></span><span></span></div>

</div>

<div class="rpg-box">

### Notes de partie

<div class="notes-lines" aria-label="Notes de partie">
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
</div>

</div>

</div>

</section>

<section class="rpg-sheet-page character-sheet">

<div class="rpg-sheet-title">

## AGENT·E DES FORCES SPÉCIALES

<span>personnage</span>

</div>

<div class="character-top">

<div class="rpg-box">

### Statistiques

| PV | FOR | RES | TAC | PER | AGI |
| --- | --- | --- | --- | --- | --- |
| 12 | 5 | 3 | 4 | 2 | 2 |

</div>

<div class="rpg-box">

### Tracker PV

<div class="hp-tracker" aria-label="13 points de vie"><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span></div>

</div>

</div>

<div class="character-bio">

<div class="name-line"><strong>Nom :</strong><span></span></div>

<p>L'État a pris en charge l'enfant à l'âge de quatre ans. Pas de jouets, pas de berceuses. À seize ans, iel dominait sa promotion. À dix-sept, iel avait déjà mené trois opérations sur le terrain. À dix-huit ans, un dossier classifié est tombé entre ses mains par accident. Dedans : deux noms, deux photos, un procès-verbal d'exécution. Ses parents. Des révolutionnaires, disait le rapport. Abattu·es par son·sa mentor Kasev, cellui-là même qui, penché·e sur le berceau de l'enfant orphelin·e, avait murmuré : « Je ferai de votre enfant le·a plus fidèle toutou de l'État. » Iel a posé le dossier. Iel a pris ses affaires. Et iel est parti·e, sans un mot, sans se retourner. L'État a envoyé trois escouades à ses trousses. Aucune n'est revenue au complet.</p>

</div>

<div class="character-grid">

<div class="rpg-box">

### Compétences passives

- **Instinct de survie** — *Ne peut jamais être tué en un seul coup. Si devrait mourir → reste à 1 PV (2×/partie). Même s'il doit subir -4PV alors qu'il ne lui en reste que 2, il survit à 1PV.*
- **Rat de laboratoire** — *Immunité aux poisons.*

</div>

<div class="rpg-box">

### Combat

- **Frappe décisive** — *2×/partie, transforme un coup en critique auto (déclarer avant le jet).*
- **Riposte** — *Si une attaque le·a rate, contre-attaque immédiate (sans coût d'action).*

</div>

<div class="rpg-box">

### Faiblesse

**Déformations professionnelles :** À chaque premier combat dans un biome, il passe son premier tour, étant trop occupé à sur-analyser le terrain.

</div>

<div class="rpg-box character-choices">

### Compétences au choix — Choisis 2 parmi 5

- [ ] **Tir de suppression** — *Force toutes les créatures d'une zone à se mettre à couvert 1 tour.*
- [ ] **Démolisseur** — *+4 pour détruire structures, carapaces, barrières. Peut forcer les passages.*
- [ ] **Commandement de terrain** — *1×/tour, donne un ordre tactique : un·e allié·e se repositionne gratuitement ou gagne +2 à sa prochaine action.*
- [ ] **Seconde peau** — *L'armure ne gêne jamais ses mouvements.*
- [ ] **Zéro hésitation** — *Agit toujours en premier au 1<sup>er</sup> tour. **Malus :** ne peut pas fuir.*

</div>

</div>

<div class="sheet-bottom">

<div class="rpg-box">

### Inventaire (7 emplacements)

<ol class="inventory-lines" aria-label="Inventaire, sept emplacements">
  <li><span>1.</span></li>
  <li><span>2.</span></li>
  <li><span>3.</span></li>
  <li><span>4.</span></li>
  <li><span>5.</span></li>
  <li><span>6.</span></li>
  <li><span>7.</span></li>
</ol>

<div class="gear-lines"><strong>Arme et armure :</strong><span></span><span></span></div>

</div>

<div class="rpg-box">

### Notes de partie

<div class="notes-lines" aria-label="Notes de partie">
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
</div>

</div>

</div>

</section>

<section class="rpg-sheet-page character-sheet">

<div class="rpg-sheet-title">

## PRISONNIER·RE

<span>personnage</span>

</div>

<div class="character-top">

<div class="rpg-box">

### Statistiques

| PV | FOR | RES | RUS | PER | AGI |
| --- | --- | --- | --- | --- | --- |
| 10 | 2 | 2 | 5 | 3 | 5 |

</div>

<div class="rpg-box">

### Tracker PV

<div class="hp-tracker" aria-label="10 points de vie"><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span></div>

</div>

</div>

<div class="character-bio">

<div class="name-line"><strong>Nom :</strong><span></span></div>

<p>Iel est en prison. Pourquoi ? Bonne question. Si vous trouvez la réponse, faites-lui signe, parce qu'iel aimerait bien savoir aussi. Les juges n'ont pas été très clair·es, l'avocat·e non plus, et honnêtement, à un moment, iel a arrêté d'écouter. Le truc, c'est que personne n'a jamais vraiment insisté pour comprendre : ni les matons, ni les codétenu·es, ni l'administration. Alors iel s'est dit : bon, d'accord, c'est comme ça. Et iel s'est installé·e. Confortablement, même. Iel a son petit coin, ses petites habitudes, ses petits trafics, rien de bien méchant, des trucs trop minuscules pour que les gardien·nes se donnent la peine de lever un sourcil. Un peu de troc par-ci, un service par-là. Avec le temps, iel s'est fait des ami·es, a appris à jouer aux cartes avec la main gauche, à regagner son lit superposé à cloche-pied, à se faufiler dans la cantine pour récupérer les desserts non distribués. L'idée de sortir ? Iel n'y pense même plus. Dehors, c'est compliqué.</p>

</div>

<div class="character-grid">

<div class="rpg-box">

### Compétences passives

- **Personne ne me surveille** — *Se déplace discrètement même observé. Les créatures ciblent les autres en priorité.*
- **Sang-froid** — *Quand iel est à 3 PV ou moins, iel gagne +2 à tous ses jets au lieu de paniquer. Plus la situation est désespérée, plus iel devient dangereux·se.*

</div>

<div class="rpg-box">

### Combat

- **Coup bas** — *Par surprise : **coup critique**. Si raté, la cible se concentre exclusivement sur lui.*
- **Lampe empoisonnée** — *Enduit ses armes ou ses projectiles de substances empoisonnées. Les attaques appliquent l'état empoisonné pendant deux tours (non-cumulable).*

</div>

<div class="rpg-box">

### Faiblesse

**Chocottes** En cas de coup dur, son réflexe immédiat est de prendre la fuite et de se trouver vite fait bien fait une bonne cachette.

</div>

<div class="rpg-box character-choices">

### Compétences au choix — Choisis 2 parmi 5

- [ ] **Saltimbanque** — *Très habile en toutes circonstances (+2 AGI).*
- [ ] **Joker** — *2×/biome, annule une conséquence négative le concernant.*
- [ ] **Caméléon** — *1×/biome, peut imiter le comportement ou la posture d'une créature observée pendant 1 tour. Pendant 1 tour (ou 1 scène hors combat), les créatures de cette espèce le traitent comme l'un des leurs.*
- [ ] **Fantôme** — *Après avoir infligé des dégâts, iel peut immédiatement se repositionner (se mettre à couvert, reculer, changer de flanc). Les ennemis perdent sa trace jusqu'à sa prochaine attaque.*
- [ ] **Assassin Drama Queen** — *Quand iel tombe à 0 PV, iel ne meurt pas immédiatement. Iel a droit à une dernière action : une attaque, un mot, un geste, un sabotage. Cette action bénéficie de +5 au jet ! Puis iel s'effondre en soupirant très fort.*

</div>

</div>

<div class="sheet-bottom">

<div class="rpg-box">

### Inventaire (7 emplacements)

<ol class="inventory-lines" aria-label="Inventaire, sept emplacements">
  <li><span>1.</span></li>
  <li><span>2.</span></li>
  <li><span>3.</span></li>
  <li><span>4.</span></li>
  <li><span>5.</span></li>
  <li><span>6.</span></li>
  <li><span>7.</span></li>
</ol>

<div class="gear-lines"><strong>Arme et armure :</strong><span></span><span></span></div>

</div>

<div class="rpg-box">

### Notes de partie

<div class="notes-lines" aria-label="Notes de partie">
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
</div>

</div>

</div>

</section>

<section class="rpg-sheet-page character-sheet">

<div class="rpg-sheet-title">

## INGÉNIEUR·E

<span>personnage</span>

</div>

<div class="character-top">

<div class="rpg-box">

### Statistiques

| PV | FOR | RES | TECHNO | PER | AGI |
| --- | --- | --- | --- | --- | --- |
| 9 | 2 | 3 | 5 | 3 | 2 |

</div>

<div class="rpg-box">

### Tracker PV

<div class="hp-tracker" aria-label="9 points de vie"><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span></div>

</div>

</div>

<div class="character-bio">

<div class="name-line"><strong>Nom :</strong><span></span></div>

<p>Personne lambda. Askip les machines lui parlent. Mais on sait pas trop, personne n'a vraiment envie de lui parler. Iel ne sait pas poser de questions, mais iel aime bien expliquer le fonctionnement des choses de la vie.</p>

</div>

<div class="character-grid">

<div class="rpg-box">

### Compétences passives

- **Sociopathe** — *Iel peut ignorer les décisions collectives et agir dans son coin, parce qu'iel sait mieux que tout le monde.*
- **Optimisation continue** — *Chaque objet utilisé régulièrement gagne +1 après 2 jours (cumulable 2× max).*

</div>

<div class="rpg-box">

### Combat

- **Tourelle improvisée** — *Construit une tourelle légère (1 tour de setup) qui tire automatiquement (1d6/tour).*
- **Data Analyst** — *Peut activer la posture Data Analyst : iel ne peut plus jouer mais observe et étudie tout ce qui se passe grâce à ses intruments de mesure. Dans cet état, retire 2 RES à tous les adversaires.*

</div>

<div class="rpg-box">

### Faiblesse

**Fascination dévorante :** Lorsqu'iel est confronté à une TECHNO inconnue, la curiosité prend possession d'ellui. Iel passe son tour.

</div>

<div class="rpg-box character-choices">

### Compétences au choix — Choisis 2 parmi 5

- [ ] **Firewall mental** — *Immunisé aux effets psychiques/hypnotiques des créatures.*
- [ ] **Télémétrie avancée** — *+3 PER grâce à ses super lunettes.*
- [ ] **Armurier** — *Au début de chaque biome, désigne un allié dont l'armure gagne +1 RES.*
- [ ] **Forgeron** — *Au début de chaque biome, désigne un allié dont l'arme gagne +1 DEG.*
- [ ] **Fusées de dispersion** — *Il possède deux puissantes fusées IEM qui déstabilisent les cibles et infligent 2d10 DMG en TECHNO.*

</div>

</div>

<div class="sheet-bottom">

<div class="rpg-box">

### Inventaire (7 emplacements)

<ol class="inventory-lines" aria-label="Inventaire, sept emplacements">
  <li><span>1.</span></li>
  <li><span>2.</span></li>
  <li><span>3.</span></li>
  <li><span>4.</span></li>
  <li><span>5.</span></li>
  <li><span>6.</span></li>
  <li><span>7.</span></li>
</ol>

<div class="gear-lines"><strong>Arme et armure :</strong><span></span><span></span></div>

</div>

<div class="rpg-box">

### Notes de partie

<div class="notes-lines" aria-label="Notes de partie">
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
</div>

</div>

</div>

</section>

<section class="rpg-sheet-page character-sheet">

<div class="rpg-sheet-title">

## CUISINIER·ÈRE

<span>personnage</span>

</div>

<div class="character-top">

<div class="rpg-box">

### Statistiques

| PV | FOR | RES | CREA | PER | AGI |
| --- | --- | --- | --- | --- | --- |
| 11 | 2 | 3 | 5 | 3 | 3 |

</div>

<div class="rpg-box">

### Tracker PV

<div class="hp-tracker" aria-label="11 points de vie"><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span></div>

</div>

</div>

<div class="character-bio">

<div class="name-line"><strong>Nom :</strong><span></span></div>

<p>Iel n'est <strong>pas</strong> cuisinier·ère. Iel est alchimiste. Ce mot, « cuisinier·ère », iel le trouve réducteur, vulgaire presque. Ce qu'iel fait en cuisine, c'est de la transmutation. Tout a commencé dans un petit appartement humide au-dessus d'une mine de cobalt. Sa cousine, qui l'a élevé·e, descendait dans les galeries chaque matin avant l'aube et remontait chaque soir en toussant. Iel la regardait se frotter le dos avec une grimace, et ça lui serrait le cœur. Alors iel s'est mis·e à cuisiner pour elle. Pas juste pour nourrir : pour soigner. Des bouillons aux racines anti-inflammatoires. Des pâtes infusées aux champignons bronchodilatateurs. Des desserts calmants au miel fermenté. Ça marchait, en plus, sa cousine toussait moins, souriait davantage. Iel a continué à combiner tout ce qui lui passait sous la main, à tester des associations improbables, à chercher dans chaque ingrédient le remède caché. Et puis un jour, à la cantine où iel travaillait, iel a un tout petit peu forcé sur le dosage d'un extrait de fleur de givre dans le ragoût du mardi. Résultat : trente-sept convives pétrifié·es pendant six heures, raides comme des statues, les yeux grands ouverts. Suspension immédiate. Mais franchement, si on y réfléchit bien, c'est quand même une découverte remarquable.</p>

</div>

<div class="character-grid">

<div class="rpg-box">

### Compétences passives

- **Poison goûtu** — *L'état empoisonné lui rend 1PV/tour au lui de lui en retirer.*
- **Quand l'estomac est content...** — *+1 à tous les jets grâce aux bons petits plats du cuisto préféré de l'équipage.*

</div>

<div class="rpg-box">

### Combat

- **Recette de grand-mère** — *Pendant le combat, peut utiliser une action pour soigner un·e allié·e de 1d6 une fois par combat*
- **Précision de boucher·ère** — *Si une créature à 4 PV ou moins, iel peut l'exécuter si iel fait une réussite aux dés (>12 CREA).*

</div>

<div class="rpg-box">

### Faiblesse

**Gastro-sensibilité :** Comme iel sent toujours la nourriture, les créatures le ciblent toujours en premier.

</div>

<div class="rpg-box character-choices">

### Compétences au choix — Choisis 2 parmi 5

- [ ] **Chimiste culinaire** — *Extrait substances actives en cuisinant : toxines, stimulants, antidotes.*
- [ ] **Festin revigorant** — *Lors d'un repos, soigne **tout le groupe** de 2 PV chacun.*
- [ ] **Appât gourmet** — *Prépare appât irrésistible pour un type de créature. Il peut attirer une créature. Mais le jet déterminera l'attitude de la créature.*
- [ ] **Dernier repas** — *Une seule fois par partie, peut redonner la vie à un·e allié·e mort·e.*
- [ ] **Injection d'adrénaline** — *3×/partie, prépare un stimulant qui donne +2 FOR à un allié pour toute la durée du combat.*

</div>

</div>

<div class="sheet-bottom">

<div class="rpg-box">

### Inventaire (7 emplacements)

<ol class="inventory-lines" aria-label="Inventaire, sept emplacements">
  <li><span>1.</span></li>
  <li><span>2.</span></li>
  <li><span>3.</span></li>
  <li><span>4.</span></li>
  <li><span>5.</span></li>
  <li><span>6.</span></li>
  <li><span>7.</span></li>
</ol>

<div class="gear-lines"><strong>Arme et armure :</strong><span></span><span></span></div>

</div>

<div class="rpg-box">

### Notes de partie

<div class="notes-lines" aria-label="Notes de partie">
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
</div>

</div>

</div>

</section>

<section class="rpg-sheet-page character-sheet">

<div class="rpg-sheet-title">

## POMPISTE/ PYROMANE

<span>personnage</span>

</div>

<div class="character-top">

<div class="rpg-box">

### Statistiques

| PV | FOR | RES | BRICOL | PER | AGI |
| --- | --- | --- | --- | --- | --- |
| 14 | 3 | 5 | 4 | 3 | 1 |

</div>

<div class="rpg-box">

### Tracker PV

<div class="hp-tracker" aria-label="15 points de vie"><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span><span class="hp-box"></span></div>

</div>

</div>

<div class="character-bio">

<div class="name-line"><strong>Nom :</strong><span></span></div>

<p>Dans la famille Pyrone, on naît avec une allumette entre les doigts. L'illustre Overlord de Pyrone, baron·ne incontesté·e de toutes les industries touchant de près ou de loin au feu, avait élevé son héritier·ère dans la plus pure tradition des flammes. Mais la jeune braise s'ennuyait. Les intrigues commerciales tortueuses, les dîners interminables avec des aristocrates décati·es qui sentaient le soufre refroidi, les querelles dynastiques autour du monopole des briquets, tout cela l'agaçait. Alors, le jour de son départ, iel organisa ses adieux avec le seul langage qu'iel connaissait : un feu d'artifice. Sauf qu'iel y est allé·e un peu fort. La planète tout entière s'est embrasée avec des couleurs magnifique, éteignant avec elle une bonne partie de la dynastie Pyrone. On pourrait penser qu'iel voit un psy pour soigner ce qui aurait pu être un traumatisme, mais iel a toujours du feu sur ellui.</p>

</div>

<div class="character-grid">

<div class="rpg-box">

### Compétences passives

- **J'ai toujours du feu sur moi** — *+2 aux jets impliquant l'élément feu. De plus, les attaques portées avec des armes de type feu enflamment les cibles pendant de tour. État enflammé : la cible perd 1PV au début de son tour de jeu.*
- **Peau épaisse** — *Réduit de 1 tous les dégâts reçus (s'iel doit subir -1PV, iel subit néanmoins -1PV). Les brûlures ne lui font aucun effet.*

</div>

<div class="rpg-box">

### Combat

- **Cocktails molotov** — *Peut fabriquer des cocktails Molotov facilement. **Part avec 2 cocktails Molotov.***
- **Cri de provocation** — *Pousse un hurlement qui enrage les adversaires et les met au défi. 2d10 RES réussite à 12. En cas de réussite, la prochaine attaque de chaque ennemi ciblera le·a pompiste.*

</div>

<div class="rpg-box">

### Faiblesse

**Iel veut mettre le feu à tout.** À chaque effet de feu, jet pour voir si iel inflige des dégâts collatéraux aux allié·es.

</div>

<div class="rpg-box character-choices">

### Compétences au choix — Choisis 2 parmi 5

- [ ] **Bombe artisanale** — *Fabrique un explosif improvisé avec les matériaux disponibles (1 tour de préparation). 2d10 dégâts en zone, détruit les barricades et structures. Jet de BRICOL (diff. 10) : échec = explose prématurément (1d6 dégâts à iel et aux alliés proches qui ignore 2 RES). 2×/partie*
- [ ] **Surcharge thermique contrôlée** — *Pousse un objet, une arme, une armure, au-delà des limites : +3 aux dés, mais destruction au bout de deux utilisations.*
- [ ] **Mur de flamme** — *Créé un mur de flamme où il le souhaite. Il inflige -2PV et appliqué l'état enflammé si un PJ ou une créature le traverse.*
- [ ] **Mastodonte** — *Soulève ou déplace les objets lourds. +4 FOR pour les actions de force brute. Hors combat, ou pour manipulation tactique en combat (pas pour attaquer).*
- [ ] **Bouclier de fortune** — *Fabrique un bouclier avec des débris. +2 RES, se détruit après un combat.*

</div>

</div>

<div class="sheet-bottom">

<div class="rpg-box">

### Inventaire (7 emplacements)

<ol class="inventory-lines" aria-label="Inventaire, sept emplacements">
  <li><span>1.</span></li>
  <li><span>2.</span></li>
  <li><span>3.</span></li>
  <li><span>4.</span></li>
  <li><span>5.</span></li>
  <li><span>6.</span></li>
  <li><span>7.</span></li>
</ol>

<div class="gear-lines"><strong>Arme et armure :</strong><span></span><span></span></div>

</div>

<div class="rpg-box">

### Notes de partie

<div class="notes-lines" aria-label="Notes de partie">
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
  <span></span>
</div>

</div>

</div>

</section>

</div>

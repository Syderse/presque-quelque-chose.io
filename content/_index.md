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

#
  # <--- BLOC CALENDRIER 'PATAPHYSIQUE CORRIGÉ --->
  #
  - block: markdown
    id: pataphysique
    content:
      title: "almanach 'pataphysique"
      text: |
        <div style="text-align: center; font-family: 'Times New Roman', serif;">
          <h3 id="pataphysical-date" style="font-weight: bold; font-size: 1.5rem; color: var(--pataphysique-primary);">
            Chargement...
          </h3>
          <p id="pataphysical-activity" style="font-style: italic; font-size: 1.1rem; min-height: 1.2em;"></p>
        </div>

        <script src="/js/PataphysicalDate.js"></script>

        <script>
        document.addEventListener('DOMContentLoaded', async function() {
          let almanachData = {}; // Notre nouvelle source de données

          try {
            // --- ÉTAPE A: Charger l'ALMANACH (le nouveau JSON) ---
            try {
              const response = await fetch('/almanach/index.json');
              if (response.ok) {
                almanachData = await response.json();
                console.log("Almanach des inoccupations chargé.", almanachData);
              } else {
                console.warn("Fichier /almanach/index.json non trouvé. Seuls les saints officiels seront affichés.");
              }
            } catch (fetchError) {
              console.warn("Erreur lors du fetch de /almanach/index.json:", fetchError);
            }

            // --- ÉTAPE B: Calculer les dates ---
            if (typeof PataphysicalDate === 'undefined') {
              throw new Error("Moteur de conversion 'pataphysique (PataphysicalDate.js) non chargé.");
            }
            
            const pDateInstance = new PataphysicalDate(); // Date 'pata
            const today = new Date(); // Date Grégorienne

            // 1. Calcul de la date 'pata pour l'affichage
            const pDateString = `${pDateInstance.getDay()} ${pDateInstance.getMonthName()} ${pDateInstance.getFullYear()} E.P.`;

            // 2. Calcul de la clé Grégorienne (YYYY-MM-DD) pour la recherche
            const yyyy = today.getFullYear();
            const mm = String(today.getMonth() + 1).padStart(2, '0'); // +1 car getMonth() est 0-indexé
            const dd = String(today.getDate()).padStart(2, '0');
            const gregorianKey = `${yyyy}-${mm}-${dd}`; // ex: "2025-11-16"

            // --- ÉTAPE C: Trouver l'inoccupation (LA NOUVELLE LOGIQUE) ---
            
            // On récupère le saint officiel de la bibliothèque
            const officialSaint = pDateInstance.getSaintOfDay();

            // Priorité 1: Inoccupation de l'almanach (via clé grégorienne)
            // Priorité 2: Saint Officiel (de la bibliothèque JS)
            // Priorité 3: Vacuation par défaut
            const activity = almanachData[gregorianKey] || 
                               officialSaint || 
                               "Vacuation. Rien à célébrer ce jour.";

            // --- ÉTAPE D: Injecter dans le HTML ---
            const dateEl = document.getElementById('pataphysical-date');
            const activityEl = document.getElementById('pataphysical-activity');

            if (dateEl) dateEl.innerText = pDateString;
            if (activityEl) activityEl.innerHTML = activity; // innerHTML pour supporter <strong> etc.
            
          } catch (e) {
            console.error("Erreur lors de l'initialisation du widget 'pataphysique:", e);
            const el = document.getElementById('pataphysical-date');
            if (el) {
              el.innerText = "Erreur de conversion.";
              el.style.color = "red";
            }
            const activityEl = document.getElementById('pataphysical-activity');
            if (activityEl) activityEl.innerText = e.message;
          }
        });
        </script>
    design:
      # On le met dans une seule colonne
      columns: '1'
      # On ajoute un peu d'espace
      spacing:
        padding: ["2rem", 0, "2rem", 0]

---
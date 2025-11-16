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

# ... (votre section 'features' se termine ici) ...
      spacing:
        padding: ["1rem", 0, "2rem", 0] # Un peu d'air

#
# <--- NOUVEAU BLOC : CALENDRIER 'PATAPHYSIQUE AUTONOME --->
#
- block: markdown
  id: pataphysique
  content:
    title: "éphéméride 'pataphysique"
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
        let pataphysicalCustom = {}; // Initialiser en cas d'échec

        try {
          // --- ÉTAPE A: Charger les données CUSTOM (un seul fetch) ---
          // (On ignore les erreurs, car ce fichier est optionnel)
          try {
            const customResponse = await fetch('/data/pataphysique_custom.json');
            if (customResponse.ok) {
              pataphysicalCustom = await customResponse.json();
            } else {
              console.warn("Fichier pataphysique_custom.json non trouvé. Seuls les saints officiels seront affichés.");
            }
          } catch (fetchError) {
            console.warn("Erreur lors du fetch de pataphysique_custom.json:", fetchError);
          }

          // --- ÉTAPE B: Calculer la date ---
          if (typeof PataphysicalDate === 'undefined') {
            throw new Error("Moteur de conversion 'pataphysique non chargé.");
          }

          const pDateInstance = new PataphysicalDate();
          const pDate = {
            day: pDateInstance.getDay(),
            month: pDateInstance.getMonthName(),
            year: pDateInstance.getFullYear()
          };

          // --- ÉTAPE C: Trouver le saint (LA NOUVELLE LOGIQUE) ---
          const dateString = `${pDate.day} ${pDate.month} ${pDate.year} E.P.`;
          
          // La clé pour chercher dans notre JSON custom
          const dateKey = `${pDate.day}-${pDate.month}`;
          
          // On utilise la MÉTHODE de la bibliothèque !
          const officialSaint = pDateInstance.getSaintOfDay();

          // Priorité au custom, PUIS au saint officiel de la bibliothèque
          const activity = pataphysicalCustom[dateKey] || 
                           officialSaint || 
                           "Vacuation. Rien à célébrer ce jour.";

          // --- ÉTAPE D: Injecter dans le HTML ---
          const dateEl = document.getElementById('pataphysical-date');
          const activityEl = document.getElementById('pataphysical-activity');

          if (dateEl) dateEl.innerText = dateString;
          if (activityEl) activityEl.innerText = activity;

        } catch (e) {
          console.error("Erreur lors de l'initialisation du widget 'pataphysique:", e);
          const el = document.getElementById('pataphysical-date');
          if (el) {
            el.innerText = "Erreur de conversion.";
            el.style.color = "red"; // Rendre l'erreur visible
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

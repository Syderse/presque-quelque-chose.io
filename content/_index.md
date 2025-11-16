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
  # <--- NOUVEAU BLOC : GUICHET ALÉATOIRE --->
  #
  - block: markdown
    id: guichet-aleatoire
    content:
      text: |
        <div style="text-align: center; margin-top: 1rem; margin-bottom: 2rem;">
          <a href="#" id="random-article-button" style="font-size: 3rem; text-decoration: none; line-height: 1;" title="Guichet Aléatoire">
            🌀
          </a>
          <br>
          <small>guichet aléatoire</small>
        </div>

        <script>
        document.addEventListener('DOMContentLoaded', function() {
          // On cible le bouton que nous venons de créer
          const randomButton = document.getElementById('random-article-button');
          
          if (randomButton) {
            // On attache un écouteur d'événement au clic
            randomButton.addEventListener('click', async function(e) {
              e.preventDefault(); // Annule le clic sur le lien (le "#")
              
              try {
                // ÉTAPE C.1 : Récupérer notre fichier JSON
                // (Note : le nom correspond au "baseName" de l'Étape 1)
                const response = await fetch('/articles-aleatoires.json');
                
                if (!response.ok) {
                  throw new Error('La liste des articles est introuvable (réponse: ' + response.status + ')');
                }
                
                const articles = await response.json();
                
                if (!articles || articles.length === 0) {
                  throw new Error("Aucun article n'a été trouvé dans la liste.");
                }

                // ÉTAPE C.2 : Choisir un élément au hasard
                const randomIndex = Math.floor(Math.random() * articles.length);
                const randomArticle = articles[randomIndex];

                // ÉTAPE C.3 : Rediriger l'utilisateur
                if (randomArticle && randomArticle.url) {
                  window.location.href = randomArticle.url;
                } else {
                  throw new Error("L'article aléatoire sélectionné est invalide.");
                }

              } catch (error) {
                // En cas d'erreur (ex: JSON non trouvé), on prévient l'utilisateur
                console.error("Erreur du guichet aléatoire:", error);
                randomButton.innerText = "Erreur 😵";
              }
            });
          }
        });
        </script>
    design:
      # On le met dans une seule colonne
      columns: '1'

#
  # <--- BLOC CALENDRIER 'PATAPHYSIQUE CORRIGÉ --->
  #
  - block: markdown
    id: pataphysique
    content:
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
        padding: ["1rem", 0, "1rem", 0]
  
---
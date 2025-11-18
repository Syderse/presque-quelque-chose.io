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
        # Réduction drastique des marges (Haut, Droite, Bas, Gauche)
        padding: ["0", "0", "1rem", "0"]
      biography:
        style: 'text-align: justify; font-size: 0.8em;'
      avatar:
        size: medium
        shape: circle

  #
  # <--- BLOC CALENDRIER 'PATAPHYSIQUE --->
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
          let almanachData = {}; 

          try {
            try {
              const response = await fetch('/almanach/index.json');
              if (response.ok) {
                almanachData = await response.json();
              } 
            } catch (fetchError) {
              console.warn("Erreur fetch almanach", fetchError);
            }

            if (typeof PataphysicalDate === 'undefined') {
              throw new Error("Moteur 'pataphysique non chargé.");
            }
            
            const pDateInstance = new PataphysicalDate();
            const today = new Date();

            const pDateString = `${pDateInstance.getDay()} ${pDateInstance.getMonthName()} ${pDateInstance.getFullYear()} E.P.`;

            const yyyy = today.getFullYear();
            const mm = String(today.getMonth() + 1).padStart(2, '0'); 
            const dd = String(today.getDate()).padStart(2, '0');
            const gregorianKey = `${yyyy}-${mm}-${dd}`;

            const officialSaint = pDateInstance.getSaintOfDay();
            const activity = almanachData[gregorianKey] || officialSaint || "Vacuation.";

            const dateEl = document.getElementById('pataphysical-date');
            const activityEl = document.getElementById('pataphysical-activity');

            if (dateEl) dateEl.innerText = pDateString;
            if (activityEl) activityEl.innerHTML = activity; 
            
          } catch (e) {
            console.error("Erreur widget:", e);
          }
        });
        </script>
    design:
      columns: '1'
      spacing:
        # Espace réduit pour coller au bloc suivant
        padding: ["1rem", "0", "0.5rem", "0"]

  #
  # <--- BLOC FUSIONNÉ : GUICHET & COMPTEUR (CÔTE À CÔTE) --->
  #
  - block: markdown
    id: dashboard-mixte
    content:
      text: |
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center justify-center max-w-4xl mx-auto">
          
          <div class="text-center border-r-0 md:border-r md:border-gray-200 dark:md:border-gray-700 p-4">
            <div style="margin-bottom: 1rem;">
              <a href="#" id="random-article-button" style="font-size: 4rem; text-decoration: none; line-height: 1; transition: transform 0.2s;" title="Guichet Aléatoire" onmouseover="this.style.transform='scale(1.2)'" onmouseout="this.style.transform='scale(1)'">
                🌀
              </a>
              <br>
              <span class="text-xs font-mono uppercase tracking-widest text-gray-500">Clinamen</span>
            </div>
          </div>

          <div class="text-center p-4">
            {{< compteur-pataphysique >}}
          </div>

        </div>

        <script>
        document.addEventListener('DOMContentLoaded', function() {
          const randomButton = document.getElementById('random-article-button');
          if (randomButton) {
            randomButton.addEventListener('click', async function(e) {
              e.preventDefault(); 
              try {
                const response = await fetch('/articles-aleatoires.json');
                if (!response.ok) throw new Error('Erreur index');
                const articles = await response.json();
                if (!articles || articles.length === 0) throw new Error("Vide");
                
                const randomIndex = Math.floor(Math.random() * articles.length);
                const randomArticle = articles[randomIndex];

                if (randomArticle && randomArticle.url) {
                  // Petit effet visuel avant redirection
                  randomButton.innerText = "🚀";
                  setTimeout(() => { window.location.href = randomArticle.url; }, 300);
                } else {
                  throw new Error("URL invalide");
                }
              } catch (error) {
                console.error(error);
                randomButton.innerText = "⛔️";
              }
            });
          }
        });
        </script>
    design:
      columns: '1'
      background:
        color: 'bg-gray-50 dark:bg-slate-900' # Fond unifié pour la zone "Outils"
      spacing:
        # Padding interne au bloc
        padding: ["2rem", "0", "3rem", "0"]
---
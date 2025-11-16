---
title: 'Home'
date: 2023-10-24
type: landing
sections:
  # --- Bloc 1 : Biographie (Existant) ---
  - block: resume-biography
    content:
      # The user's folder name in content/authors/
      username: admin
    design:
      spacing:
        padding: [0, 0, 0, 0]
      biography:
        style: 'text-align: justify; font-size: 0.8em;'
      # Avatar customization
      avatar:
        size: medium
        shape: circle

  # --- Bloc 2 : NOUVEAU (Calendrier 'Pataphysique AVEC LOGIQUE INTÉGRÉE) ---
  - block: markdown
    id: calendrier
    content:
      # Titre du bloc (vide)
      title: ""
      # Le HTML, le pont de données, ET le script de logique
      text: |-
        <div id="pataphysique-widget" aria-live="polite">
            <div id="pataphysical-date">Chargement de la date 'pataphysique...</div>
            <div id="pataphysical-activity">Observation de l'activité du jour...</div>
        </div>

        <script>
          const pataphysicalSaints = {{.Site.Data.pataphysique_saints | jsonify | default "null" }};
          const pataphysicalCustom = {{.Site.Data.pataphysique_custom | jsonify | default "null" }};
        </script>

        <script src="{{ "/js/PataphysicalDate.js" | relURL }}"></script>

        <script>
          document.addEventListener('DOMContentLoaded', function() {
            // Cibler les éléments HTML
            const dateEl = document.getElementById('pataphysical-date');
            const activityEl = document.getElementById('pataphysical-activity');

            try {
              // --- Étape 1 : Vérifier les données ---
              if (!pataphysicalSaints || Object.keys(pataphysicalSaints).length === 0) {
                throw new Error("DONNÉES ÉCHOUÉES : 'pataphysique_saints.json' est vide ou invalide. Vérifiez le copier-coller du JSON.");
              }
              if (!pataphysicalCustom) {
                throw new Error("DONNÉES ÉCHOUÉES : 'pataphysique_custom.json' n'a pas pu être chargé.");
              }
              
              // --- Étape 2 : Vérifier la bibliothèque (Voie A) ---
              if (typeof PataphysicalDate === 'undefined') {
                throw new Error("BIBLIOTHÈQUE ÉCHOUÉE : 'PataphysicalDate.js' n'a pas pu être chargé. Vérifiez que le fichier existe bien dans /static/js/");
              }

              // --- Étape 3 : Exécuter la logique (si tout va bien) ---
              const pDateInstance = new PataphysicalDate();
              const pDate = {
                day: pDateInstance.getDay(),
                month: pDateInstance.getMonthName(),
                year: pDateInstance.getFullYear()
              };

              // --- Étape 4 : Rendu ---
              const dateString = `${pDate.day} ${pDate.month} ${pDate.year} E.P.`;
              const dateKey = `${pDate.day}-${pDate.month}`;
              
              const activity = pataphysicalCustom[dateKey] || 
                               pataphysicalSaints[dateKey] || 
                               "Vacuation. Rien à célébrer ce jour.";

              // Injection des résultats
              if (dateEl) dateEl.innerText = dateString;
              if (activityEl) activityEl.innerText = activity;

            } catch (e) {
              // --- Afficher l'erreur SPÉCIFIQUE sur la page ---
              console.error("Erreur 'Pataphysique DÉTAILLÉE:", e.message);
              if (dateEl) dateEl.innerText = "Erreur de conversion 'pataphysique.";
              
              // Affiche le message d'erreur détaillé directement dans le widget !
              if (activityEl) activityEl.innerText = e.message; 
            }
          });
        </script>
    design:
      # Design pleine largeur
      columns: '1'
      spacing:
        padding: ['3rem', 0, '0', 0] # Ajout d'un peu d'espace au-dessus

  # --- Bloc 3 : Almanach des Inoccupations (Inchangé) ---
  - block: markdown
    id: almanach
    content:
      # Titre de la section
      title: "Almanach des Inoccupations"
      # Le HTML, CSS, et JS de l'almanach
      text: |-
        <style>
          .almanac-container { min-height: 300px; }
          .almanac-entry { margin-bottom: 2rem; padding-bottom: 1.5rem; border-bottom: 1px dashed var(--tw-prose-borders); }
          .almanac-entry:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
          .almanac-header { border-bottom: 1px solid var(--tw-prose-borders); padding-bottom: 1rem; margin-bottom: 1.5rem; }
          .almanac-date { font-size: 1.5rem; font-weight: bold; color: var(--tw-prose-headings); }
          .almanac-content { font-size: 1.25rem; line-height: 1.7; }
          .almanac-content strong { color: var(--hb-color-primary-600); }
        </style>
        <div id="almanac-wrapper" style="display: none;">
          <div class="almanac-container">
            <div id="almanac-content" class="almanac-content">
              <p>recherche des inoccupations de la semaine...</p>
            </div>
          </div>
        </div>
        <script>
          document.addEventListener('DOMContentLoaded', () => {
            let allEvents = [];
            const userLocale = 'fr-fr';
            const dateOptions = { day: 'numeric', month: 'long', year: 'numeric' };
            const wrapperEl = document.getElementById('almanac-wrapper');
            const contentEl = document.getElementById('almanac-content');
            const normalizeDate = (date) => {
              let d = new Date(date);
              d.setHours(0, 0, 0, 0);
              return d;
            };
            const today = new Date();
            const todayNormalized = normalizeDate(new Date());
            const dayOfWeek = today.getDay(); // 0=dimanche, 1=lundi
            const daysToSubtract = (dayOfWeek === 0) ? 6 : (dayOfWeek - 1);
            const startOfWeek = new Date(todayNormalized);
            startOfWeek.setDate(todayNormalized.getDate() - daysToSubtract);
            const endOfWeek = new Date(startOfWeek);
            endOfWeek.setDate(startOfWeek.getDate() + 6);
            endOfWeek.setHours(23, 59, 59, 999);
            fetch('/almanach/index.xml?v=' + new Date().getTime())
              .then(response => response.text())
              .then(str => new window.DOMParser().parseFromString(str, 'text/xml'))
              .then(data => {
                const items = data.querySelectorAll('item');
                items.forEach(item => {
                  allEvents.push({
                    title: item.querySelector('title').textContent,
                    description: item.querySelector('description').textContent,
                    pubDate: item.querySelector('pubDate').textContent
                  });
                });
                const weekEvents = allEvents.filter(event => {
                  const eventDate = normalizeDate(event.pubDate);
                  return eventDate >= startOfWeek && eventDate <= endOfWeek;
                });
                weekEvents.sort((a, b) => new Date(a.pubDate) - new Date(b.pubDate));
                if (weekEvents.length > 0) {
                  let htmlContent = '';
                  weekEvents.forEach(event => {
                    const eventDate = new Date(event.pubDate);
                    htmlContent += `
                      <div class="almanac-entry">
                        <div class="almanac-header">
                          <div class="almanac-date">${eventDate.toLocaleDateString(userLocale, dateOptions)}</div>
                        </div>
                        <div class="almanac-content">
                          ${event.description}
                        </div>
                      </div>
                    `;
                  });
                  contentEl.innerHTML = htmlContent;
                } else {
                  contentEl.innerHTML = "<p>aucune inoccupation n'est prévue pour cette semaine. profitez du vide.</p>";
                }
                wrapperEl.style.display = 'block';
              })
              .catch(err => {
                console.error("erreur pataphysique:", err);
                contentEl.innerHTML = "<p>l'almanach n'a pas pu être chargé. les ondes sont brouillées.</p>";
                wrapperEl.style.display = 'block';
              });
          });
        </script>
    design:
      # Design pleine largeur
      columns: '1'

  # --- Bloc 4 : Collection (Existant) ---
  - block: collection
    content:
      filters:
        folders:
          - blog
    design:
      spacing:
        padding: ['3rem', 0, '6rem', 0]
---
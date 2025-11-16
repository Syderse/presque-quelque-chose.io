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
        size: medium  # Options: small (150px), medium (200px, default), large (320px), xl (400px), xxl (500px)
        shape: circle # Options: circle (default), square, rounded

  # --- Bloc 2 : NOUVEAU (Calendrier 'Pataphysique) ---
  - block: markdown
    id: calendrier
    content:
      # Titre du bloc (vide)
      title: ""
      # Le HTML du widget
      text: |-
        <div id="pataphysique-widget" aria-live="polite">
            <div id="pataphysical-date">Chargement de la date 'pataphysique...</div>
            <div id="pataphysical-activity">Observation de l'activité du jour...</div>
        </div>
    design:
      # Design pleine largeur
      columns: '1'
      spacing:
        padding: ['3rem', 0, '0', 0] # Ajout d'un peu d'espace au-dessus

  # --- Bloc 3 : NOUVEAU (Almanach des Inoccupations) ---
  - block: markdown
    id: almanach
    content:
      # Titre de la section
      title: "Almanach des Inoccupations"
      # Le HTML, CSS, et JS de l'almanach
      text: |-
        <style>
          .almanac-container {
            min-height: 300px;
          }
          .almanac-entry {
            margin-bottom: 2rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px dashed var(--tw-prose-borders);
          }
          .almanac-entry:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
          }
          .almanac-header {
            border-bottom: 1px solid var(--tw-prose-borders);
            padding-bottom: 1rem;
            margin-bottom: 1.5rem;
          }
          .almanac-date {
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--tw-prose-headings);
          }
          .almanac-content {
            font-size: 1.25rem;
            line-height: 1.7;
          }
          .almanac-content strong {
            color: var(--hb-color-primary-600);
          }
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

            // éléments de l'interface
            const wrapperEl = document.getElementById('almanac-wrapper');
            const contentEl = document.getElementById('almanac-content');
            
            // fonction pour normaliser la date (enlève l'heure)
            const normalizeDate = (date) => {
              let d = new Date(date);
              d.setHours(0, 0, 0, 0);
              return d;
            };

            // --- logique : calculer le début et la fin de la semaine ---
            
            const today = new Date();
            const todayNormalized = normalizeDate(new Date());
            const dayOfWeek = today.getDay(); // 0=dimanche, 1=lundi, ..., 6=samedi

            const daysToSubtract = (dayOfWeek === 0) ? 6 : (dayOfWeek - 1);
            
            const startOfWeek = new Date(todayNormalized);
            startOfWeek.setDate(todayNormalized.getDate() - daysToSubtract);
            
            const endOfWeek = new Date(startOfWeek);
            endOfWeek.setDate(startOfWeek.getDate() + 6);
            
            endOfWeek.setHours(23, 59, 59, 999);
            
            // --- fin de la logique ---

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

                // 2. filtrer les événements pour la semaine en cours
                const weekEvents = allEvents.filter(event => {
                  const eventDate = normalizeDate(event.pubDate);
                  return eventDate >= startOfWeek && eventDate <= endOfWeek;
                });

                // 3. trier les événements de la semaine par date
                weekEvents.sort((a, b) => new Date(a.pubDate) - new Date(b.pubDate));

                // 4. afficher les événements (ou un message si vide)
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
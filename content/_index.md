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
  # ----- bloc almanach sans catégorie -----
  #
  - block: markdown
    id: almanach
    content:
      title: "almanach des inoccupations personnelles"
      subtitle: "les inoccupations de la semaine en cours."
      text: |
        <style>
          .almanac-container {
            font-family: 'georgia', 'times new roman', serif;
            border: 4px double var(--tw-prose-bold);
            border-radius: 0;
            background: var(--tw-prose-bg);
            box-shadow: 5px 5px 0px 0px var(--tw-prose-bold);
            padding: 2rem;
            margin-bottom: 2rem;
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
            
            // 
            // ----- CORRECTION N°1 : on met la fin de la semaine à 23:59:59 -----
            //
            endOfWeek.setHours(23, 59, 59, 999);
            
            // --- fin de la logique ---

            // 1. fetcher le flux rss (xml)
            //
            // ----- CORRECTION N°2 : on ajoute un cache-buster -----
            //
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
                  // on normalise la date de l'événement (qui vient du xml)
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
                  // pas d'événement cette semaine
                  contentEl.innerHTML = "<p>aucune inoccupation n'est prévue pour cette semaine. profitez du vide.</p>";
                }

                // quoi qu'il arrive, on affiche le conteneur
                wrapperEl.style.display = 'block';
                
              })
              .catch(err => {
                console.error("erreur pataphysique:", err);
                contentEl.innerHTML = "<p>l'almanach n'a pas pu être chargé. les ondes sont brouillées.</p>";
                wrapperEl.style.display = 'block';
              });
          });
        </script>
---
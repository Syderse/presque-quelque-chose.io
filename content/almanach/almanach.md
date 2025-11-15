---
title: "almanach des inoccupations"
type: landing # utilise une page 'landing' pour la pleine largeur
sections:
  - block: markdown
    id: almanac-viewer
    content:
      title: "almanach des inoccupations impersonnelles"
      subtitle: "l'éphéméride 'pataphysique du jour."
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
          .almanac-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--tw-prose-borders);
            padding-bottom: 1rem;
            margin-bottom: 1.5rem;
          }
          .almanac-date {
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--tw-prose-headings);
          }
          .almanac-category {
            font-family: 'courier new', monospace;
            font-size: 1rem;
            font-style: italic;
            background-color: var(--tw-prose-invert-bg);
            color: var(--tw-prose-invert-body);
            padding: 0.25rem 0.5rem;
          }
          .almanac-content {
            font-size: 1.25rem;
            line-height: 1.7;
          }
          .almanac-content strong {
            color: var(--hb-color-primary-600);
          }
          
          /* les boutons de navigation ont disparu du css, car ils ont disparu du html */

        </style>

        <div id="almanac-wrapper" style="display: none;">
          <div class="almanac-container">
            <div class="almanac-header">
              <div id="almanac-date" class="almanac-date">chargement...</div>
              <div id="almanac-category" class="almanac-category"></div>
            </div>
            <div id="almanac-content" class="almanac-content">
              <p>recherche de l'inoccupation correspondante...</p>
            </div>
          </div>
          </div>
        
        <script>
          document.addEventListener('DOMContentLoaded', () => {
            let allEvents = [];
            // currentEventIndex n'est plus nécessaire

            // formats de date
            const userLocale = 'fr-fr';
            const dateOptions = { day: 'numeric', month: 'long', year: 'numeric' };

            // éléments de l'interface
            const wrapperEl = document.getElementById('almanac-wrapper'); // <- nouvel élément
            const dateEl = document.getElementById('almanac-date');
            const categoryEl = document.getElementById('almanac-category');
            const contentEl = document.getElementById('almanac-content');
            
            // modification clé 3 : les variables prevBtn et nextBtn sont supprimées.

            // fonction pour normaliser la date (enlève l'heure)
            const normalizeDate = (date) => {
              let d = new Date(date);
              d.setHours(0, 0, 0, 0);
              return d;
            };

            // fonction pour afficher l'événement trouvé
            const displayEvent = (event) => {
              if (!event) return;
              
              const eventDate = new Date(event.pubDate);
              
              dateEl.textContent = eventDate.toLocaleDateString(userLocale, dateOptions);
              categoryEl.textContent = event.category;
              contentEl.innerHTML = event.description; // utilise innerhtml pour les balises <strong>
            };

            // fonction pour trouver l'événement du jour
            const findEventForDate = (date) => {
              const normalizedToday = normalizeDate(date);
              
              // on trie les événements par date au cas où
              allEvents.sort((a, b) => new Date(a.pubDate) - new Date(b.pubDate));

              // on utilise .find() au lieu de .findIndex() pour avoir l'événement directement
              const eventToday = allEvents.find(event => {
                return normalizeDate(event.pubDate).getTime() === normalizedToday.getTime();
              });

              return eventToday; // retourne l'événement ou 'undefined'
            };

            // --- exécution ---
            // 1. fetcher le flux rss
            fetch('/almanach/index.xml')
              .then(response => response.text())
              .then(str => new window.DOMParser().parseFromString(str, 'text/xml'))
              .then(data => {
                const items = data.querySelectorAll('item');
                
                items.forEach(item => {
                  allEvents.push({
                    title: item.querySelector('title').textContent,
                    description: item.querySelector('description').textContent,
                    pubDate: item.querySelector('pubDate').textContent,
                    category: item.querySelector('category') ? item.querySelector('category').textContent : '(général)'
                  });
                });

                // 2. trouver l'événement d'aujourd'hui
                const today = new Date();
                let eventFound = findEventForDate(today); // c'est l'objet événement, ou 'undefined'

                // 
                // modification clé 4 : la logique d'affichage
                //
                if (eventFound) {
                  // un événement est trouvé !
                  displayEvent(eventFound);
                  // on affiche le conteneur
                  wrapperEl.style.display = 'block';
                } else {
                  // pas d'événement pour aujourd'hui.
                  // on ne fait rien. la page reste blanche.
                  // la 'div' almanac-wrapper reste en 'display: none'.
                  console.log("aucune inoccupation n'est prévue pour aujourd'hui. profitez du vide.");
                }

                //
                // modification clé 5 : 
                // les 'event listeners' pour prevBtn et nextBtn ont été supprimés.
                //
                
              })
              .catch(err => {
                console.error("erreur pataphysique:", err);
                // on n'affiche rien à l'utilisateur, on log juste en console.
              });
          });
        </script>
---
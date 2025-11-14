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
            font-family: 'Georgia', 'Times New Roman', serif;
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
            font-family: 'Courier New', monospace;
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
          .almanac-nav {
            display: flex;
            justify-content: space-between;
            margin-top: 1.5rem;
            font-family: sans-serif;
          }
          .almanac-nav-btn {
            padding: 0.5rem 1rem;
            border: 1px solid var(--tw-prose-borders);
            text-decoration: none;
            cursor: pointer;
            user-select: none;
          }
          .almanac-nav-btn:hover {
            background-color: var(--tw-prose-invert-bg);
            color: var(--tw-prose-invert-body);
          }
        </style>

        <div id="almanac-wrapper">
          <div class="almanac-container">
            <div class="almanac-header">
              <div id="almanac-date" class="almanac-date">chargement...</div>
              <div id="almanac-category" class="almanac-category"></div>
            </div>
            <div id="almanac-content" class="almanac-content">
              <p>recherche de l'inoccupation correspondante...</p>
            </div>
          </div>
          <div class="almanac-nav">
            <div id="almanac-prev" class="almanac-nav-btn">← occupation précédente</div>
            <div id="almanac-next" class="almanac-nav-btn">occupation suivante →</div>
          </div>
        </div>
        
        <script>
          document.addEventListener('DOMContentLoaded', () => {
            let allEvents = [];
            let currentEventIndex = -1;

            // formats de date
            const userLocale = 'fr-fr';
            const dateOptions = { day: 'numeric', month: 'long', year: 'numeric' };

            // éléments de l'interface
            const dateEl = document.getElementById('almanac-date');
            const categoryEl = document.getElementById('almanac-category');
            const contentEl = document.getElementById('almanac-content');
            const prevBtn = document.getElementById('almanac-prev');
            const nextBtn = document.getElementById('almanac-next');

            // fonction pour normaliser la date (enlève l'heure)
            const normalizeDate = (date) => {
              let d = new Date(date);
              d.setHours(0, 0, 0, 0);
              return d;
            };

            // fonction pour afficher un événement par son index
            const displayEvent = (index) => {
              if (index < 0 || index >= allEvents.length) return;
              
              currentEventIndex = index;
              const event = allEvents[index];
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

              const eventIndex = allEvents.findIndex(event => {
                return normalizeDate(event.pubDate).getTime() === normalizedToday.getTime();
              });

              return eventIndex;
            };

            // --- exécution ---
            // 1. fetcher le flux rss (xml) généré par hugo
            // !! important : le script cherche les données dans /agenda/index.xml
            fetch('/agenda/index.xml')
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
                let eventIndex = findEventForDate(today);

                if (eventIndex !== -1) {
                  displayEvent(eventIndex);
                } else {
                  // si pas d'événement, afficher un message
                  dateEl.textContent = today.toLocaleDateString(userLocale, dateOptions);
                  categoryEl.textContent = "(repos)";
                  contentEl.textContent = "aucune inoccupation n'est prévue pour aujourd'hui. profitez du vide.";
                }

                // 3. lier les boutons de navigation
                prevBtn.addEventListener('click', () => {
                  if (currentEventIndex > 0) {
                    displayEvent(currentEventIndex - 1);
                  } else if (allEvents.length > 0) {
                    displayEvent(allEvents.length - 1); // boucle vers la fin
                  }
                });

                nextBtn.addEventListener('click', () => {
                  if (currentEventIndex < allEvents.length - 1) {
                    displayEvent(currentEventIndex + 1);
                  } else if (allEvents.length > 0) {
                    displayEvent(0); // boucle vers le début
                  }
                });
              })
              .catch(err => {
                console.error("erreur pataphysique:", err);
                dateEl.textContent = "erreur";
                contentEl.textContent = "l'almanach n'a pas pu être chargé. les ondes sont brouillées.";
              });
          });
        </script>
---
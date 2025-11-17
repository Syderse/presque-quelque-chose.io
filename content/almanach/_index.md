---
title: "almanach des inoccupations"
type: landing 
outputs: ["HTML", "JSON-ALMANACH"] # <--- C'est la ligne CRUCIALE qui active le JSON uniquement pour cette page
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

            // formats de date
            const userLocale = 'fr-fr';
            const dateOptions = { day: 'numeric', month: 'long', year: 'numeric' };

            // éléments de l'interface
            const wrapperEl = document.getElementById('almanac-wrapper');
            const dateEl = document.getElementById('almanac-date');
            const categoryEl = document.getElementById('almanac-category');
            const contentEl = document.getElementById('almanac-content');
            
            // fonction pour normaliser la date (enlève l'heure)
            const normalizeDate = (date) => {
              let d = new Date(date);
              d.setHours(0, 0, 0, 0);
              return d;
            };

            // fonction pour afficher l'événement trouvé
            const displayEvent = (event) => {
              if (!event) return;
              
              // Note: event.date vient du JSON
              const eventDate = new Date(event.date); 
              
              dateEl.textContent = eventDate.toLocaleDateString(userLocale, dateOptions);
              categoryEl.textContent = event.category || 'inoccupation';
              contentEl.innerHTML = event.content; 
            };

            // fonction pour trouver l'événement du jour
            const findEventForDate = (date) => {
              const normalizedToday = normalizeDate(date);
              
              // on trie les événements par date
              allEvents.sort((a, b) => new Date(a.date) - new Date(b.date));

              const eventToday = allEvents.find(event => {
                return normalizeDate(event.date).getTime() === normalizedToday.getTime();
              });

              return eventToday; 
            };

            // --- exécution ---
            // 1. Fetcher le JSON (et non plus le XML/RSS)
            fetch('/almanach/index.json')
              .then(response => {
                if (!response.ok) {
                   throw new Error("HTTP error " + response.status);
                }
                return response.json();
              })
              .then(data => {
                // Hugo retourne généralement un tableau d'objets
                // Nous adaptons la lecture pour le format JSON standard de Hugo
                data.forEach(item => {
                  allEvents.push({
                    title: item.title,
                    content: item.content || item.summary || item.description, // Supporte plusieurs formats de sortie
                    date: item.date,
                    category: item.categories ? item.categories[0] : (item.category || '(général)')
                  });
                });

                // 2. trouver l'événement d'aujourd'hui
                const today = new Date();
                let eventFound = findEventForDate(today); 

                if (eventFound) {
                  displayEvent(eventFound);
                  wrapperEl.style.display = 'block';
                } else {
                  console.log("aucune inoccupation n'est prévue pour aujourd'hui.");
                  // Optionnel : afficher un message par défaut
                  // wrapperEl.style.display = 'block';
                  // contentEl.innerHTML = "Rien à signaler aujourd'hui. Vacuation totale.";
                }
              })
              .catch(err => {
                console.error("erreur chargement almanach:", err);
              });
          });
        </script>
---
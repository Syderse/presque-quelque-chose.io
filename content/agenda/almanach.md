---
title: "almanach des inoccupations"
type: landing # nous utilisons une page 'landing' pour avoir une pleine largeur
sections:
  - block: markdown
    id: almanac-viewer
    content:
      title: "almanach des inoccupations"
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
            color: var(--hb-color-primary-600); /* surligne les "==" */
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
          .almanac-hidden {
            display: none;
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
        
        {{< include "layouts/partials/hooks/body-end/almanac-logic.html" >}}
---
(() => {
  "use strict";

  const PAGE_SIZE = 50;
  const root = document.querySelector("[data-antenne-radio-root]");
  if (!root) return;

  const byId = (id) => document.getElementById(id);
  const grid = byId("antenne-radio-card-grid");
  const form = byId("antenne-radio-filter-form");
  const status = byId("antenne-radio-filter-status");
  const totalCounter = byId("antenne-radio-total-signals");
  const visibleCounter = byId("antenne-radio-visible-signals");
  const categorySelect = byId("antenne-radio-filter-category");
  const sourceSelect = byId("antenne-radio-filter-source");
  const languageSelect = byId("antenne-radio-filter-language");
  const yearSelect = byId("antenne-radio-filter-year");
  const sortSelect = byId("antenne-radio-filter-sort");
  const searchInput = byId("antenne-radio-filter-search");
  const loadMore = byId("load-more");

  const activeFiltersBar = byId("active-filters-bar");
  const activeFiltersBadges = activeFiltersBar ? activeFiltersBar.querySelector(".active-filters-badges") : null;
  const clearFiltersBtn = byId("clear-filters");

  if (!grid || !form || !status || !loadMore) return;

  document.documentElement.classList.add("antenne-radio-js-enabled");

  const SORT_LABELS = {
    "date-asc": "Date ↑ (ancien d'abord)",
    "title-asc": "Titre A→Z"
  };

  const labels = {
    blog: "billets et blogs",
    journal_article: "articles académiques",
    hal: "HAL",
    rss: "RSS",
    und: "langue non déclarée",
    fr: "français",
    en: "anglais"
  };

  const collator = new Intl.Collator("fr", { sensitivity: "base" });
  const sourceNames = new Map();
  let items = [];
  let filteredItems = [];
  let visibleLimit = PAGE_SIZE;

  const normalize = (value) => String(value || "")
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase();

  const labelFor = (value) => labels[value] || value || "non déclaré";

  const safeUrl = (value) => {
    const url = String(value || "");
    return /^https?:\/\//.test(url) ? url : "#";
  };

  const formatDate = (value) => {
    if (!value) return "date inconnue";
    const date = new Date(value);
    if (Number.isNaN(date.valueOf())) return "date inconnue";
    return new Intl.DateTimeFormat("fr-FR", { dateStyle: "medium" }).format(date);
  };

  const makeText = (tagName, className, text) => {
    const element = document.createElement(tagName);
    if (className) element.className = className;
    element.textContent = text;
    return element;
  };

  const makeMeta = (text) => makeText("span", "antenne-radio-meta", text);

  const setStatus = (shown, matching) => {
    const signalLabel = shown > 1 ? "signaux" : "signal";
    const displayedLabel = shown > 1 ? "affichés" : "affiché";
    status.textContent = `${shown} ${signalLabel} ${displayedLabel} sur ${matching} résultat${matching > 1 ? "s" : ""}.`;
  };

  const resetOptions = (select) => {
    if (select) select.length = 1;
  };

  const fillSelect = (select, values, formatter) => {
    if (!select) return;
    resetOptions(select);
    values
      .filter(Boolean)
      .sort((a, b) => collator.compare(formatter(a), formatter(b)))
      .forEach((value) => {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = formatter(value);
        select.append(option);
      });
  };

  const fillYearSelect = (select) => {
    if (!select) return;
    resetOptions(select);
    const years = Array.from(new Set(
      items.map((item) => item.published_at ? item.published_at.slice(0, 4) : null).filter(Boolean)
    )).sort((a, b) => b.localeCompare(a));
    years.forEach((year) => {
      const option = document.createElement("option");
      option.value = year;
      option.textContent = year;
      select.append(option);
    });
  };

  const hydrateControls = (sources) => {
    sources.forEach((source) => {
      if (source.attribution_id) sourceNames.set(source.attribution_id, source.name || source.attribution_id);
    });

    fillSelect(categorySelect, Array.from(new Set(items.map((item) => item.source_type))), labelFor);
    fillSelect(
      sourceSelect,
      Array.from(new Set(items.map((item) => item.attribution_id))),
      (value) => sourceNames.get(value) || value
    );
    fillSelect(languageSelect, Array.from(new Set(items.map((item) => item.language))), labelFor);
    fillYearSelect(yearSelect);
  };

  const createCard = (item) => {
    const article = document.createElement("article");
    article.className = "antenne-radio-card";
    article.dataset.family = item.source_family || "";
    article.setAttribute("role", "listitem");

    const head = makeText("div", "antenne-radio-card-head", "");
    head.append(makeText("div", "antenne-radio-source-kicker", item.source_name || "source non déclarée"));
    if (item.container_title) {
      head.append(makeText("div", "antenne-radio-container-title", item.container_title));
    }

    const body = makeText("div", "antenne-radio-card-body", "");

    const title = makeText("h3", "antenne-radio-card-title", "");
    const titleLink = document.createElement("a");
    titleLink.href = safeUrl(item.url);
    titleLink.target = "_blank";
    titleLink.rel = "noopener noreferrer";
    titleLink.textContent = item.title || "Titre non déclaré";
    title.append(titleLink);
    body.append(title);

    if (Array.isArray(item.authors) && item.authors.length > 0) {
      const MAX_AUTHORS = 3;
      const shown = item.authors.slice(0, MAX_AUTHORS);
      const extra = item.authors.length > MAX_AUTHORS ? ` +${item.authors.length - MAX_AUTHORS}` : "";
      body.append(makeText("p", "antenne-radio-authors", shown.join(", ") + extra));
    }

    const meta = makeText("div", "antenne-radio-meta-list", "");
    meta.setAttribute("aria-label", "métadonnées publiques");
    meta.append(makeMeta(labelFor(item.source_type)));
    meta.append(makeMeta(labelFor(item.language)));
    if (item.doi) meta.append(makeMeta(`doi: ${item.doi}`));

    const footer = makeText("div", "antenne-radio-card-footer", "");
    footer.append(makeText("span", "antenne-radio-date", formatDate(item.published_at)));

    const origin = document.createElement("a");
    origin.className = "antenne-radio-link";
    origin.href = safeUrl(item.url);
    origin.target = "_blank";
    origin.rel = "noopener noreferrer";
    origin.textContent = "origine";
    footer.append(origin);

    body.append(meta, footer);
    article.append(head, body);
    return article;
  };

  const createEmptyState = () => {
    const container = document.createElement("div");
    container.className = "antenne-radio-empty-state";

    const iconContainer = document.createElement("div");
    iconContainer.className = "antenne-radio-empty-icon";
    iconContainer.setAttribute("aria-hidden", "true");

    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("viewBox", "0 0 24 24");
    svg.setAttribute("width", "40");
    svg.setAttribute("height", "40");
    svg.setAttribute("fill", "none");
    svg.setAttribute("stroke", "currentColor");
    svg.setAttribute("stroke-width", "2");
    svg.setAttribute("stroke-linecap", "round");
    svg.setAttribute("stroke-linejoin", "round");
    svg.setAttribute("focusable", "false");

    const path1 = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path1.setAttribute("d", "M4.9 19.1C1 15.2 1 8.8 4.9 4.9");
    const path2 = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path2.setAttribute("d", "M7.8 16.2c-2.3-2.3-2.3-6.1 0-8.5");
    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", "12");
    circle.setAttribute("cy", "12");
    circle.setAttribute("r", "1");
    const path3 = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path3.setAttribute("d", "M16.2 7.8c2.3 2.3 2.3 6.1 0 8.5");
    const path4 = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path4.setAttribute("d", "M19.1 4.9C23 8.8 23 15.2 19.1 19.1");
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", "1");
    line.setAttribute("y1", "1");
    line.setAttribute("x2", "23");
    line.setAttribute("y2", "23");

    svg.append(path1, path2, circle, path3, path4, line);
    iconContainer.append(svg);

    const text = document.createElement("p");
    text.className = "antenne-radio-empty-text";
    text.textContent = "Aucun signal ne correspond à vos critères de recherche.";

    const resetBtn = document.createElement("button");
    resetBtn.type = "button";
    resetBtn.className = "antenne-radio-empty-reset";
    resetBtn.textContent = "Réinitialiser les filtres";
    resetBtn.addEventListener("click", () => {
      if (categorySelect) categorySelect.value = "";
      if (sourceSelect) sourceSelect.value = "";
      if (languageSelect) languageSelect.value = "";
      if (yearSelect) yearSelect.value = "";
      if (sortSelect) sortSelect.value = "date-desc";
      if (searchInput) searchInput.value = "";
      applyFilters();
      if (searchInput) searchInput.focus();
    });

    container.append(iconContainer, text, resetBtn);
    return container;
  };

  const itemMatches = (item) => {
    const category = categorySelect ? categorySelect.value : "";
    const source = sourceSelect ? sourceSelect.value : "";
    const language = languageSelect ? languageSelect.value : "";
    const year = yearSelect ? yearSelect.value : "";
    const search = normalize(searchInput ? searchInput.value : "");
    const text = normalize([
      item.title,
      item.source_name,
      item.doi,
      item.source_type,
      item.language,
      item.container_title,
      Array.isArray(item.authors) ? item.authors.join(" ") : ""
    ].join(" "));

    return (!category || item.source_type === category)
      && (!source || item.attribution_id === source)
      && (!language || item.language === language)
      && (!year || (item.published_at || "").startsWith(year))
      && (!search || text.includes(search));
  };

  const sortItems = (arr) => {
    const sort = sortSelect ? sortSelect.value : "date-desc";
    return [...arr].sort((a, b) => {
      if (sort === "date-asc") {
        return new Date(a.published_at || 0) - new Date(b.published_at || 0);
      }
      if (sort === "title-asc") {
        return collator.compare(a.title || "", b.title || "");
      }
      return new Date(b.published_at || 0) - new Date(a.published_at || 0);
    });
  };

  const renderActiveFilters = () => {
    if (!activeFiltersBar || !activeFiltersBadges) return;

    activeFiltersBadges.replaceChildren();
    const active = [];

    const category = categorySelect ? categorySelect.value : "";
    const source = sourceSelect ? sourceSelect.value : "";
    const language = languageSelect ? languageSelect.value : "";
    const year = yearSelect ? yearSelect.value : "";
    const sort = sortSelect ? sortSelect.value : "date-desc";
    const search = searchInput ? searchInput.value.trim() : "";

    if (category) active.push({ label: `Catégorie : ${labelFor(category)}`, element: categorySelect });
    if (source) active.push({ label: `Source : ${sourceNames.get(source) || source}`, element: sourceSelect });
    if (language) active.push({ label: `Langue : ${labelFor(language)}`, element: languageSelect });
    if (year) active.push({ label: `Année : ${year}`, element: yearSelect });
    if (sort && sort !== "date-desc") {
      active.push({ label: `Tri : ${SORT_LABELS[sort] || sort}`, element: sortSelect, defaultValue: "date-desc" });
    }
    if (search) active.push({ label: `Recherche : « ${search} »`, element: searchInput });

    if (active.length > 0) {
      activeFiltersBar.removeAttribute("hidden");
      activeFiltersBar.style.display = "flex";

      active.forEach((filter) => {
        const badge = document.createElement("button");
        badge.type = "button";
        badge.className = "active-filter-badge";
        badge.setAttribute("aria-label", `Retirer le filtre ${filter.label}`);
        badge.setAttribute("role", "listitem");

        const textSpan = document.createElement("span");
        textSpan.textContent = filter.label;
        badge.append(textSpan);

        const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        svg.setAttribute("viewBox", "0 0 24 24");
        svg.setAttribute("width", "14");
        svg.setAttribute("height", "14");
        svg.setAttribute("fill", "none");
        svg.setAttribute("stroke", "currentColor");
        svg.setAttribute("stroke-width", "3");
        svg.setAttribute("stroke-linecap", "round");
        svg.setAttribute("stroke-linejoin", "round");
        svg.setAttribute("aria-hidden", "true");
        svg.setAttribute("focusable", "false");

        const line1 = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line1.setAttribute("x1", "18");
        line1.setAttribute("y1", "6");
        line1.setAttribute("x2", "6");
        line1.setAttribute("y2", "18");
        const line2 = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line2.setAttribute("x1", "6");
        line2.setAttribute("y1", "6");
        line2.setAttribute("x2", "18");
        line2.setAttribute("y2", "18");
        svg.append(line1, line2);
        badge.append(svg);

        badge.addEventListener("click", () => {
          filter.element.value = filter.defaultValue !== undefined ? filter.defaultValue : "";
          applyFilters();
          filter.element.focus();
        });

        activeFiltersBadges.append(badge);
      });
    } else {
      activeFiltersBar.setAttribute("hidden", "");
      activeFiltersBar.style.display = "none";
    }
  };

  const updateURL = () => {
    const params = new URLSearchParams();
    const category = categorySelect ? categorySelect.value : "";
    const source = sourceSelect ? sourceSelect.value : "";
    const language = languageSelect ? languageSelect.value : "";
    const year = yearSelect ? yearSelect.value : "";
    const sort = sortSelect ? sortSelect.value : "date-desc";
    const search = searchInput ? searchInput.value.trim() : "";

    if (category) params.set("cat", category);
    if (source) params.set("src", source);
    if (language) params.set("lang", language);
    if (year) params.set("year", year);
    if (sort && sort !== "date-desc") params.set("sort", sort);
    if (search) params.set("q", search);

    const queryString = params.toString();
    const newUrl = window.location.pathname + (queryString ? "?" + queryString : "");
    window.history.replaceState(null, "", newUrl);
  };

  const syncFiltersFromURL = () => {
    const params = new URLSearchParams(window.location.search);
    const q = params.get("q") || "";
    const cat = params.get("cat") || "";
    const src = params.get("src") || "";
    const lang = params.get("lang") || "";
    const year = params.get("year") || "";
    const sort = params.get("sort") || "date-desc";

    if (searchInput) searchInput.value = q;

    if (categorySelect) {
      const optionExists = Array.from(categorySelect.options).some((opt) => opt.value === cat);
      categorySelect.value = optionExists ? cat : "";
    }
    if (sourceSelect) {
      const optionExists = Array.from(sourceSelect.options).some((opt) => opt.value === src);
      sourceSelect.value = optionExists ? src : "";
    }
    if (languageSelect) {
      const optionExists = Array.from(languageSelect.options).some((opt) => opt.value === lang);
      languageSelect.value = optionExists ? lang : "";
    }
    if (yearSelect) {
      const optionExists = Array.from(yearSelect.options).some((opt) => opt.value === year);
      yearSelect.value = optionExists ? year : "";
    }
    if (sortSelect) {
      const optionExists = Array.from(sortSelect.options).some((opt) => opt.value === sort);
      sortSelect.value = optionExists ? sort : "date-desc";
    }
  };

  const render = () => {
    const visibleItems = filteredItems.slice(0, visibleLimit);
    const fragment = document.createDocumentFragment();

    grid.replaceChildren();
    visibleItems.forEach((item) => fragment.append(createCard(item)));

    if (fragment.childNodes.length) {
      grid.append(fragment);
    } else {
      grid.append(createEmptyState());
    }

    if (totalCounter) totalCounter.textContent = String(items.length);
    if (visibleCounter) visibleCounter.textContent = String(visibleItems.length);
    setStatus(visibleItems.length, filteredItems.length);

    loadMore.hidden = visibleLimit >= filteredItems.length;
  };

  const applyFilters = () => {
    visibleLimit = PAGE_SIZE;
    filteredItems = sortItems(items.filter(itemMatches));
    updateURL();
    renderActiveFilters();
    render();
  };

  const loadIndex = async () => {
    const indexUrl = root.dataset.indexUrl || "/antenne-radio/index.json";
    status.textContent = "Chargement des signaux publics.";

    try {
      const response = await fetch(indexUrl, { headers: { Accept: "application/json" } });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      items = Array.isArray(data.items) ? data.items : [];
      hydrateControls(Array.isArray(data.sources) ? data.sources : []);
      syncFiltersFromURL();
      applyFilters();
    } catch (error) {
      grid.replaceChildren();
      grid.append(createEmptyState());
      status.textContent = "Chargement impossible.";
      loadMore.hidden = true;
    }
  };

  form.addEventListener("input", applyFilters);
  form.addEventListener("change", applyFilters);
  form.addEventListener("reset", () => window.setTimeout(applyFilters, 0));

  if (clearFiltersBtn) {
    clearFiltersBtn.addEventListener("click", () => {
      if (categorySelect) categorySelect.value = "";
      if (sourceSelect) sourceSelect.value = "";
      if (languageSelect) languageSelect.value = "";
      if (yearSelect) yearSelect.value = "";
      if (sortSelect) sortSelect.value = "date-desc";
      if (searchInput) searchInput.value = "";
      applyFilters();
      if (searchInput) searchInput.focus();
    });
  }

  loadMore.addEventListener("click", () => {
    visibleLimit += PAGE_SIZE;
    render();
  });

  loadIndex();
})();

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
  const searchInput = byId("antenne-radio-filter-search");
  const loadMore = byId("load-more");

  if (!grid || !form || !status || !loadMore) return;

  document.documentElement.classList.add("antenne-radio-js-enabled");

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
    .replace(/[\u0300-\u036f]/g, "")
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
  };

  const createCard = (item) => {
    const article = document.createElement("article");
    article.className = "antenne-radio-card";
    article.dataset.family = item.source_family || "";
    article.setAttribute("role", "listitem");

    const head = makeText("div", "antenne-radio-card-head", "");
    head.append(makeText("div", "antenne-radio-source-kicker", item.source_name || "source non déclarée"));

    const body = makeText("div", "antenne-radio-card-body", "");
    const title = makeText("h3", "antenne-radio-card-title", "");
    const titleLink = document.createElement("a");
    titleLink.href = safeUrl(item.url);
    titleLink.target = "_blank";
    titleLink.rel = "noopener noreferrer";
    titleLink.textContent = item.title || "Titre non déclaré";
    title.append(titleLink);

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

    body.append(title, meta, footer);
    article.append(head, body);
    return article;
  };

  const itemMatches = (item) => {
    const category = categorySelect ? categorySelect.value : "";
    const source = sourceSelect ? sourceSelect.value : "";
    const language = languageSelect ? languageSelect.value : "";
    const search = normalize(searchInput ? searchInput.value : "");
    const text = normalize([item.title, item.source_name, item.doi, item.source_type, item.language].join(" "));

    return (!category || item.source_type === category)
      && (!source || item.attribution_id === source)
      && (!language || item.language === language)
      && (!search || text.includes(search));
  };

  const render = () => {
    const visibleItems = filteredItems.slice(0, visibleLimit);
    const fragment = document.createDocumentFragment();

    grid.replaceChildren();
    visibleItems.forEach((item) => fragment.append(createCard(item)));

    if (fragment.childNodes.length) {
      grid.append(fragment);
    } else {
      grid.append(makeText("p", "antenne-radio-empty", "Aucun signal public ne correspond aux filtres."));
    }

    if (totalCounter) totalCounter.textContent = String(items.length);
    if (visibleCounter) visibleCounter.textContent = String(visibleItems.length);
    setStatus(visibleItems.length, filteredItems.length);

    loadMore.hidden = visibleLimit >= filteredItems.length;
  };

  const applyFilters = () => {
    visibleLimit = PAGE_SIZE;
    filteredItems = items.filter(itemMatches);
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
      applyFilters();
    } catch (error) {
      grid.replaceChildren();
      grid.append(makeText("p", "antenne-radio-empty", "L'index public n'a pas pu être chargé."));
      status.textContent = "Chargement impossible.";
      loadMore.hidden = true;
    }
  };

  form.addEventListener("input", applyFilters);
  form.addEventListener("change", applyFilters);
  form.addEventListener("reset", () => window.setTimeout(applyFilters, 0));
  loadMore.addEventListener("click", () => {
    visibleLimit += PAGE_SIZE;
    render();
  });

  loadIndex();
})();

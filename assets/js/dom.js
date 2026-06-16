/* DOM — bouton récalcitrant (P15).
   Reconversion minimale du DOM ENGINE d'origine : clic après clic (000→999), il
   débite une réplique de /data/dom-story.json, persiste le compteur, et s'éteint
   sur une pierre tombale au clic 999. Vanilla, sans dépendance. */
(function () {
  var KEY = 'pqc_dom_lifespan_v1'; // clé d'origine : préserve l'état des visiteurs
  var MAX = 999;

  var btn = document.getElementById('dom-button');
  if (!btn) return; // garde-fou : pas de DOM sur cette page

  var section = document.getElementById('dom');
  var counter = document.getElementById('dom-counter');
  var line = document.getElementById('dom-line');
  var story = null;

  var count = parseInt(localStorage.getItem(KEY), 10) || 0;

  // Réglage admin discret, sans mot de passe théâtral : ?dom=NNN dans l'URL.
  var forced = new URLSearchParams(location.search).get('dom');
  if (forced !== null) {
    count = Math.max(0, Math.min(MAX, parseInt(forced, 10) || 0));
    save();
  }

  function save() { localStorage.setItem(KEY, count); }
  function pad(n) { return String(n).padStart(3, '0'); }
  function renderCounter() { counter.textContent = pad(count) + ' / ' + MAX; }

  function showLine() {
    if (!story) return;
    var text = story[Math.min(count - 1, story.length - 1)] || '…';
    line.style.opacity = '0';
    line.textContent = text;
    line.hidden = false;
    requestAnimationFrame(function () { line.style.opacity = '1'; });
  }

  function tombstone() {
    section.innerHTML =
      '<p class="dom-epitaph">Ici repose DOM.<br>Il a bien cliqué.</p>' +
      '<p class="dom-end">Connection terminated.</p>';
  }

  renderCounter();
  if (count >= MAX) tombstone();

  fetch('/data/dom-story.json')
    .then(function (r) { return r.json(); })
    .then(function (data) {
      story = data;
      if (count > 0 && count < MAX) showLine(); // reprise : réplique courante
    })
    .catch(function () { story = null; }); // JSON absent : le bouton reste muet

  btn.addEventListener('click', function () {
    if (count >= MAX) return;
    count++;
    save();
    renderCounter();
    showLine();
    if (count >= MAX) tombstone();
  });
})();

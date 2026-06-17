/**
 * ALMANACH — version texte (P16)
 * Deux lignes sur l'accueil :
 *   1. la date pataphysique du jour + le saint (lib PataphysicalDate.js, offline) ;
 *   2. une entrée de la réserve tirée au hasard, en texte plein.
 * Rotation « deck » sans répétition conservée (localStorage), sans extrait,
 * sans modale, sans bouton « lire la suite ».
 * Dépendance : PataphysicalDate.js
 */

document.addEventListener('DOMContentLoaded', async () => {
    const STORAGE_KEY = 'pqch.almanach.deck.v2';
    const STORAGE_VERSION = 2;

    const lineEl = document.getElementById('almanach-line');
    const entryEl = document.getElementById('almanach-entry');

    // Rien à faire hors de l'accueil.
    if (!lineEl && !entryEl) return;

    // 1. Ligne pataphysique (date + saint).
    if (lineEl && typeof window.PataphysicalDate !== 'undefined') {
        try {
            const pata = new window.PataphysicalDate();
            const day = pata.getDay() === 1 ? '1er' : pata.getDay();
            const dayName = pata.getDayName().toLowerCase();
            const phrase = `Nous sommes le ${dayName} ${day} ${pata.getMonthName()} ${pata.getFullYear()} E.P., fête de ${pata.getSaintOfDay()}.`;
            lineEl.textContent = phrase;
            lineEl.hidden = false;
        } catch (err) {
            console.warn('Almanach : calcul pataphysique impossible.', err);
        }
    }

    // 2. Entrée aléatoire (réserve JSON).
    if (!entryEl) return;

    const shuffle = (values) => {
        const shuffled = [...values];
        for (let i = shuffled.length - 1; i > 0; i -= 1) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
    };

    const normalizeEntries = (data) => {
        if (Array.isArray(data.entries)) {
            return data.entries
                .map((entry, index) => ({
                    id: String(entry.id || entry.date || `entry-${index + 1}`),
                    title: entry.title ? String(entry.title) : '',
                    text: String(entry.text || entry.content || '')
                }))
                .filter((entry) => entry.id && entry.text)
                .filter((entry, index, entries) => (
                    entries.findIndex((candidate) => candidate.id === entry.id) === index
                ));
        }

        if (data.database && typeof data.database === 'object') {
            return Object.entries(data.database)
                .map(([date, text]) => ({ id: date, title: '', text: String(text || '') }))
                .filter((entry) => entry.id && entry.text)
                .filter((entry, index, entries) => (
                    entries.findIndex((candidate) => candidate.id === entry.id) === index
                ));
        }

        return [];
    };

    const getFingerprint = (ids) => ids.slice().sort().join('|');

    const createDeck = (ids, avoidFirstId = '') => {
        const deck = shuffle(ids);
        if (deck.length > 1 && deck[0] === avoidFirstId) {
            const swapIndex = deck.findIndex((id, index) => index > 0 && id !== avoidFirstId);
            if (swapIndex > 0) {
                [deck[0], deck[swapIndex]] = [deck[swapIndex], deck[0]];
            }
        }
        return deck;
    };

    const readReserveState = () => {
        try {
            const rawState = window.localStorage.getItem(STORAGE_KEY);
            if (!rawState) return null;
            const state = JSON.parse(rawState);
            if (
                !state ||
                state.version !== STORAGE_VERSION ||
                typeof state.fingerprint !== 'string' ||
                !Array.isArray(state.queue)
            ) {
                window.localStorage.removeItem(STORAGE_KEY);
                return null;
            }
            return state;
        } catch (_err) {
            try { window.localStorage.removeItem(STORAGE_KEY); } catch (_e) { /* indisponible */ }
            return null;
        }
    };

    const writeReserveState = (state) => {
        try {
            window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
        } catch (_err) {
            // Le site reste fonctionnel sans persistance locale.
        }
    };

    const pickEntry = (entries) => {
        if (!entries.length) return null;

        const byId = new Map(entries.map((entry) => [entry.id, entry]));
        const ids = entries.map((entry) => entry.id);
        const fingerprint = getFingerprint(ids);
        const fallback = () => entries[Math.floor(Math.random() * entries.length)];
        const state = readReserveState();

        let queue = [];
        let lastShownId = '';

        if (state && state.fingerprint === fingerprint) {
            queue = state.queue.filter((id) => byId.has(id));
            lastShownId = byId.has(state.lastShownId) ? state.lastShownId : '';
        } else if (state && byId.has(state.lastShownId)) {
            lastShownId = state.lastShownId;
        }

        if (!queue.length) {
            queue = createDeck(ids, lastShownId);
        }

        const nextId = queue.shift();
        writeReserveState({
            version: STORAGE_VERSION,
            fingerprint,
            queue,
            lastShownId: nextId
        });

        return byId.get(nextId) || fallback();
    };

    try {
        const response = await fetch('/almanach/index.json');
        if (!response.ok) throw new Error('API JSON inaccessible');

        const data = await response.json();
        const entry = pickEntry(normalizeEntries(data));
        if (!entry) return;

        const text = entry.title ? `${entry.title} — ${entry.text}` : entry.text;
        entryEl.textContent = `« ${text.replace(/\s+/g, ' ').trim()} »`;
        entryEl.hidden = false;
    } catch (err) {
        console.warn('Almanach : réserve inaccessible.', err);
    }
});

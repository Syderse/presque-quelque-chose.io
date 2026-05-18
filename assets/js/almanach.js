/**
 * ALMANACH UNIVERSAL CONTROLLER
 * Un seul script pour les gouverner tous (Widget & Page Complète).
 * Nécessite: PataphysicalDate.js
 */

document.addEventListener('DOMContentLoaded', async () => {
    const STORAGE_KEY = 'pqch.almanach.deck.v2';
    const STORAGE_VERSION = 2;
    const EXCERPT_LIMIT = 260;

    // 0. Dépendance
    if (typeof window.PataphysicalDate === 'undefined') {
        console.warn("🥞 PataphysicalDate.js introuvable.");
        return;
    }

    // 1. Mapping des Éléments DOM (IDs Standardisés)
    const els = {
        // Date Pata
        dayName: document.getElementById('pata-day-name'),
        dayNumber: document.getElementById('pata-day-number'),
        month: document.getElementById('pata-month'),
        year: document.getElementById('pata-year'),
        saint: document.getElementById('pata-saint'),
        saintMobile: document.getElementById('pata-saint-mobile'),
        
        // Méta & Contenu
        gregorian: document.getElementById('gregorian-ref'),
        content: document.getElementById('almanach-content'),
        readMore: document.getElementById('almanach-read-more'),
        dialog: document.getElementById('almanach-dialog'),
        dialogTitle: document.getElementById('almanach-dialog-title'),
        dialogBody: document.getElementById('almanach-dialog-body'),
        
        // Container (pour animation éventuelle)
        container: document.getElementById('almanach-container')
    };

    // Si aucun élément clé n'est présent, on arrête le script (économie de ressources)
    if (!els.dayNumber && !els.content) return;

    // 2. Calcul Pataphysique
    const now = new Date();
    const pata = new window.PataphysicalDate();
    
    // Mise à jour sécurisée du DOM (Date)
    const safeText = (el, text) => { if(el) el.textContent = text; };
    
    // Adaptation défensive au cas où l'API de la lib change
    try {
        safeText(els.dayName, pata.getDayName());
        safeText(els.dayNumber, pata.getDay());
        safeText(els.month, pata.getMonthName());
        safeText(els.year, `${pata.getFullYear()} E.P.`);
        safeText(els.saint, pata.getSaintOfDay());
        safeText(els.saintMobile, pata.getSaintOfDay());
        safeText(els.gregorian, now.toLocaleDateString('fr-FR'));
    } catch (e) {
        console.error("Erreur calcul Pata:", e);
    }

    // 3. Récupération du JSON (La "Blague" du jour)
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
                    date: entry.date ? String(entry.date) : '',
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
                .map(([date, text]) => ({
                    id: date,
                    date,
                    title: '',
                    text: String(text || '')
                }))
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
            try {
                window.localStorage.removeItem(STORAGE_KEY);
            } catch (_removeErr) {
                // localStorage peut être indisponible ou verrouillé.
            }
            return null;
        }
    };

    const writeReserveState = (state) => {
        try {
            window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
            return true;
        } catch (_err) {
            // Le site reste fonctionnel sans persistance locale.
            return false;
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
        const nextState = {
            version: STORAGE_VERSION,
            fingerprint,
            queue,
            lastShownId: nextId,
            updatedAt: new Date().toISOString()
        };

        writeReserveState(nextState);

        return byId.get(nextId) || fallback();
    };

    const makeExcerpt = (text) => {
        const normalized = text.replace(/\s+/g, ' ').trim();
        if (normalized.length <= EXCERPT_LIMIT) return normalized;

        const slice = normalized.slice(0, EXCERPT_LIMIT);
        const lastSpace = slice.lastIndexOf(' ');
        const cut = lastSpace > Math.floor(EXCERPT_LIMIT * 0.65)
            ? slice.slice(0, lastSpace)
            : slice;

        return `${cut.trim()}...`;
    };

    const renderEntry = (entry) => {
        const entryText = entry.title ? `${entry.title} — ${entry.text}` : entry.text;
        const excerpt = makeExcerpt(entryText);
        const hasMore = excerpt !== entryText;

        els.content.dataset.entryId = entry.id;
        els.content.dataset.entryTitle = entry.title || '';
        els.content.dataset.entryText = entry.text;
        els.content.dataset.entryFullText = entryText;
        els.content.dataset.hasMore = String(hasMore);
        els.content.textContent = `« ${excerpt} »`;
        els.content.classList.remove('italic'); // Style "actif"
        els.content.style.opacity = '1';

        if (els.readMore) {
            els.readMore.hidden = !hasMore;
        }
    };

    const getCurrentDialogEntry = () => {
        if (!els.content) return null;

        return {
            title: els.content.dataset.entryTitle || "Entrée d'almanach",
            text: els.content.dataset.entryText || els.content.dataset.entryFullText || ''
        };
    };

    const fillDialogBody = (text) => {
        if (!els.dialogBody) return;

        els.dialogBody.textContent = '';
        const paragraphs = text
            .split(/\n{2,}/)
            .map((part) => part.replace(/\s+/g, ' ').trim())
            .filter(Boolean);

        for (const paragraphText of paragraphs.length ? paragraphs : [text]) {
            const paragraph = document.createElement('p');
            paragraph.textContent = paragraphText;
            els.dialogBody.appendChild(paragraph);
        }
    };

    const openDialog = () => {
        if (!els.dialog || !els.dialogBody) return;
        if (els.dialog.open) return;

        const entry = getCurrentDialogEntry();
        if (!entry || !entry.text) return;

        safeText(els.dialogTitle, entry.title);
        fillDialogBody(entry.text);

        if (typeof els.dialog.showModal === 'function') {
            els.dialog.showModal();
        } else {
            els.dialog.setAttribute('open', '');
        }
    };

    if (els.readMore && els.content) {
        els.readMore.hidden = els.content.dataset.hasMore !== 'true';
        els.readMore.addEventListener('click', openDialog);
    }

    if (els.dialog) {
        els.dialog.addEventListener('click', (event) => {
            if (event.target === els.dialog && typeof els.dialog.close === 'function') {
                els.dialog.close();
            }
        });

        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape' && els.dialog.open && typeof els.dialog.close === 'function') {
                els.dialog.close();
            }
        });
    }

    try {
        const response = await fetch('/almanach/index.json');
        if (!response.ok) throw new Error('API JSON inaccessible');
        
        const data = await response.json();
        const entry = pickEntry(normalizeEntries(data));
        
        if (els.content) {
            if (entry) {
                // Animation de succès
                els.content.style.opacity = '0';
                setTimeout(() => {
                    renderEntry(entry);
                }, 150);
            } else {
                els.content.textContent = "La réserve d'almanach est vide pour le moment.";
            }
        }
    } catch (err) {
        console.warn("Almanach Data Error:", err);
        if(els.content) els.content.textContent = "Communication avec l'Éther interrompue.";
    }
});

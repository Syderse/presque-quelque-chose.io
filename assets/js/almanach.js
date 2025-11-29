/**
 * ALMANACH UNIVERSAL CONTROLLER
 * Un seul script pour les gouverner tous (Widget & Page Complète).
 * Nécessite: PataphysicalDate.js
 */

document.addEventListener('DOMContentLoaded', async () => {
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
        
        // Méta & Contenu
        gregorian: document.getElementById('gregorian-ref'),
        content: document.getElementById('almanach-content'),
        
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
        safeText(els.gregorian, now.toLocaleDateString('fr-FR'));
    } catch (e) {
        console.error("Erreur calcul Pata:", e);
    }

    // 3. Récupération du JSON (La "Blague" du jour)
    const todayKey = now.toISOString().split('T')[0]; // YYYY-MM-DD

    try {
        const response = await fetch('/almanach/index.json');
        if (!response.ok) throw new Error('API JSON inaccessible');
        
        const data = await response.json();
        const entry = data.database[todayKey];
        
        if (els.content) {
            if (entry) {
                // Animation de succès
                els.content.style.opacity = '0';
                setTimeout(() => {
                    els.content.textContent = `« ${entry} »`;
                    els.content.classList.remove('italic'); // Style "actif"
                    els.content.style.opacity = '1';
                }, 150);
            } else {
                els.content.textContent = "Le néant règne aujourd'hui sur les archives.";
            }
        }
    } catch (err) {
        console.warn("Almanach Data Error:", err);
        if(els.content) els.content.textContent = "Communication avec l'Éther interrompue.";
    }
});
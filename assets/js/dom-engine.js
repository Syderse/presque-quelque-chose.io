/**
 * DOM ENGINE V4.3 - "SELF-MOUNTING PORTAL"
 * Update: Auto-injection of the narrative layer into Body.
 * No changes to baseof.html required.
 */

(function () {
    // --- CONFIGURATION ---
    const CONFIG = {
        dataUrl: '/data/dom-story.json',
        storageKey: 'pqc_dom_lifespan_v1',
        maxClicks: 999,
        acts: {
            ACT_1: 0,   // Naissance
            ACT_2: 200, // Adolescence
            ACT_3: 500, // Âge Adulte
            ACT_4: 800, // Vieillesse
            ACT_5: 950  // Agonie
        },
        admin: {
            password: 'bosse-de-nage'
        }
    };

    // --- DOM CACHE (PARTIAL) ---
    // Note: narrative is handled dynamically in init()
    const ui = {
        container: document.getElementById('dom-container'),
        chassis: document.getElementById('dom-chassis'),
        wrapper: document.getElementById('dom-wrapper'),
        btn: document.getElementById('btn-dom'),
        icon: document.getElementById('dom-icon'),
        ghost: document.getElementById('dom-icon-ghost'),
        label: document.getElementById('dom-label'),
        counter: document.getElementById('dom-counter-display'),
        console: document.getElementById('console-output'),
        tombstone: document.getElementById('dom-tombstone'),
        integrityBar: document.getElementById('integrity-bar'),
        ripple: document.getElementById('click-ripple'),
        // Admin Refs
        adminModal: document.getElementById('admin-modal'),
        adminLogin: document.getElementById('admin-login-view'),
        adminDashboard: document.getElementById('admin-dashboard-view'),
        adminInput: document.getElementById('admin-pwd-input'),
        adminError: document.getElementById('admin-error-msg'),
        adminSetCount: document.getElementById('admin-set-count'),
        adminSave: document.getElementById('admin-btn-save'),
        adminReset: document.getElementById('admin-btn-reset'),
        adminClose: document.getElementById('admin-close-btn'),
        virusLayer: document.getElementById('virus-layer'),
        // Dynamic placeholder
        narrative: null 
    };

    if (!ui.btn) return; // Exit if widget is not present

    // --- STATE ---
    let state = {
        count: parseInt(localStorage.getItem(CONFIG.storageKey) || '0'),
        story: [],
        isLoaded: false,
        act: 1,
        adminOpen: false
    };

    // --- INITIALIZATION ---
    async function init() {
        // 1. Mount the Narrative Layer (The Portal)
        mountNarrativeLayer();

        renderIntegrityBar();

        // Si déjà mort
        if (state.count >= CONFIG.maxClicks) {
            triggerEndgame(true);
        } else {
            updateScene(state.count);
        }

        // Core Listeners
        ui.btn.addEventListener('click', handleClick);

        // Admin Listeners
        ui.counter.addEventListener('contextmenu', handleRightClick);
        ui.tombstone.addEventListener('contextmenu', handleRightClick);

        ui.adminInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') checkPassword(ui.adminInput.value);
        });
        ui.adminClose.addEventListener('click', closeAdmin);
        ui.adminSave.addEventListener('click', updateFromAdmin);
        ui.adminReset.addEventListener('click', factoryReset);

        // Silent Data Load
        try {
            const req = await fetch(CONFIG.dataUrl);
            state.story = await req.json();
            state.isLoaded = true;
            console.log(`[DOM] Memory loaded: ${state.story.length} fragments.`);
        } catch (e) {
            console.error('[DOM] Memory corruption:', e);
            state.story = ["Erreur 404.", "Je suis vide."];
            state.isLoaded = true;
        }
    }

    // --- ARCHITECTURE: PORTAL MOUNTING ---
    function mountNarrativeLayer() {
        const ID = 'dom-narrative-zone-global';
        let layer = document.getElementById(ID);

        if (!layer) {
            layer = document.createElement('div');
            layer.id = ID;
            // Tailwind-like styling via JS to ensure isolation
            layer.style.position = 'fixed';
            layer.style.top = '0';
            layer.style.left = '0';
            layer.style.width = '100vw';
            layer.style.height = '100vh';
            layer.style.pointerEvents = 'none'; // Click-through
            layer.style.zIndex = '9999'; // Always on top
            layer.style.overflow = 'hidden';
            
            document.body.appendChild(layer);
            console.log("[DOM] Narrative Layer injected into Body.");
        }
        
        ui.narrative = layer;
    }

    // --- CORE LOGIC ---
    function handleClick() {
        if (state.count >= CONFIG.maxClicks) return;

        state.count++;
        saveState();

        triggerRipple();
        updateScene(state.count);

        if (state.isLoaded) {
            const text = getStoryLine(state.count);
            spawnMessage(text);
            logConsole(`EVENT_CLICK [ID:${state.count}]`);
        }

        if (state.count >= CONFIG.maxClicks) {
            setTimeout(() => triggerEndgame(false), 1500);
        }
    }

    function saveState() {
        localStorage.setItem(CONFIG.storageKey, state.count);
    }

    // --- VISUAL ENGINE (ENTROPY) ---
    function updateScene(n) {
        ui.counter.innerText = `${n.toString().padStart(3, '0')} / ${CONFIG.maxClicks}`;

        const lifeRatio = 1 - (n / CONFIG.maxClicks);
        updateIntegrityBar(lifeRatio);

        // Determine Act
        let currentAct = 1;
        if (n > CONFIG.acts.ACT_5) currentAct = 5;
        else if (n > CONFIG.acts.ACT_4) currentAct = 4;
        else if (n > CONFIG.acts.ACT_3) currentAct = 3;
        else if (n > CONFIG.acts.ACT_2) currentAct = 2;
        state.act = currentAct;

        applyEntropy(n, lifeRatio, currentAct);
        updateLabel(currentAct);
    }

    function applyEntropy(n, life, act) {
        ui.wrapper.style.filter = 'none';
        ui.wrapper.style.transform = 'rotate(0deg)';
        ui.label.classList.remove('glitch-active');
        ui.ghost.style.opacity = 0;

        if (act >= 3) {
            const desat = (n - CONFIG.acts.ACT_3) / 300;
            ui.wrapper.style.filter = `grayscale(${desat * 0.5})`;
        }

        if (act >= 4) {
            const intensity = (n - CONFIG.acts.ACT_4) / 200;
            ui.wrapper.style.filter = `grayscale(${0.5 + intensity * 0.5}) blur(${intensity * 2}px)`;

            const rot = (Math.random() - 0.5) * intensity * 10;
            ui.wrapper.style.transform = `rotate(${rot}deg)`;

            ui.wrapper.style.opacity = 0.5 + (life * 0.5);

            ui.ghost.style.opacity = intensity * 0.8;
            ui.ghost.style.transform = `translate(${intensity * 5}px, ${intensity * -2}px)`;
        }

        if (act === 5) {
            ui.wrapper.style.filter = `grayscale(1) contrast(1.5) blur(1px)`;
            ui.label.classList.add('glitch-active');
            ui.wrapper.style.opacity = Math.max(0.1, life * 2);
        }
    }

    function updateLabel(act) {
        const labels = { 1: "init", 2: "run", 3: "wait", 4: "fail", 5: "..." };
        ui.label.innerText = labels[act] || "ERROR";
        ui.label.style.letterSpacing = `${0.2 + (state.count / 1000) * 0.5}em`;
    }

// --- SCATTERING ENGINE (V4.5: CENTER-OFFSET CORRECTION) ---
    function spawnMessage(text) {
        if (!ui.narrative) return;

        const bubble = document.createElement('div');

        // Styles conditionnels
        let bgClass = "bg-ctp-surface0/90 text-ctp-text border-ctp-surface2";
        if (state.act >= 4) bgClass = "bg-ctp-crust/95 text-ctp-red border-ctp-red border-dashed";

        bubble.className = `msg-bubble-v4 fixed whitespace-nowrap px-4 py-2 rounded-lg border shadow-xl backdrop-blur-md text-xs font-mono ${bgClass}`;
        bubble.innerText = text;

        // --- POSITION RELATIVE AU BOUTON (VIEWPORT COORDS) ---
        const btnRect = ui.btn.getBoundingClientRect();
        // On part du centre du bouton
        const btnCenterX = btnRect.left + btnRect.width / 2;
        const btnCenterY = btnRect.top + btnRect.height / 2;

        // --- DIRECTIONAL MATH ---
        const minRadius = 100;  
        const maxRadius = 450; // On augmente la portée pour compenser le décalage

        // Cône de visée vers la droite (Est)
        // On resserre un peu l'angle vertical pour éviter que ça parte trop bas/haut hors écran
        const minAngle = -Math.PI / 5; // ~ -36 deg
        const maxAngle = Math.PI / 2;  // ~ +90 deg
        
        const angle = minAngle + Math.random() * (maxAngle - minAngle);
        const distance = minRadius + Math.random() * (maxRadius - minRadius);

        const offsetX = Math.cos(angle) * distance;
        const offsetY = Math.sin(angle) * distance;

        let finalX = btnCenterX + offsetX;
        let finalY = btnCenterY + offsetY;

        // --- SAFETY CLAMP
        
        // 1. COMPENSATION DE CENTRAGE :
        // L'animation CSS fait un translate(-50%, -50%). 
        // Donc finalX est le CENTRE de la bulle.
        // Si la bulle fait 300px de large, il faut que finalX soit à 150px du bord du bouton.
        const estimatedHalfWidth = 140; // Marge de sécurité pour texte long
        
        // Le "Mur Invisible" à gauche est maintenant décalé de cette demi-largeur
        const safeLeft = btnRect.right + estimatedHalfWidth; 
        
        // 2. COMPENSATION BORD DROIT ÉCRAN :
        // Idem, on ne veut pas que la moitié droite sorte de l'écran
        const safeRight = window.innerWidth - estimatedHalfWidth - 20;

        // Application des contraintes
        finalX = Math.max(safeLeft, Math.min(safeRight, finalX));
        
        // Contraintes Verticales (Marge simple)
        const marginY = 40;
        finalY = Math.max(marginY, Math.min(window.innerHeight - marginY, finalY));

        bubble.style.left = `${finalX}px`;
        bubble.style.top = `${finalY}px`;
        bubble.style.zIndex = '10000'; 

        ui.narrative.appendChild(bubble);

        setTimeout(() => {
            if (bubble.parentNode) bubble.parentNode.removeChild(bubble);
        }, 5000); 
    }

    // --- BOSSE-DE-NAGE (ADMIN MODULE) ---
    function handleRightClick(e) {
        e.preventDefault();
        state.adminOpen = true;
        ui.adminModal.classList.remove('hidden');
        ui.adminModal.classList.add('flex');

        // Reset View
        ui.adminLogin.classList.remove('hidden');
        ui.adminDashboard.classList.add('hidden');
        ui.adminError.classList.add('hidden');
        ui.adminInput.value = '';
        ui.adminInput.focus();
    }

    function checkPassword(pwd) {
        if (pwd === CONFIG.admin.password) {
            ui.adminLogin.classList.add('hidden');
            ui.adminDashboard.classList.remove('hidden');
            ui.adminDashboard.classList.add('flex');
            ui.adminSetCount.value = state.count;
            logConsole("ADMIN ACCESS GRANTED");
        } else {
            ui.adminError.classList.remove('hidden');
            triggerHahaFlood();
            logConsole("SECURITY BREACH DETECTED");
        }
    }

    function triggerHahaFlood() {
        ui.virusLayer.classList.remove('hidden');
        const phrases = ["HA HA", "NO", "DENIED", "👀", "🚫"];
        let count = 0;

        const interval = setInterval(() => {
            if (count > 50) {
                clearInterval(interval);
                ui.virusLayer.innerHTML = '';
                ui.virusLayer.classList.add('hidden');
                closeAdmin();
                return;
            }

            const span = document.createElement('span');
            span.innerText = phrases[Math.floor(Math.random() * phrases.length)];
            span.className = "absolute text-ctp-red font-bold font-mono animate-ping";
            span.style.left = `${Math.random() * 100}%`;
            span.style.top = `${Math.random() * 100}%`;
            span.style.fontSize = `${10 + Math.random() * 40}px`;

            ui.virusLayer.appendChild(span);
            count++;
        }, 50);
    }

    function updateFromAdmin() {
        let newCount = parseInt(ui.adminSetCount.value);
        if (isNaN(newCount)) return;
        newCount = Math.max(0, Math.min(newCount, CONFIG.maxClicks));
        state.count = newCount;
        saveState();
        updateScene(state.count);

        if (state.count < CONFIG.maxClicks) {
            ui.tombstone.classList.add('hidden');
            ui.tombstone.classList.remove('flex');
            ui.wrapper.style.display = 'block';
        } else {
            triggerEndgame(true);
        }

        closeAdmin();
        logConsole(`ADMIN OVERRIDE: COUNT SET TO ${newCount}`);
    }

    function factoryReset() {
        state.count = 0;
        localStorage.removeItem(CONFIG.storageKey);
        location.reload();
    }

    function closeAdmin() {
        ui.adminModal.classList.add('hidden');
        ui.adminModal.classList.remove('flex');
        state.adminOpen = false;
    }

    // --- UTILS ---
    function renderIntegrityBar() {
        ui.integrityBar.innerHTML = '';
        for (let i = 0; i < 10; i++) {
            const dash = document.createElement('div');
            dash.className = "w-1 h-2 bg-ctp-green rounded-[1px] transition-colors duration-500";
            ui.integrityBar.appendChild(dash);
        }
    }

    function updateIntegrityBar(ratio) {
        const dashes = ui.integrityBar.children;
        const activeCount = Math.ceil(ratio * 10);
        for (let i = 0; i < 10; i++) {
            dashes[i].className = i < activeCount
                ? (ratio > 0.6 ? "w-1 h-2 bg-ctp-green rounded-[1px]" : (ratio > 0.3 ? "w-1 h-2 bg-ctp-yellow rounded-[1px]" : "w-1 h-2 bg-ctp-red rounded-[1px] animate-pulse"))
                : "w-1 h-2 bg-ctp-surface0 rounded-[1px]";
        }
    }

    function logConsole(msg) {
        const line = document.createElement('div');
        line.innerText = `> ${msg}`;
        ui.console.prepend(line);
        if (ui.console.children.length > 5) ui.console.removeChild(ui.console.lastChild);
    }

    function getStoryLine(n) {
        const index = Math.min(n - 1, state.story.length - 1);
        return state.story[index] || "...";
    }

    function triggerRipple() {
        ui.ripple.classList.remove('scale-0', 'opacity-0');
        ui.ripple.style.transition = 'none';
        ui.ripple.style.transform = 'scale(0)';
        ui.ripple.style.opacity = '1';
        void ui.ripple.offsetWidth;
        ui.ripple.style.transition = 'transform 0.4s ease-out, opacity 0.4s ease-out';
        ui.ripple.style.transform = 'scale(1.5)';
        ui.ripple.style.opacity = '0';
    }

    function triggerEndgame(instant) {
        ui.wrapper.style.display = 'none';
        ui.tombstone.classList.remove('hidden');
        ui.tombstone.classList.add('flex');
        if (!instant) logConsole("SYSTEM HALTED.");
    }

    // START
    init();

})();
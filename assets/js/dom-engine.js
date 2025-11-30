/**
 * DOM ENGINE V5.0 - "SOLID STATE"
 * Optimized for 60FPS. Removed all backdrop-filters and heavy blur calculations.
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

    // --- DOM CACHE ---
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
        mountNarrativeLayer();
        renderIntegrityBar();

        if (state.count >= CONFIG.maxClicks) {
            triggerEndgame(true);
        } else {
            updateScene(state.count);
        }

        // Listeners
        ui.btn.addEventListener('click', handleClick);
        ui.counter.addEventListener('contextmenu', handleRightClick);
        ui.tombstone.addEventListener('contextmenu', handleRightClick);

        ui.adminInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') checkPassword(ui.adminInput.value);
        });
        ui.adminClose.addEventListener('click', closeAdmin);
        ui.adminSave.addEventListener('click', updateFromAdmin);
        ui.adminReset.addEventListener('click', factoryReset);

        // Load Data
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

    // --- PORTAL MOUNTING (GLOBAL) ---
    function mountNarrativeLayer() {
        const ID = 'dom-narrative-zone-global';
        let layer = document.getElementById(ID);

        if (!layer) {
            layer = document.createElement('div');
            layer.id = ID;
            layer.style.position = 'fixed';
            layer.style.top = '0';
            layer.style.left = '0';
            layer.style.width = '100vw';
            layer.style.height = '100vh';
            layer.style.pointerEvents = 'none';
            layer.style.zIndex = '9999';
            layer.style.overflow = 'hidden';
            
            document.body.appendChild(layer);
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

    // --- VISUAL ENGINE (OPTIMIZED ENTROPY) ---
    // No blur calculation here to save FPS
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
        // Reset cheap props
        ui.wrapper.style.filter = 'none';
        ui.wrapper.style.transform = 'rotate(0deg)';
        ui.label.classList.remove('glitch-active');
        ui.ghost.style.opacity = 0;

        // Grayscale is hardware accelerated and cheap
        if (act >= 3) {
            const desat = (n - CONFIG.acts.ACT_3) / 300;
            ui.wrapper.style.filter = `grayscale(${desat * 0.8})`;
        }

        if (act >= 4) {
            const intensity = (n - CONFIG.acts.ACT_4) / 200;
            // Removed BLUR. Kept Grayscale. Added slight rotation.
            ui.wrapper.style.filter = `grayscale(${0.8 + intensity * 0.2})`;

            const rot = (Math.random() - 0.5) * intensity * 5; // Reduced rotation
            ui.wrapper.style.transform = `rotate(${rot}deg)`;
            
            ui.ghost.style.opacity = intensity * 1; // Solid ghost appears
            // Translate is cheap
            ui.ghost.style.transform = `translate(${intensity * 4}px, ${intensity * -2}px)`;
        }

        if (act === 5) {
            ui.wrapper.style.filter = `grayscale(1) contrast(1.2)`;
            ui.label.classList.add('glitch-active');
            ui.wrapper.style.opacity = Math.max(0.2, life * 3);
        }
    }

    function updateLabel(act) {
        const labels = { 1: "init", 2: "run", 3: "wait", 4: "fail", 5: "..." };
        ui.label.innerText = labels[act] || "ERROR";
        ui.label.style.letterSpacing = `${0.2 + (state.count / 1000) * 0.2}em`;
    }

// --- SCATTERING ENGINE (SOLID BUBBLES) ---
function spawnMessage(text) {
    if (!ui.narrative) return;

    const bubble = document.createElement('div');

    // We use a prominent border color and a solid background to achieve a "pop" without transparency.
    let baseClass = "msg-bubble-solid fixed whitespace-nowrap px-3 py-1 rounded shadow-lg border-2 text-xs font-mono font-bold";
    let colorClass = ""; // High-contrast style based on Act

    switch (state.act) {
        case 1:
            // INIT/Normal: High visibility, reassuring blue/surface contrast.
            colorClass = "bg-ctp-surface0 text-ctp-blue border-ctp-blue";
            break;
        case 2:
            // RUN: Energetic, but not critical (Mauve/Peach).
            colorClass = "bg-ctp-surface0 text-ctp-mauve border-ctp-peach";
            break;
        case 3:
            // WAIT/Warning: Yellow for caution.
            colorClass = "bg-ctp-surface0 text-ctp-yellow border-ctp-yellow";
            break;
        case 4:
            // FAIL/Entropy: Red for critical state, dashed border for instability.
            colorClass = "bg-ctp-crust text-ctp-red border-ctp-red border-dashed";
            break;
        case 5:
            // ENDGAME: Deep red and pulsing.
            colorClass = "bg-ctp-crust text-ctp-red border-ctp-red animate-pulse";
            break;
        default:
            colorClass = "bg-ctp-surface0 text-ctp-text border-ctp-surface1";
            break;
    }

    bubble.className = `${baseClass} ${colorClass}`;
    bubble.innerText = text;

    // Positioning (Centered on button + offset)
    const btnRect = ui.btn.getBoundingClientRect();
    const btnCenterX = btnRect.left + btnRect.width / 2;
    const btnCenterY = btnRect.top + btnRect.height / 2;

    const minRadius = 100;
    const maxRadius = 400;

    const minAngle = -Math.PI / 5;
    const maxAngle = Math.PI / 2;

    const angle = minAngle + Math.random() * (maxAngle - minAngle);
    const distance = minRadius + Math.random() * (maxRadius - minRadius);

    const offsetX = Math.cos(angle) * distance;
    const offsetY = Math.sin(angle) * distance;

    let finalX = btnCenterX + offsetX;
    let finalY = btnCenterY + offsetY;

    // Safety Clamps
    const estimatedHalfWidth = 140;
    const safeLeft = btnRect.right + estimatedHalfWidth;
    const safeRight = window.innerWidth - estimatedHalfWidth - 20;

    finalX = Math.max(safeLeft, Math.min(safeRight, finalX));
    const marginY = 40;
    finalY = Math.max(marginY, Math.min(window.innerHeight - marginY, finalY));

    bubble.style.left = `${finalX}px`;
    bubble.style.top = `${finalY}px`;

    ui.narrative.appendChild(bubble);

    setTimeout(() => {
        if (bubble.parentNode) bubble.parentNode.removeChild(bubble);
    }, 4000);
}

    // --- BOSSE-DE-NAGE (ADMIN) ---
    function handleRightClick(e) {
        e.preventDefault();
        state.adminOpen = true;
        ui.adminModal.classList.remove('hidden');
        ui.adminModal.classList.add('flex');

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
            if (count > 30) { // Reduced count for performance
                clearInterval(interval);
                ui.virusLayer.innerHTML = '';
                ui.virusLayer.classList.add('hidden');
                closeAdmin();
                return;
            }

            const span = document.createElement('span');
            span.innerText = phrases[Math.floor(Math.random() * phrases.length)];
            span.className = "absolute text-ctp-red font-bold font-mono animate-ping";
            span.style.left = `${Math.random() * 90}%`;
            span.style.top = `${Math.random() * 90}%`;
            span.style.fontSize = `${10 + Math.random() * 40}px`;

            ui.virusLayer.appendChild(span);
            count++;
        }, 80);
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
        logConsole(`ADMIN OVERRIDE: ${newCount}`);
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
            dash.className = "w-1 h-2 bg-ctp-green rounded-[1px]";
            ui.integrityBar.appendChild(dash);
        }
    }

    function updateIntegrityBar(ratio) {
        const dashes = ui.integrityBar.children;
        const activeCount = Math.ceil(ratio * 10);
        for (let i = 0; i < 10; i++) {
            dash = dashes[i];
            if (i < activeCount) {
                if (ratio > 0.6) dash.className = "w-1 h-2 bg-ctp-green rounded-[1px]";
                else if (ratio > 0.3) dash.className = "w-1 h-2 bg-ctp-yellow rounded-[1px]";
                else dash.className = "w-1 h-2 bg-ctp-red rounded-[1px] animate-pulse";
            } else {
                dash.className = "w-1 h-2 bg-ctp-surface0 rounded-[1px]";
            }
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
        // Updated for Solid State Ripple (Border scale)
        ui.ripple.classList.remove('scale-0', 'opacity-0');
        ui.ripple.style.transition = 'none';
        ui.ripple.style.transform = 'scale(0.8)';
        ui.ripple.style.opacity = '1';
        
        // Force Reflow
        void ui.ripple.offsetWidth;
        
        // Animate
        ui.ripple.style.transition = 'transform 0.3s ease-out, opacity 0.3s ease-out';
        ui.ripple.style.transform = 'scale(1.4)';
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
/**
 * SIDENOTE PHYSICS ENGINE V2.1 (LG-Sync)
 * Purpose: Manages collision detection for alternating marginalia.
 * Stack A: Left Gutter (Odd)
 * Stack B: Right Gutter (Even)
 * Note: Syncs with CSS 'lg' breakpoint (1024px).
 */

const SidenoteManager = {
    settings: {
        noteSelector: '.side-note-content', 
        containerSelector: 'article', 
        gap: 32, 
        minWidth: 1024 // UPDATED: Matches Tailwind 'lg' breakpoint
    },

    init() {
        this.adjust();

        // Performance: Debounced Resize
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                requestAnimationFrame(() => this.adjust());
            }, 100);
        });
        
        // Reliability: Load & Post-Load Checks
        window.addEventListener('load', () => this.adjust());
        setTimeout(() => this.adjust(), 500); 
        setTimeout(() => this.adjust(), 2000); // Catch late webfonts
    },

    adjust() {
        const isDesktop = window.innerWidth >= this.settings.minWidth;
        const notes = document.querySelectorAll(this.settings.noteSelector);
        const container = document.querySelector(this.settings.containerSelector);

        // A. Reset Phase
        // Always reset margins first to get the "Natural" top position (top: auto)
        this.reset(notes, container);

        if (!isDesktop || notes.length === 0) {
            return;
        }

        // B. Physics Phase
        let lastBottomLeft = 0;
        let lastBottomRight = 0;
        const scrollY = window.scrollY || document.documentElement.scrollTop;

        notes.forEach((note) => {
            // 1. Identify Side
            const isLeft = note.classList.contains('sn-left');
            
            // 2. Measure Geometry (This gets the position set by CSS top:auto)
            const rect = note.getBoundingClientRect();
            const absoluteTop = rect.top + scrollY;
            const height = rect.height;

            // 3. Determine Collision Target
            // If Left, check Left Stack. If Right, check Right Stack.
            let lastBottom = isLeft ? lastBottomLeft : lastBottomRight;
            
            // 4. Apply Force
            if (absoluteTop < lastBottom + this.settings.gap) {
                const push = (lastBottom + this.settings.gap) - absoluteTop;
                note.style.marginTop = `${push}px`;
                
                // Update specific stack
                const newBottom = absoluteTop + push + height;
                if (isLeft) lastBottomLeft = newBottom;
                else lastBottomRight = newBottom;
            } else {
                // No collision, register natural bottom
                const newBottom = absoluteTop + height;
                if (isLeft) lastBottomLeft = newBottom;
                else lastBottomRight = newBottom;
            }
        });

        // C. Container Extension Phase
        // Ensure article is long enough for the longest stack
        const lowestPoint = Math.max(lastBottomLeft, lastBottomRight);

        if (container && lowestPoint > 0) {
            const containerRect = container.getBoundingClientRect();
            const containerBottom = containerRect.bottom + scrollY;

            if (lowestPoint > containerBottom) {
                const diff = lowestPoint - containerBottom;
                // Add generous padding to footer
                container.style.paddingBottom = `${diff + 60}px`; 
            }
        }
    },

    reset(notes, container) {
        if (notes) notes.forEach(n => n.style.marginTop = '');
        if (container) container.style.paddingBottom = '';
    }
};

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => SidenoteManager.init());
} else {
    SidenoteManager.init();
}
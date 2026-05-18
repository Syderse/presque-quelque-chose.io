/**
 * SIDENOTE PHYSICS ENGINE V3.0 (Stable Anchor)
 * Purpose: Manages collision detection for alternating marginalia.
 * 
 * CRITICAL FIX: Uses offsetTop relative to the article container
 * for scroll-independent positioning. No more "falling notes" bug.
 * 
 * Stack A: Left Gutter (Odd notes)
 * Stack B: Right Gutter (Even notes)
 */

const SidenoteManager = {
    settings: {
        noteSelector: '.side-note-content',
        markerSelector: '.side-note-marker',
        triggerSelector: '.group\\/note', // The inline wrapper span
        labelSelector: '.side-note-trigger',
        containerSelector: 'article',
        gap: 24,
        minWidth: 1024 // Tailwind 'lg' breakpoint
    },

    init() {
        this.normalizeInlineSpacing();
        this.bindInteractions();

        // Initial adjustment after DOM is ready
        this.adjust();

        // Debounced resize handler
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                requestAnimationFrame(() => this.adjust());
            }, 100);
        });

        // Additional safety checks for late-loading content
        window.addEventListener('load', () => {
            this.normalizeInlineSpacing();
            this.adjust();
        });
        setTimeout(() => this.adjust(), 500);
        setTimeout(() => this.adjust(), 1500); // Catch late webfonts
    },

    normalizeInlineSpacing() {
        const markers = document.querySelectorAll(this.settings.markerSelector);
        const compactFollowers = '.,;:!?)]}»”’…';

        markers.forEach((marker) => {
            if (marker.dataset.spacingNormalized === 'true') return;

            const previous = this.getPreviousVisibleSibling(marker);
            if (previous?.nodeType === Node.TEXT_NODE) {
                previous.nodeValue = previous.nodeValue.replace(/\s+$/, '');
            }

            const next = this.getNextVisibleSibling(marker);
            const nextCharacter = this.getFirstVisibleCharacter(next);

            if (
                nextCharacter &&
                !/\s/.test(nextCharacter) &&
                !compactFollowers.includes(nextCharacter)
            ) {
                marker.after(document.createTextNode(' '));
            }

            marker.dataset.spacingNormalized = 'true';
        });
    },

    bindInteractions() {
        const markers = document.querySelectorAll(this.settings.markerSelector);

        markers.forEach((marker) => {
            if (marker.dataset.sidenoteBound === 'true') return;

            const checkbox = marker.querySelector('input[type="checkbox"]');
            const label = marker.querySelector(this.settings.labelSelector);
            const note = marker.querySelector(this.settings.noteSelector);

            if (!checkbox || !label || !note) return;

            const setExpanded = () => {
                const isActive = checkbox.checked;
                const activeColor = label.classList.contains('side-note-trigger--comment')
                    ? 'var(--ctp-teal)'
                    : 'var(--ctp-red)';

                label.setAttribute('aria-expanded', String(isActive));
                label.classList.toggle('side-note-trigger--active', isActive);
                marker.classList.toggle('is-sidenote-active', isActive);

                if (isActive) {
                    label.style.setProperty('color', activeColor, 'important');
                } else {
                    label.style.removeProperty('color');
                }
            };

            const toggleNote = () => {
                checkbox.checked = !checkbox.checked;
                checkbox.dispatchEvent(new Event('change', { bubbles: true }));
            };

            label.addEventListener('keydown', (event) => {
                if (event.key !== 'Enter' && event.key !== ' ') return;

                event.preventDefault();
                checkbox.checked = !checkbox.checked;
                checkbox.dispatchEvent(new Event('change', { bubbles: true }));
            });

            checkbox.addEventListener('change', setExpanded);
            note.addEventListener('click', toggleNote);

            setExpanded();
            marker.dataset.sidenoteBound = 'true';
        });
    },

    getPreviousVisibleSibling(node) {
        let current = node.previousSibling;

        while (current && current.nodeType === Node.COMMENT_NODE) {
            current = current.previousSibling;
        }

        return current;
    },

    getNextVisibleSibling(node) {
        let current = node.nextSibling;

        while (current) {
            if (current.nodeType === Node.COMMENT_NODE) {
                current = current.nextSibling;
                continue;
            }

            if (current.nodeType === Node.TEXT_NODE || current.textContent.trim() !== '') {
                return current;
            }

            current = current.nextSibling;
        }

        return null;
    },

    getFirstVisibleCharacter(node) {
        if (!node) return '';

        if (node.nodeType === Node.TEXT_NODE) {
            return node.nodeValue.charAt(0);
        }

        return node.textContent.charAt(0);
    },

    /**
     * Gets the offset from an element to a specific ancestor.
     * This is scroll-independent and stable.
     */
    getOffsetToAncestor(element, ancestor) {
        let offset = 0;
        let current = element;

        while (current && current !== ancestor && current !== document.body) {
            offset += current.offsetTop;
            current = current.offsetParent;
        }

        return offset;
    },

    adjust() {
        const isDesktop = window.innerWidth >= this.settings.minWidth;
        const container = document.querySelector(this.settings.containerSelector);
        const notes = document.querySelectorAll(this.settings.noteSelector);

        // Reset phase - always reset first
        this.reset(notes, container);

        if (!isDesktop || !container || notes.length === 0) {
            return;
        }

        // Get container's position for reference
        const containerRect = container.getBoundingClientRect();
        const containerTop = container.offsetTop;

        // Track the bottom of the last note in each stack
        let lastBottomLeft = 0;
        let lastBottomRight = 0;

        notes.forEach((note) => {
            // 1. Identify which side this note belongs to
            const isLeft = note.classList.contains('sn-left');

            // 2. Find the trigger (parent span) to get anchor position
            const trigger = note.closest(this.settings.triggerSelector);
            if (!trigger) return;

            // 3. Get a stable, scroll-independent position
            // This is the key fix: offsetTop doesn't change with scroll
            const anchorTop = this.getOffsetToAncestor(trigger, container);

            // 4. Get note height (use getBoundingClientRect for accurate measurement)
            const noteRect = note.getBoundingClientRect();
            const noteHeight = noteRect.height;

            // 5. Determine collision target for this stack
            const lastBottom = isLeft ? lastBottomLeft : lastBottomRight;

            // 6. Calculate the desired top position
            let targetTop = anchorTop;

            // 7. Apply collision avoidance if needed
            if (targetTop < lastBottom + this.settings.gap) {
                targetTop = lastBottom + this.settings.gap;
            }

            // 8. Apply the position using CSS top (not marginTop)
            // This is more reliable as it sets an explicit position
            note.style.top = `${targetTop}px`;

            // 9. Update the stack's last bottom position
            const newBottom = targetTop + noteHeight;
            if (isLeft) {
                lastBottomLeft = newBottom;
            } else {
                lastBottomRight = newBottom;
            }
        });

        // Container extension phase
        // Ensure article is long enough for the longest stack
        const lowestPoint = Math.max(lastBottomLeft, lastBottomRight);

        if (lowestPoint > 0) {
            const containerHeight = container.offsetHeight;

            if (lowestPoint > containerHeight) {
                const diff = lowestPoint - containerHeight;
                container.style.paddingBottom = `${diff + 60}px`;
            }
        }
    },

    reset(notes, container) {
        if (notes) {
            notes.forEach(n => {
                n.style.marginTop = '';
                n.style.top = '';
            });
        }
        if (container) {
            container.style.paddingBottom = '';
        }
    }
};

// Initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => SidenoteManager.init());
} else {
    SidenoteManager.init();
}

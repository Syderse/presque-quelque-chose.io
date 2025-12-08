/**
 * Mobile Tooltip System
 * Enables tap-to-reveal tooltips on mobile viewports (< 768px)
 * - On mobile: First tap shows tooltip, second tap navigates (for links)
 * - On desktop: No interference, hover behavior preserved
 * - Tap outside: closes active tooltip
 */

(function () {
  'use strict';

  const MOBILE_BREAKPOINT = 768;
  let activeTooltip = null;

  /**
   * Check if current viewport is mobile
   */
  function isMobileViewport() {
    return window.innerWidth < MOBILE_BREAKPOINT;
  }

  /**
   * Close all open tooltips
   */
  function closeAllTooltips() {
    document.querySelectorAll('[data-tooltip-trigger].show-tooltip').forEach(el => {
      el.classList.remove('show-tooltip');
    });
    activeTooltip = null;
  }

  /**
   * Handle tap on tooltip trigger
   */
  function handleTooltipTap(e) {
    // Only intercept on mobile — let desktop hover work normally
    if (!isMobileViewport()) return;

    const trigger = e.currentTarget;
    const isLink = trigger.tagName === 'A';
    const isActive = trigger.classList.contains('show-tooltip');

    if (isActive) {
      // Second tap: allow default behavior (navigation for links)
      closeAllTooltips();
      return;
    }

    // First tap: show tooltip, prevent navigation
    e.preventDefault();
    e.stopPropagation();
    closeAllTooltips();
    trigger.classList.add('show-tooltip');
    activeTooltip = trigger;
  }

  /**
   * Handle tap outside to close tooltips
   */
  function handleOutsideTap(e) {
    if (!activeTooltip) return;
    if (!isMobileViewport()) return;
    if (!activeTooltip.contains(e.target)) {
      closeAllTooltips();
    }
  }

  /**
   * Close tooltips on resize to desktop
   */
  function handleResize() {
    if (!isMobileViewport() && activeTooltip) {
      closeAllTooltips();
    }
  }

  /**
   * Initialize all tooltip triggers
   */
  function init() {
    document.querySelectorAll('[data-tooltip-trigger]').forEach(trigger => {
      trigger.addEventListener('click', handleTooltipTap);
    });

    document.addEventListener('click', handleOutsideTap);
    window.addEventListener('resize', handleResize);
  }

  // Init on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

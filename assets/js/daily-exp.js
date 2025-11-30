(function() {
    const bar = document.getElementById('daily-exp-bar');
    if (!bar) return;

    function updateExpBar() {
        const now = new Date();
        
        // Calculate seconds passed today
        const secondsPassed = (now.getHours() * 3600) + (now.getMinutes() * 60) + now.getSeconds();
        const totalSeconds = 86400; // 24 * 60 * 60
        
        // Calculate percentage (0 to 100)
        const percent = (secondsPassed / totalSeconds) * 100;
        
        // Apply width
        bar.style.width = `${percent}%`;
    }

    // Run immediately
    updateExpBar();

    // Optional: Update every minute to keep it "live" if the user stays on the page
    setInterval(updateExpBar, 60000);
})();
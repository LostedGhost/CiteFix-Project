document.addEventListener('DOMContentLoaded', function() {
    const currentUrl = new URL(window.location.href);
    const currentPath = currentUrl.pathname;
    
    document.querySelectorAll('a[href]').forEach(link => {
        try {
            const linkUrl = new URL(link.href, window.location.origin);
            
            // Ignorer si:
            // 1. C'est une ancre (#)
            // 2. C'est un lien JavaScript
            // 3. Le domaine est différent
            if (linkUrl.hash || 
                linkUrl.href.startsWith('javascript:') || 
                linkUrl.origin !== currentUrl.origin) {
                return;
            }
            
            // Comparer les chemins
            if (linkUrl.pathname === currentPath) {
                link.classList.add('active');
            }
            
        } catch (e) {
        }
    });
});
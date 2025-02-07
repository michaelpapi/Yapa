document.addEventListener("DOMContentLoaded", function () {
    const userMenu = document.getElementById("user-menu");
    if (!userMenu) return;

    const dropdown = userMenu.querySelector(".user-dropdown");
    if (!dropdown) return;

    let hoverTimeout; // Stores the timeout ID
    let menuVisible = false;

    function showMenu() {
        clearTimeout(hoverTimeout); // Cancel any pending hide action
        dropdown.style.display = "block";
        dropdown.style.opacity = "1";
        menuVisible = true;
    }

    function hideMenu() {
        hoverTimeout = setTimeout(() => {
            dropdown.style.opacity = "0";
            setTimeout(() => {
                if (!menuVisible) dropdown.style.display = "none";
            }, 300); // Matches fade-out transition
        }, 300); // Waits before hiding
    }

    // Show dropdown when hovering over user menu
    userMenu.addEventListener("mouseenter", showMenu);
    dropdown.addEventListener("mouseenter", showMenu);

    // Hide dropdown when mouse leaves both areas
    userMenu.addEventListener("mouseleave", hideMenu);
    dropdown.addEventListener("mouseleave", hideMenu);

    // Toggle dropdown when clicking
    userMenu.addEventListener("click", function (event) {
        event.stopPropagation();
        if (menuVisible) {
            menuVisible = false;
            hideMenu();
        } else {
            showMenu();
        }
    });

    // Hide dropdown when clicking outside
    document.addEventListener("click", function (event) {
        if (!userMenu.contains(event.target) && !dropdown.contains(event.target)) {
            menuVisible = false;
            hideMenu();
        }
    });
});

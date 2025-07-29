
console.log('Executing dropdown-fix.js');

document.addEventListener('DOMContentLoaded', function() {
    // Find the menu and notification buttons
    const userMenuButton = document.getElementById('user-menu-button');
    const notificationsButton = document.getElementById('notifications-button');

    if (userMenuButton) {
        // Create the user menu div
        const userMenu = document.createElement('div');
        userMenu.id = 'user-menu-dropdown';
        userMenu.className = 'hidden absolute right-0 mt-2 w-48 bg-white dark:bg-gray-700 shadow-lg rounded-md py-2 z-50';
        userMenu.innerHTML = `
            <a href="/usuarios/profile/" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600">Mi Perfil</a>
            <a href="/password_change/" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600">Cambiar Contraseña</a>
            <a href="/logout/" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600">Cerrar Sesión</a>
        `;
        userMenuButton.parentNode.appendChild(userMenu);

        // Add click listener to the user menu button
        userMenuButton.addEventListener('click', (event) => {
            event.stopPropagation();
            userMenu.classList.toggle('hidden');
        });
    }

    if (notificationsButton) {
        // Create the notifications menu div
        const notificationsMenu = document.createElement('div');
        notificationsMenu.id = 'notifications-menu-dropdown';
        notificationsMenu.className = 'hidden absolute right-0 mt-2 w-80 bg-white rounded-md shadow-lg py-1 z-50 max-h-96 overflow-y-auto';
        notificationsMenu.innerHTML = `
            <div class="px-4 py-2 border-b border-gray-200">
                <h3 class="text-sm font-medium text-gray-900">Notificaciones</h3>
            </div>
            <div id="notifications-list-container">
                <div class="px-4 py-8 text-center text-gray-500">
                    <p class="text-sm">No tienes notificaciones nuevas.</p>
                </div>
            </div>
        `;
        notificationsButton.parentNode.appendChild(notificationsMenu);

        // Add click listener to the notifications button
        notificationsButton.addEventListener('click', (event) => {
            event.stopPropagation();
            notificationsMenu.classList.toggle('hidden');
        });
    }

    // Close menus when clicking outside
    window.addEventListener('click', () => {
        const userMenu = document.getElementById('user-menu-dropdown');
        if (userMenu && !userMenu.classList.contains('hidden')) {
            userMenu.classList.add('hidden');
        }

        const notificationsMenu = document.getElementById('notifications-menu-dropdown');
        if (notificationsMenu && !notificationsMenu.classList.contains('hidden')) {
            notificationsMenu.classList.add('hidden');
        }
    });
});

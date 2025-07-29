/**
 * Gestor de funcionalidades de clientes
 */
class ClienteManager {
    static initSearch(buscadorEl, sugerenciasEl, onSelectCallback) {
        let debounce;

        if (!buscadorEl || !sugerenciasEl) {
            console.error('ERROR: Elementos buscador o sugerencias no encontrados');
            return;
        }

        buscadorEl.addEventListener('input', () => {
            clearTimeout(debounce);
            debounce = setTimeout(async () => {
                const query = buscadorEl.value.trim();

                if (!query || query.length < 2) {
                    sugerenciasEl.innerHTML = '';
                    sugerenciasEl.classList.add('hidden');
                    return;
                }

                // Mostrar indicador de carga
                sugerenciasEl.innerHTML = '<li class="px-4 py-2 text-blue-500"><i class="fas fa-spinner fa-spin mr-2"></i>Buscando...</li>';
                sugerenciasEl.classList.remove('hidden');

                try {
                    const clientes = await ApiManager.buscarClientes(query);
                    this.renderSugerencias(clientes, sugerenciasEl, onSelectCallback);
                } catch (error) {
                    console.error('Error en búsqueda:', error);
                    sugerenciasEl.innerHTML = `
                        <li class="px-4 py-2 text-red-500">
                            <i class="fas fa-exclamation-triangle mr-2"></i>
                            Error: ${error.message || 'No se pudo conectar con el servidor'}
                        </li>
                    `;
                }
            }, 300);
        });

        // Ocultar sugerencias al hacer clic fuera
        document.addEventListener('click', (e) => {
            if (!buscadorEl.contains(e.target) && !sugerenciasEl.contains(e.target)) {
                sugerenciasEl.classList.add('hidden');
            }
        });
    }

    static renderSugerencias(clientes, sugerenciasEl, onSelectCallback) {
        if (clientes.length === 0) {
            sugerenciasEl.innerHTML = '<li class="px-4 py-2 text-gray-500"><i class="fas fa-search mr-2"></i>No se encontraron clientes</li>';
        } else {
            sugerenciasEl.innerHTML = clientes.map(c => `
                <li data-id="${c.id}" class="px-4 py-2 hover:bg-gray-100 cursor-pointer border-b border-gray-200 last:border-b-0 transition-colors">
                    <div class="font-semibold text-gray-900">${c.empresa || c.razon || 'Sin nombre'}</div>
                    <div class="text-sm text-gray-600">NIT: ${c.nit || c.codigo || 'N/A'}</div>
                    ${c.razon && c.razon !== c.empresa ? `<div class="text-sm text-gray-500">${c.razon}</div>` : ''}
                    ${c.direccion ? `<div class="text-xs text-gray-400">${c.direccion}</div>` : ''}
                </li>
            `).join('');

            // Event listeners para selección
            sugerenciasEl.querySelectorAll('li[data-id]').forEach(li => {
                li.onclick = (e) => {
                    e.preventDefault();
                    this.selectFromSugerencia(li, sugerenciasEl, onSelectCallback);
                };
            });
        }

        sugerenciasEl.classList.remove('hidden');
    }

    static selectFromSugerencia(li, sugerenciasEl, onSelectCallback) {
        const empresaText = li.querySelector('.font-semibold').textContent;
        const nitText = li.querySelector('.text-gray-600').textContent;
        
        const buscador = document.getElementById('buscador');
        buscador.value = `${empresaText} - ${nitText}`;
        buscador.style.backgroundColor = '#f0f9ff';
        buscador.style.borderColor = '#0ea5e9';

        sugerenciasEl.innerHTML = '';
        sugerenciasEl.classList.add('hidden');

        onSelectCallback(li.dataset.id);
    }

    static preseleccionar(cliente, buscadorEl) {
        buscadorEl.value = `${cliente.empresa} (${cliente.nit})`;
        buscadorEl.style.backgroundColor = '#f0f9ff';
        buscadorEl.style.borderColor = '#0ea5e9';
        buscadorEl.readOnly = true;

        // Agregar botón para cambiar cliente
        const cambiarBtn = document.createElement('button');
        cambiarBtn.innerHTML = '<i class="fas fa-edit mr-1"></i>Cambiar Cliente';
        cambiarBtn.className = 'ml-2 px-3 py-2 bg-blue-500 hover:bg-blue-600 text-white text-sm rounded-lg transition-colors';
        cambiarBtn.onclick = () => {
            buscadorEl.value = '';
            buscadorEl.style.backgroundColor = '';
            buscadorEl.style.borderColor = '';
            buscadorEl.readOnly = false;
            cambiarBtn.remove();
            
            document.getElementById('step2').style.display = 'none';
            document.getElementById('catalogo').style.display = 'none';
            
            buscadorEl.focus();
        };

        buscadorEl.parentElement.appendChild(cambiarBtn);
    }
}
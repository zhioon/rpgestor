/**
 * Gestor de productos
 */
class ProductoManager {
    static render(productos, container) {
        container.innerHTML = productos.map(p => this.renderProductCard(p)).join('');
    }

    static renderProductCard(producto) {
        const precio = parseFloat(producto.precio);
        const stock = parseInt(producto.stock, 10);
        const descuento = parseFloat(producto.descuento);
        const imgSrc = producto.imagen_url || '/static/img/placeholder.png';

        return `
            <div class="product-card ${descuento > 0 ? 'product-card-descuento' : 'product-card-normal'}">
                <div class="flex items-start space-x-4">
                    <!-- Columna izquierda: Imagen y Stock -->
                    <div class="flex-shrink-0">
                        <!-- Imagen del producto -->
                        <div class="w-32 h-40 md:w-40 md:h-48 bg-gray-200 border border-gray-300 rounded-xl flex items-center justify-center mb-2 overflow-hidden">
                            ${producto.imagen_url ?
                                `<img src="${imgSrc}" alt="${producto.nombre}" class="w-full h-full object-cover cursor-pointer" onclick="ImageModal.open('${imgSrc}')" loading="lazy">` :
                                `<div class="text-center text-gray-500">
                                    <i class="fas fa-image text-4xl"></i>
                                    <div class="text-sm md:text-base font-medium mt-2">Sin Imagen</div>
                                </div>`
                            }
                        </div>

                        <!-- Stock debajo de la imagen -->
                        <div class="text-center">
                            <div class="flex items-center justify-center space-x-2">
                                <span class="text-xl font-bold ${stock > 10 ? 'text-green-600' : stock > 0 ? 'text-yellow-600' : 'text-red-600'}">
                                    ${stock}
                                </span>
                                <span class="text-sm px-2 py-1 rounded-full ${stock > 10 ? 'bg-green-100 text-green-800' : stock > 0 ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800'}">
                                    ${stock > 10 ? 'Disponible' : stock > 0 ? 'Poco stock' : 'Agotado'}
                                </span>
                            </div>
                        </div>
                    </div>

                    <!-- Información del producto -->
                    <div class="flex-1 min-w-0 flex flex-col justify-between py-1">
                        <!-- Parte superior: Código, nombre y precio -->
                        <div>
                            <div class="text-xl md:text-2xl font-bold text-gray-900 mb-1">${producto.codigo}</div>
                            <div class="text-base md:text-lg font-semibold text-gray-800 mb-3 leading-tight">${producto.nombre}</div>
                            <div class="mb-4">
                                <span class="text-base md:text-lg text-gray-700">Precio unitario: </span>
                                <span class="text-lg md:text-xl font-bold text-gray-900">${Utils.formatCurrency(precio)}</span>
                            </div>
                        </div>

                        <!-- Parte inferior: Controles -->
                        <div class="space-y-2">
                            <!-- Primera fila: Cantidad y Fuera de stock -->
                            <div class="flex items-start space-x-4">
                                <div class="flex items-center space-x-2">
                                    <label class="text-sm text-gray-700">Cantidad:</label>
                                    <input type="number" class="prod-cant w-16 px-2 py-1 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-center font-semibold"
                                           value="1" min="1" max="${stock || 1}">
                                </div>

                                <label class="flex items-start space-x-2">
                                    <input type="checkbox" class="fuera-stock w-4 h-4 rounded mt-0.5" data-id="${producto.id}" onchange="ProductoManager.toggleNotaFueraStock(this, '${producto.id}')">
                                    <span class="text-sm text-gray-700 leading-tight">Fuera de<br>stock</span>
                                </label>
                            </div>

                            <!-- Segunda fila: Botón Agregar -->
                            <div>
                                <button class="add-btn bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors duration-200 flex items-center font-semibold"
                                        data-id="${producto.id}"
                                        data-codigo="${producto.codigo}"
                                        data-nombre="${producto.nombre}"
                                        data-precio="${precio}"
                                        data-descuento="${descuento}"
                                        data-stock="${stock}">
                                    <i class="fas fa-plus mr-1"></i>
                                    Agregar
                                </button>
                            </div>
                        </div>

                        <!-- Campo de nota para fuera de stock -->
                        <div id="nota-fuera-stock-${producto.id}" class="hidden mt-2">
                            <label class="text-xs text-gray-600">Motivo para pedir fuera de stock:</label>
                            <textarea class="nota-fuera-stock w-full px-2 py-1 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-xs mt-1"
                                      rows="2"
                                      placeholder="Ej: Cliente solicita cantidad específica, producto en tránsito, etc."></textarea>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    static toggleNotaFueraStock(checkbox, productId) {
        const notaDiv = document.getElementById(`nota-fuera-stock-${productId}`);
        if (checkbox.checked) {
            notaDiv.classList.remove('hidden');
        } else {
            notaDiv.classList.add('hidden');
            notaDiv.querySelector('textarea').value = '';
        }
    }
}

/**
 * Gestor de búsqueda de productos
 */
class ProductSearchManager {
    static init() {
        const searchInput = document.getElementById('buscar-productos');
        if (!searchInput) return;

        let debounce;
        searchInput.addEventListener('input', () => {
            clearTimeout(debounce);
            debounce = setTimeout(() => {
                this.filterProducts(searchInput.value.trim());
            }, 200);
        });
    }

    static filterProducts(query) {
        const products = document.querySelectorAll('.product-card');
        
        products.forEach(card => {
            const codigo = card.querySelector('[data-codigo]')?.dataset.codigo || '';
            const nombre = card.querySelector('[data-nombre]')?.dataset.nombre || '';
            
            const matches = !query || 
                           codigo.toLowerCase().includes(query.toLowerCase()) ||
                           nombre.toLowerCase().includes(query.toLowerCase());
            
            card.style.display = matches ? 'block' : 'none';
        });
    }

    static clear() {
        const searchInput = document.getElementById('buscar-productos');
        if (searchInput) {
            searchInput.value = '';
            this.filterProducts('');
        }
    }
}

// Función global para compatibilidad
window.clearProductSearch = () => ProductSearchManager.clear();
window.toggleNotaFueraStock = (checkbox, productId) => ProductoManager.toggleNotaFueraStock(checkbox, productId);
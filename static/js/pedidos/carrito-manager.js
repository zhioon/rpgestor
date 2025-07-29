/**
 * Gestor del carrito de compras
 */
class CarritoManager {
    static addItem(data, resumenBody) {
        const { id, codigo, nombre } = data;
        const precio = parseFloat(data.precio);
        const stock = parseInt(data.stock, 10);
        const descuento = parseFloat(data.descuento);

        const card = document.querySelector(`button[data-id="${id}"]`).closest('.product-card');
        const prodCant = card.querySelector('.prod-cant');
        let qty = Math.max(1, parseInt(prodCant.value, 10) || 1);
        const fuera = card.querySelector('.fuera-stock').checked;

        // Validar stock
        if (!fuera && qty > stock) {
            NotificationManager.show(`Solo hay ${stock} unidades en stock. Se ajustó la cantidad o marca "Fuera stock" para pedir más.`, 'warning');
            qty = stock;
            prodCant.value = stock;
        }

        // Verificar si ya existe en el carrito
        let row = resumenBody.querySelector(`tr[data-id="${id}"]`);
        if (row) {
            const inp = row.querySelector('.cant');
            inp.value = parseInt(inp.value, 10) + qty;
            inp.dispatchEvent(new Event('input'));
            return;
        }

        // Crear nueva fila
        row = this.createCartRow(data, qty, fuera);
        resumenBody.appendChild(row);
        this.bindRowEvents(row);

        NotificationManager.show(`${nombre} agregado al carrito`, 'success');
    }

    static createCartRow(data, qty, fuera) {
        const { id, codigo, nombre, precio, descuento, stock } = data;
        const precioNum = parseFloat(precio);

        const row = document.createElement('tr');
        row.dataset.id = id;
        row.dataset.stock = stock;
        row.className = 'hover:bg-gray-50 transition-colors duration-200';

        if (descuento > 0) row.classList.add('bg-yellow-50');
        if (fuera) row.classList.add('bg-red-50');

        row.innerHTML = `
            <td class="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">${codigo}</td>
            <td class="px-4 py-3 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">${nombre}</div>
            </td>
            <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-900">${Utils.formatCurrency(precioNum)}</td>
            <td class="px-4 py-3 whitespace-nowrap">
                <input type="number" class="cant w-16 px-2 py-1 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                       value="${qty}" min="1" max="${fuera ? qty : stock}">
            </td>
            <td class="px-4 py-3 whitespace-nowrap text-sm font-medium text-green-600 subtotal">${Utils.formatCurrency(precioNum * qty)}</td>
            <td class="px-4 py-3 whitespace-nowrap text-sm font-medium">
                <button class="remove bg-red-100 hover:bg-red-200 text-red-800 px-2 py-1 rounded transition-colors duration-200">
                    <i class="fas fa-trash text-xs"></i>
                </button>
            </td>
            <td class="px-4 py-3 whitespace-nowrap">
                <input type="text" class="nota w-full px-2 py-1 border border-gray-300 rounded text-sm" placeholder="Nota...">
            </td>
        `;

        return row;
    }

    static bindRowEvents(row) {
        // Evento para cambio de cantidad
        row.querySelector('.cant').addEventListener('input', e => {
            let v = parseInt(e.target.value, 10) || 1;
            if (v < 1) v = 1;

            const maxStock = parseInt(row.dataset.stock, 10);
            const fuera = row.classList.contains('bg-red-50');

            if (!fuera && v > maxStock) {
                NotificationManager.show(`Solo hay ${maxStock} unidades en stock. Cantidad ajustada.`, 'warning');
                v = maxStock;
            }

            e.target.value = v;

            // Actualizar subtotal
            const precio = parseFloat(row.children[2].textContent.replace(/[$.,]/g, ''));
            row.querySelector('.subtotal').textContent = Utils.formatCurrency(precio * v);

            // Actualizar totales
            this.updateTotal(document.getElementById('total'), row.closest('tbody'));
            this.updateCompacto(document.getElementById('carrito-compacto'), row.closest('tbody'));
        });

        // Evento para eliminar
        row.querySelector('.remove').onclick = () => {
            this.removeItem(row);
        };
    }

    static removeItem(row) {
        row.remove();
        this.updateTotal(document.getElementById('total'), document.getElementById('resumen-body'));
        this.updateCompacto(document.getElementById('carrito-compacto'), document.getElementById('resumen-body'));

        const btnConfirm = document.getElementById('btn-confirmar');
        if (document.getElementById('resumen-body').children.length === 0) {
            btnConfirm.disabled = true;
        }

        NotificationManager.show('Producto removido del carrito', 'info');
    }

    static updateTotal(totalEl, resumenBody) {
        const sum = Array.from(resumenBody.querySelectorAll('.subtotal')).reduce((a, td) =>
            a + parseFloat(td.textContent.replace(/[$.,]/g, '')), 0
        );
        totalEl.textContent = Utils.formatCurrency(sum);
    }

    static updateCompacto(carritoCompacto, resumenBody) {
        const rows = Array.from(resumenBody.querySelectorAll('tr[data-id]'));

        if (rows.length === 0) {
            carritoCompacto.innerHTML = `
                <div class="text-center text-gray-500 py-8">
                    <i class="fas fa-shopping-cart text-4xl mb-3 text-gray-300"></i>
                    <p class="text-sm">Tu carrito está vacío</p>
                    <p class="text-xs text-gray-400">Agrega productos para comenzar</p>
                </div>
            `;
            return;
        }

        const itemsHTML = rows.map(row => {
            const codigo = row.children[0].textContent.trim();
            const nombre = row.children[1].textContent.trim();
            const precio = row.children[2].textContent;
            const cantidad = row.querySelector('.cant').value;
            const subtotal = row.querySelector('.subtotal').textContent;

            return `
                <div class="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
                    <div class="flex-1 min-w-0">
                        <div class="text-sm font-medium text-gray-900 truncate">${nombre}</div>
                        <div class="text-xs text-gray-500">${codigo} • ${precio} c/u</div>
                    </div>
                    <div class="flex items-center space-x-2 ml-2">
                        <span class="text-sm font-medium text-gray-600">×${cantidad}</span>
                        <span class="text-sm font-bold text-green-600">${subtotal}</span>
                        <button onclick="CarritoManager.removeFromCompacto('${row.dataset.id}')"
                                class="text-red-500 hover:text-red-700 p-1"
                                title="Eliminar producto">
                            <i class="fas fa-times text-xs"></i>
                        </button>
                    </div>
                </div>
            `;
        }).join('');

        carritoCompacto.innerHTML = `
            <div class="space-y-2">
                ${itemsHTML}
            </div>
            <div class="mt-4 pt-3 border-t border-gray-200">
                <button onclick="CarritoDetailManager.toggle()"
                        class="w-full text-xs text-blue-600 hover:text-blue-800 py-2">
                    <i class="fas fa-list mr-1"></i>Ver detalle completo
                </button>
            </div>
        `;
    }

    static removeFromCompacto(productId) {
        const row = document.getElementById('resumen-body').querySelector(`tr[data-id="${productId}"]`);
        if (row) {
            this.removeItem(row);
        }
    }

    static getItems(resumenBody) {
        return Array.from(resumenBody.querySelectorAll('tr[data-id]')).map(row => ({
            producto: parseInt(row.dataset.id, 10), // Cambiar 'id' por 'producto' para que coincida con el backend
            cantidad: parseInt(row.querySelector('.cant').value, 10),
            nota: row.querySelector('.nota').value.trim()
        }));
    }
}

/**
 * Gestor del carrito detallado
 */
class CarritoDetailManager {
    static toggle() {
        const carritoDetallado = document.getElementById('carrito-detallado');
        const isHidden = carritoDetallado.style.display === 'none' || carritoDetallado.style.display === '';

        carritoDetallado.style.display = isHidden ? 'block' : 'none';

        if (isHidden) {
            carritoDetallado.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }
}

// Funciones globales para compatibilidad
window.removeFromCarrito = (productId) => CarritoManager.removeFromCompacto(productId);
window.toggleCarritoDetallado = () => CarritoDetailManager.toggle();
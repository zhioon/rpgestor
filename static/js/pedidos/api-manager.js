/**
 * Gestor de llamadas API
 */
class ApiManager {
    static get csrftoken() {
        return document.querySelector('meta[name=csrf-token]').content;
    }

    static async buscarClientes(query) {
        const url = `/pedidos/ajax/buscar-cliente/?q=${encodeURIComponent(query)}`;
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrftoken
            }
        });

        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status} - ${response.statusText}`);
        }

        const data = await response.json();
        return data.clientes || [];
    }

    static async getPriceTypes(clienteId) {
        const response = await fetch(`/pedidos/ajax/price-types/${clienteId}/`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrftoken
            }
        });

        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status} - ${response.statusText}`);
        }

        const data = await response.json();
        return data.price_types || [];
    }

    static async getProductos(clienteId, priceType) {
        const response = await fetch(`/pedidos/ajax/productos/${clienteId}/${priceType}/`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrftoken
            }
        });

        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status} - ${response.statusText}`);
        }

        const data = await response.json();
        return data.productos || [];
    }

    static async confirmarPedido(clienteId, items, nota = '') {
        const response = await fetch('/pedidos/confirmar/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrftoken
            },
            body: JSON.stringify({ 
                cliente: clienteId, 
                items: items,
                nota: nota
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        return await response.json();
    }
}
/**
 * Módulo principal para crear pedidos
 */
class CrearPedidoManager {
    constructor() {
        this.clienteId = null;
        this.csrftoken = document.querySelector('meta[name=csrf-token]').content;
        this.elementos = this.initElementos();
        this.clientePreseleccionado = window.clientePreseleccionado || null;
    }

    initElementos() {
        return {
            buscador: document.getElementById('buscador'),
            sugerencias: document.getElementById('sugerencias'),
            step2: document.getElementById('step2'),
            priceTypeSel: document.getElementById('price-type'),
            catalogoEl: document.getElementById('catalogo'),
            resumenBody: document.getElementById('resumen-body'),
            totalEl: document.getElementById('total'),
            btnConfirm: document.getElementById('btn-confirmar'),
            productosContainer: document.getElementById('productos-container'),
            carritoCompacto: document.getElementById('carrito-compacto')
        };
    }

    async init() {
        console.log('🚀 Inicializando CrearPedidoManager...');
        
        try {
            this.initClientePreseleccionado();
            this.initClientSearch();
            this.initEventListeners();
            console.log('✅ Inicialización completada');
        } catch (error) {
            console.error('❌ Error en inicialización:', error);
            NotificationManager.show('Error al inicializar la aplicación', 'error');
        }
    }

    initEventListeners() {
        // Tipo de precio
        this.elementos.priceTypeSel.addEventListener('change', () => this.loadProductos());
        
        // Confirmar pedido
        this.elementos.btnConfirm.addEventListener('click', () => this.confirmarPedido());
        
        // Delegación de eventos para productos
        this.elementos.productosContainer.addEventListener('click', (e) => this.handleProductClick(e));
    }

    initClientePreseleccionado() {
        if (this.clientePreseleccionado) {
            ClienteManager.preseleccionar(this.clientePreseleccionado, this.elementos.buscador);
            this.selectCliente(this.clientePreseleccionado.id);
            NotificationManager.show(`Cliente seleccionado: ${this.clientePreseleccionado.empresa}`, 'success');
        }
    }

    initClientSearch() {
        ClienteManager.initSearch(this.elementos.buscador, this.elementos.sugerencias, (id) => this.selectCliente(id));
    }

    async selectCliente(id) {
        try {
            this.clienteId = id;
            const priceTypes = await ApiManager.getPriceTypes(id);
            
            UIManager.populatePriceTypes(this.elementos.priceTypeSel, priceTypes);
            UIManager.showStep(this.elementos.step2);
            UIManager.hideStep(this.elementos.catalogoEl);
            
            this.clearCarrito();
            this.elementos.step2.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            
        } catch (error) {
            console.error('Error al seleccionar cliente:', error);
            NotificationManager.show('Error al cargar información del cliente', 'error');
        }
    }

    async loadProductos() {
        try {
            const priceType = this.elementos.priceTypeSel.value;
            if (!priceType || !this.clienteId) return;

            const productos = await ApiManager.getProductos(this.clienteId, priceType);
            ProductoManager.render(productos, this.elementos.productosContainer);
            
            UIManager.showStep(this.elementos.catalogoEl);
            ProductSearchManager.init();
            
        } catch (error) {
            console.error('Error al cargar productos:', error);
            NotificationManager.show('Error al cargar productos', 'error');
        }
    }

    handleProductClick(e) {
        const addBtn = e.target.closest('.add-btn');
        if (addBtn) {
            e.preventDefault();
            CarritoManager.addItem(addBtn.dataset, this.elementos.resumenBody);
            this.updateUI();
            return;
        }

        const removeBtn = e.target.closest('.remove');
        if (removeBtn) {
            e.preventDefault();
            CarritoManager.removeItem(removeBtn.closest('tr'));
            this.updateUI();
        }
    }

    updateUI() {
        CarritoManager.updateTotal(this.elementos.totalEl, this.elementos.resumenBody);
        CarritoManager.updateCompacto(this.elementos.carritoCompacto, this.elementos.resumenBody);
        this.elementos.btnConfirm.disabled = this.elementos.resumenBody.children.length === 0;
    }

    clearCarrito() {
        this.elementos.resumenBody.innerHTML = '';
        this.updateUI();
    }

    async confirmarPedido() {
        const originalText = this.elementos.btnConfirm.innerHTML;
        
        try {
            const items = CarritoManager.getItems(this.elementos.resumenBody);
            if (items.length === 0) {
                NotificationManager.show('Agrega productos al carrito', 'warning');
                return;
            }

            if (!this.clienteId) {
                NotificationManager.show('Selecciona un cliente primero', 'warning');
                return;
            }

            // Capturar la nota del pedido
            const notaPedido = document.getElementById('nota-pedido').value.trim();

            console.log('Confirmando pedido para cliente:', this.clienteId, 'con items:', items, 'nota:', notaPedido);
            
            UIManager.setLoadingState(this.elementos.btnConfirm, true);

            const response = await ApiManager.confirmarPedido(this.clienteId, items, notaPedido);
            
            console.log('Respuesta del servidor:', response);
            
            if (response.redirect_url) {
                NotificationManager.show('Pedido creado exitosamente', 'success');
                // Pequeño delay para que se vea la notificación
                setTimeout(() => {
                    window.location.href = response.redirect_url;
                }, 500);
            } else {
                throw new Error('No se recibió URL de redirección');
            }

        } catch (error) {
            console.error('Error al confirmar pedido:', error);
            
            let errorMessage = 'Error al confirmar el pedido';
            if (error.message.includes('404')) {
                errorMessage = 'Endpoint no encontrado. Verifica la configuración del servidor.';
            } else if (error.message.includes('500')) {
                errorMessage = 'Error interno del servidor. Intenta de nuevo.';
            } else if (error.message.includes('403')) {
                errorMessage = 'No tienes permisos para realizar esta acción.';
            }
            
            NotificationManager.show(errorMessage, 'error');
            UIManager.setLoadingState(this.elementos.btnConfirm, false, originalText);
        }
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.crearPedidoManager = new CrearPedidoManager();
    window.crearPedidoManager.init();
});
/**
 * Utilidades generales
 */
class Utils {
    static formatCurrency(value) {
        return Math.round(value).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    }

    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

/**
 * Gestor de interfaz de usuario
 */
class UIManager {
    static setLoadingState(element, isLoading, originalText = '') {
        if (isLoading) {
            element.disabled = true;
            element.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Cargando...';
        } else {
            element.disabled = false;
            element.innerHTML = originalText;
        }
    }

    static showStep(element) {
        element.style.display = 'block';
    }

    static hideStep(element) {
        element.style.display = 'none';
    }

    static populatePriceTypes(selectElement, priceTypes) {
        selectElement.innerHTML = `<option value="">-- Selecciona tipo de precio --</option>` +
            priceTypes.map(t => `<option value="${t.value}">${t.label}</option>`).join('');
    }
}

/**
 * Gestor del modal de imágenes
 */
class ImageModal {
    static init() {
        const modal = document.getElementById('image-modal');
        const modalImage = modal.querySelector('img');
        const closeButton = document.getElementById('close-image-modal');

        closeButton.addEventListener('click', () => {
            modal.classList.add('hidden');
        });

        modal.addEventListener('click', event => {
            if (event.target === modal) {
                modal.classList.add('hidden');
            }
        });

        // Hacer disponible globalmente
        window.ImageModal = this;
    }

    static open(imageUrl) {
        const modal = document.getElementById('image-modal');
        const modalImage = modal.querySelector('img');
        
        modalImage.src = imageUrl;
        modal.classList.remove('hidden');
    }
}

// Inicializar modal cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    ImageModal.init();
});

// Función global para compatibilidad
window.openImageModal = (imageUrl) => ImageModal.open(imageUrl);
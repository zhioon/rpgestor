from django import forms
from django.forms import inlineformset_factory
from .models import Pedido, ItemPedido
from clientes.models import Cliente
from productos.models import Producto

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
        }

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['producto', 'cantidad', 'descuento']
        widgets = {
            'producto':    forms.Select(attrs={'class': 'form-control'}),
            'cantidad':    forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'descuento':   forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01}),
        }

# Creamos el inline formset: mínimo 1, máximo 10 ítems por pedido
ItemPedidoFormSet = inlineformset_factory(
    Pedido, ItemPedido,
    form=ItemPedidoForm,
    extra=1,                # 1 formulario extra vacío
    can_delete=True,
    min_num=1,
    validate_min=True,
    max_num=10,
    validate_max=True
)

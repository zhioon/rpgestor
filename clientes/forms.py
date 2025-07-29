from django import forms

class UploadExcelForm(forms.Form):
    excel_file = forms.FileField(
        label='Seleccione archivo .xlsx de clientes',
        help_text='La primera fila debe ser el encabezado con todos los campos'
    )

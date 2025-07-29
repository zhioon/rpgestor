from django import forms

class UploadExcelForm(forms.Form):
    excel_file = forms.FileField(
        label='Seleccione archivo .xlsx',
        help_text='Las cabeceras reales están en la fila 5 (header=4)'
    )

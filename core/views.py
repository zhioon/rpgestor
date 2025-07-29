from django.shortcuts import render
from .models import TestModel
from .utils import export_queryset_to_csv

def export_tests(request):
    """
    Exporta todas las instancias de TestModel a un CSV descargable.
    """
    qs = TestModel.objects.all()
    return export_queryset_to_csv(
        queryset=qs,
        fields=['id', 'name', 'created_at', 'updated_at'],
        filename='testmodels.csv'
    )


# Create your views here.

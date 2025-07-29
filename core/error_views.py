from django.shortcuts import render

def custom_404_view(request, exception=None):
    """
    Vista personalizada para errores 404
    """
    return render(request, '404.html', status=404)

def custom_500_view(request):
    """
    Vista personalizada para errores 500
    """
    return render(request, '500.html', status=500)
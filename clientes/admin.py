from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at', 'updated_at')
    # opcional: search_fields = ('data__Empresa', 'data__Nit')


# Register your models here.

from django.contrib import admin
from .models import Grupo, SubGrupo, Producto
from django.utils.html import format_html

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'created_at')

@admin.register(SubGrupo)
class SubGrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'grupo', 'created_at')
    list_filter  = ('grupo',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'codigo','nombre','grupo','subgrupo','precio1','stock','imagen_thumbnail'
    )
    list_filter  = ('grupo','subgrupo')
    search_fields= ('codigo','nombre')
    readonly_fields = ('imagen_preview',)

    def imagen_thumbnail(self, obj):
        if obj.imagen:
            return format_html(f'<img src="{obj.imagen.url}" width="100" />')
        return "(Sin imagen)"
    imagen_thumbnail.short_description = 'Imagen'

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html(f'<img src="{obj.imagen.url}" width="300" />')
        return "(Sin imagen)"
    imagen_preview.short_description = 'Previsualización'

# Register your models here.

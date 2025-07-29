from django.contrib import admin
from .models import TestModel

@admin.register(TestModel)
class TestModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')


# Register your models here.

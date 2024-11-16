from django.contrib import admin
from .models import Poet

class PoetAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'birth_year', 'death_year')
    list_filter = ['birth_year']
    search_fields = ['full_name', 'biography']

admin.site.register(Poet, PoetAdmin)
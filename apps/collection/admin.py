from django.contrib import admin
from .models import Collection

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type')
    search_fields = ['title', 'description', 'type']

admin.site.register(Collection, CollectionAdmin)
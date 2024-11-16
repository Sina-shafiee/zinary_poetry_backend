from django.contrib import admin
from .models import Poem

class PoemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'year_written')
    search_fields = ['title']

admin.site.register(Poem, PoemAdmin)
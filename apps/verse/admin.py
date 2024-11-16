from django.contrib import admin
from .models import Verse

class VerseAdmin(admin.ModelAdmin):
    list_display = ('id', 'order','first_hemistich', 'second_hemistich')

admin.site.register(Verse, VerseAdmin)
from django.db import models
from apps.poet.models import Poet
from apps.collection.models import Collection

class Poem(models.Model):
    title = models.CharField(max_length=255)
    year_written = models.DateField(null=True, blank=True)
    
    poet = models.ForeignKey(Poet, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "poems"

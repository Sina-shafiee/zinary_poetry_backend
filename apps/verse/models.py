from django.db import models
from apps.poem.models import Poem


class Verse(models.Model):
    order = models.IntegerField()

    first_hemistich = models.CharField(max_length=255)
    second_hemistich = models.CharField(max_length=255)

    poem = models.ForeignKey(Poem, on_delete=models.CASCADE)

    def __str__(self):
        return "order: {} - {}".format(self.order,self.first_hemistich)

    class Meta:
        db_table = "verses"
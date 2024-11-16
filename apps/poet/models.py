from django.db import models

class Poet(models.Model):
    full_name = models.CharField(max_length=150)

    birth_year = models.DateField(null=True, blank=True)
    death_year = models.DateField(null=True, blank=True)

    biography = models.TextField()

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "poets"

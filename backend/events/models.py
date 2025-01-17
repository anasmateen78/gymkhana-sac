from django.db import models
from main.models import Society, Committee


class Event(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    location = models.CharField(max_length=64)
    date = models.DateTimeField()
    society = models.ForeignKey(Society, null=True, blank=True, default=None, on_delete=models.CASCADE,
                             help_text="Leave blank to make this a general event.")
    committee = models.ForeignKey(Committee, null=True, blank=True, default=None, on_delete=models.CASCADE,
                             help_text="Leave blank to make this a general event.")
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.name

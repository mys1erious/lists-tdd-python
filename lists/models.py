from django.db import models
from django.urls import reverse


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(
        to='List',
        default=None,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('list', 'text')
        ordering = ('id',)

    def __str__(self):
        return self.text


class List(models.Model):
    def get_absolute_url(self):
        return reverse('view_list', kwargs={'pk': self.id})

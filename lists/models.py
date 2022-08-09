from django.db import models
from django.urls import reverse


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(
        to='List',
        default=None,
        on_delete=models.CASCADE
    )


class List(models.Model):
    def get_absolute_url(self):
        return reverse('view_list', kwargs={'pk': self.id})

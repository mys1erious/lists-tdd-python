from django.db import models
from django.urls import reverse
from django.conf import settings


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
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, null=True
    )

    @property
    def name(self):
        return self.item_set.first().text

    @staticmethod
    def create_new(first_item_text, owner=None):
        lst = List.objects.create(owner=owner)
        Item.objects.create(text=first_item_text, list=lst)
        return lst

    def get_absolute_url(self):
        return reverse('view_list', kwargs={'pk': self.id})

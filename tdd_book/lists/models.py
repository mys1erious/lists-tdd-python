from django.db import models


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(
        to='List',
        default=None,
        on_delete=models.CASCADE
    )


class List(models.Model):
    ...

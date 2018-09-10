from django.db import models


class List(models.Model):
    pass


# Create your models here.
class Item(models.Model):
    text = models.CharField(max_length=255, default="nothing...")
    todo_list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.text

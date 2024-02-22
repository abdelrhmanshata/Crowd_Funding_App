from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @classmethod
    def getAllCategory(cls):
        return cls.objects.all()

    @classmethod
    def getCategory(cls, categoryID):
        return cls.objects.get(id=categoryID)

    @classmethod
    def deleteCategory(cls, categoryID):
        return cls.objects.get(id=categoryID).delete()

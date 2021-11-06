from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Photo(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=False, blank=False)
    photo_title = models.CharField(max_length=200,null=False, blank=False)
    photo_price = models.FloatField(null=False, blank=False)
    frame_size = models.CharField(max_length=200,null=False, blank=False)

    def __str__(self):
        return self.photo_title


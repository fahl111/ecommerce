from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=20)
    desc=models.TextField()
    image=models.ImageField(upload_to="Category",null=True,blank=True)
    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=30)
    desc = models.TextField(default="")
    image = models.ImageField(upload_to='product', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def str(self):
        return self.name
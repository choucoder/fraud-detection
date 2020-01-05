from django.db import models
from datetime import datetime

class Admin(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)

    def __str__(self):

        return f'Admin<{self.username}>'


class User(models.Model):

    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12)
    email_id = models.EmailField()
    amount_limit = models.IntegerField()
    ip_address = models.GenericIPAddressField()

    def __str__(self):

        return f'User<{self.username}>'


class Product(models.Model):

    id_product = models.CharField(max_length=100, primary_key=True)
    product_name = models.CharField(max_length=100)
    cost = models.FloatField()
    image = models.CharField(max_length=500)

    def __str__(self):

        return f'Product<{self.id_product}, {self.product_name}>'


class TransactionHistory(models.Model):

    id_history = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cost = models.FloatField()
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(default=datetime.now())

# First put in settings INSTALLED_APPS the name of app (mogli)
# Seconds make python3.7 manage.py makemigrations mogli
# Then, make python3.7 manage.py migrate
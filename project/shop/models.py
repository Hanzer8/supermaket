from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime
from django.urls import reverse


class Product(models.Model):
   name = models.CharField(max_length=50)
   description = models.TextField(null=True)
   quantity = models.IntegerField(validators=[MinValueValidator(0)],
                                  default=1)
   category = models.ForeignKey(to='Category', on_delete=models.CASCADE,
                                related_name='products',
                                null=True)
   price = models.FloatField(validators=[MinValueValidator(0.0)], )

   def __str__(self):
      truncated_description = self.description[:20] + '...' if self.description else ''
      return f'{self.name}: {truncated_description}'

   def get_absolute_url(self):
      return reverse('product', args=[str(self.id)])


# Категория, к которой будет привязываться товар
class    Category(models.Model):
   name = models.CharField(max_length=100, unique=True)

   def __str__(self):
      return self.name


director = 'DI'
admin = 'AD'
cook = 'CO'
cashier = 'CA'
cleaner = 'CL'

POSITIONS = [
   (director, 'Директор'),
   (admin, 'Администратор'),
   (cook, 'Повар'),
   (cashier, 'Кассир'),
   (cleaner, 'Уборщик')
]


class Staff(models.Model):
   full_name = models.CharField(max_length=255)
   position = models.CharField(max_length=2,
                               choices=POSITIONS,
                               default=cashier)
   labor_contract = models.IntegerField()


class Order(models.Model):
   time_in = models.DateTimeField(auto_now_add=True)
   time_out = models.DateTimeField(null=True)
   cost = models.FloatField(default=0.0)
   pickup = models.BooleanField(default=False)
   complete = models.BooleanField(default=False)
   staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
   products = models.ManyToManyField(Product, through='ProductOrder')

   def finish_order(self):
      self.time_out = datetime.now()
      self.complete = True
      self.save()


class ProductOrder(models.Model):
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   order = models.ForeignKey(Order, on_delete=models.CASCADE)
   _amount = models.IntegerField(default=1)

   def product_sum(self):
      product_price = self.product.price
      return product_price * self.amount

   @property
   def amount(self):
      return self._amount

   @amount.setter
   def amount(self, value):
      self._amount = int(value) if value >= 0 else 0
      self.save()

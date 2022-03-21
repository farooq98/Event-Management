from django.db import models

# Create your models here.

class Order(models.Model):

    def __str__(self):
        return str(self.id)

class OrderLine(models.Model):

    order = models.ForeignKey(Order, related_name='order_lines', on_delete=models.PROTECT)
    destination = models.CharField(max_length=255)
    destination_iata = models.CharField(max_length=50)
    origin = models.CharField(max_length=255)
    origin_iata = models.CharField(max_length=50)
    type = models.CharField(max_length=255)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()

    def __str__(self):
        return str(self.id)
    
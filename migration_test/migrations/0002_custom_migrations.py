# Generated by Django 3.2.12 on 2022-03-21 16:07

from django.db import migrations, models
import random
from django.utils import timezone
from datetime import timedelta
import time

def add_default_data(apps, schema_editor):
    t1 = time.time()
    Order = apps.get_model("migration_test", "Order")
    OrderLine = apps.get_model("migration_test", "OrderLine")
    db_alias = schema_editor.connection.alias

    Order.objects.using(db_alias).bulk_create([
        Order() for i in range(100000)
    ])

    order_ids = Order.objects.all().values_list("id", flat=True)
    CITIES = [
        ('Karachi', "KHI"), 
        ("Lahore", "LHE"), 
        ("Islamabad", "ISL")
    ]

    TYPES = [
        "ONEWAY",
        "RETURN",
    ]

    for _ in range(0, 5000000, 100000):

        order_line_data = []

        for _ in range(100000):
            destination = random.choice(CITIES)
            origin = random.choice(CITIES)
            booking_type = random.choice(TYPES)
            departure = timezone.now() + timedelta(days=random.randint(-365, 365))
            order_line_data.append(
                OrderLine(
                    order_id = random.choice(order_ids),
                    destination = destination[0],
                    destination_iata = destination[1],
                    origin = origin[0],
                    origin_iata = origin[1],
                    type = booking_type,
                    departure = departure,
                    arrival = departure + timedelta(days=random.randint(0,1)),
                )
            )

        OrderLine.objects.using(db_alias).bulk_create(order_line_data)
    
    t2 = time.time() - t1
    print(f"time in seconds: {t2}\nTime in minutes: {t2/60}")


class Migration(migrations.Migration):

    dependencies = [
        ('migration_test', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_default_data),
    ]
# Generated by Django 3.0.4 on 2020-03-20 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0002_magazineloan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookloan',
            name='hand_in_date',
            field=models.DateTimeField(null=True),
        ),
    ]
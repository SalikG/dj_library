# Generated by Django 3.0.4 on 2020-03-27 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0003_auto_20200320_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magazineloan',
            name='hand_in_date',
            field=models.DateTimeField(null=True),
        ),
    ]

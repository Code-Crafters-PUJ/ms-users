# Generated by Django 5.0.3 on 2024-04-30 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Company", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="NIT",
            field=models.CharField(max_length=45, unique=True),
        ),
    ]

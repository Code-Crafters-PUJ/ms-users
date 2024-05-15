# Generated by Django 5.0.3 on 2024-05-13 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="company",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("NIT", models.CharField(max_length=45, unique=True)),
                ("businessArea", models.CharField(max_length=45)),
                ("employeeNumber", models.IntegerField()),
                ("businessName", models.CharField(max_length=45)),
                ("electronicBilling", models.CharField(max_length=45)),
                ("electronicPayroll", models.CharField(max_length=45)),
            ],
        ),
    ]

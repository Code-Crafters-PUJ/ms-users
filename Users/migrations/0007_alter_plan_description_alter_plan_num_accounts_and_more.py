# Generated by Django 5.0.3 on 2024-05-26 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Users", "0006_alter_plan_plan_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plan",
            name="description",
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name="plan",
            name="num_accounts",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="plan",
            name="num_services",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="plan",
            name="users",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

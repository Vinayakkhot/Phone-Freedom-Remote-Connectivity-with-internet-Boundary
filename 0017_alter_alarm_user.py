# Generated by Django 5.0.3 on 2024-05-05 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0016_alarm"),
    ]

    operations = [
        migrations.AlterField(
            model_name="alarm",
            name="user",
            field=models.CharField(max_length=100),
        ),
    ]

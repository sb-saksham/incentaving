# Generated by Django 3.0.2 on 2020-01-09 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conservationcount',
            name='is_apt',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 3.0.2 on 2020-01-11 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_auto_20200110_2308'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ['-posted_time']},
        ),
    ]
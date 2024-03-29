# Generated by Django 3.0.2 on 2020-01-15 04:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='action_images')),
                ('related_to_cause', models.CharField(choices=[('Pollution', 'Pollution'), ('Water', 'Water'), ('Plastic', 'Plastic'), ('Climate Change', 'Climate Change'), ('Land Degradation', 'Land Degradation'), ('Waste Management', 'Waste Management')], max_length=40)),
                ('description', models.CharField(max_length=400, unique=True)),
                ('solution', models.CharField(max_length=400)),
                ('required_cc', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ConservationCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.BigIntegerField(default=0)),
                ('is_apt', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conservation_count', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

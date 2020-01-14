from django.db import models
from django.contrib.auth import settings


User = settings.AUTH_USER_MODEL


cause_choices = [
    ('Pollution', 'Pollution'),
    ('Water', 'Water'),
    ('Plastic', 'Plastic'),
    ('Climate Change', 'Climate Change',),
    ('Land Degradation', 'Land Degradation'),
    ('Waste Management', 'Waste Management'),
]


class Action(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='action_images', null=True, blank=True)  # change upload_to=media/action_images/
    related_to_cause = models.CharField(max_length=40, choices=cause_choices)
    description = models.CharField(max_length=400, unique=True)
    solution = models.CharField(max_length=400)
    required_cc = models.IntegerField()

    def __str__(self):
        return self.name


class ConservationCount(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="conservation_count")
    score = models.BigIntegerField(default=0)
    is_apt = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

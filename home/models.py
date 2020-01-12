from django.db import models


class Card(models.Model):
    title = models.CharField(max_length=264)
    text = models.TextField()
    image = models.ImageField(upload_to='card_images')
    hashtag = models.CharField(max_length=264)

    def __str__(self):
        return self.title
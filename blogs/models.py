from accounts.models import User, EmailSubscription
from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings
from django.db import models
from utils import unique_slug_generator
from ckeditor.fields import RichTextField
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.shortcuts import reverse


class BlogQueryset(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True).order_by('-date_created')  # Blog.objects.all().featured()

    def search(self, query):
        lookups = (Q(title__icontains=query) | Q(content__icontains=query)) | Q(catchy_line__icontains=query) | Q(author_name__icontains=query)
        return self.filter(lookups).distinct()


class BlogManager(models.Manager):
    def get_queryset(self):
        return BlogQueryset(model=self.model, using=self._db)

    def search_for(self, query):
        qs = self.get_queryset().search(query=query)
        if qs.exists() != 0:
            return qs, True
        else:
            return self.get_queryset().featured(), False


class Blog(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=100)
    featured = models.BooleanField(default=False)
    content = RichTextField()
    tile_image = models.ImageField(upload_to='blog_tile')
    author_name = models.CharField(max_length=45)
    catchy_line = models.CharField(max_length=400)
    is_published = models.BooleanField(default=False)

    objects = BlogManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogs:blog_home', kwargs={'slug': self.slug})


def blog_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(blog_slug, sender=Blog)


def get_rl():
    recipient_list = [user.email for user in User.objects.all()]
    recipient_list = recipient_list + [es.email for es in EmailSubscription.objects.all()]
    recipient_list = list(dict.fromkeys(recipient_list))
    return recipient_list


def post_save_blog_send_notification(sender, instance, created, *args, **kwargs):
    if instance.is_published:
        if not settings.debug:
            host = 'https://' + settings.ALLOWED_HOSTS[1]
        else:
            host = 'http://'
        link = str(host) + str(instance.get_absolute_url())
        context = {'link': link, 'title': instance.title}
        recipient_list = get_rl()
        txt_message = get_template('blogs/new_blog/message.txt').render(context=context)
        subject = 'Read about the new blog on Incentaving.com ...'
        html_message = get_template('blogs/new_blog/message.html').render(context=context)
        sent_mail = send_mail(
            from_email='Incentaving <no-reply@Incentaving.com>',
            recipient_list=recipient_list,
            message=txt_message,
            html_message=html_message,
            subject=subject,
            fail_silently=False,
        )
        return sent_mail


post_save.connect(post_save_blog_send_notification, sender=Blog)


class Comments(models.Model):
    user = models.ManyToManyField(User, related_name='all_comments', blank=True)
    blog = models.ForeignKey(Blog, related_name='blog_comments', on_delete=models.CASCADE)
    content = RichTextField()
    posted_time = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ['-posted_time']

    def __str__(self):
        return str(self.blog.title)

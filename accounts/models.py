from datetime import timedelta
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone, safestring
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import pre_save, post_save
from utils import unique_key
from django.core.mail import send_mail
from django.template.loader import get_template


class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("User should have an Email!")
        if not password:
            raise ValueError("User should have a Valid Password!")
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
        )
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email=email,
            full_name=full_name,
            password=password,
            is_staff=True,
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, full_name=None):
        user = self.create_user(
            email=self.normalize_email(email),
            full_name=full_name,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=264, unique=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True) # change upload_to='media/profile_images/'
    full_name = models.CharField(max_length=264, null=True, blank=True)
    is_active = models.BooleanField(default=True)  # can login
    staff = models.BooleanField(default=False)  # is a staff
    admin = models.BooleanField(default=False)  # is a superuser
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'    # assign the email field as the username field
    # by default when declaring own user model USERNAME and password is required we can add extra required by
    REQUIRED_FIELDS = []  # [ 'field_name' ]

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        try:
            sn = self.full_name.split(' ')[0]
        except AttributeError:
            sn = self.full_name
        return sn

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff


class EmailActivationQueryset(models.query.QuerySet):
    def confirmable(self):
        now = timezone.now()
        start_range = now - timedelta(days=float(7))
        end_range = now
        return self.filter(
            activated=False,
            forced_expired=False,
        ).filter(
            timestamp__gt=start_range,
            timestamp__lte=end_range,
        )


class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQueryset(model=self.model, using=self._db)

    def email_exists(self, email):
        return self.get_queryset().filter(Q(email=email) | Q(user__email=email)).filter(activated=False)


class EmailActivation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    key = models.CharField(max_length=50, blank=True, null=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    expires = models.IntegerField(default=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable()
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            user = self.user
            user.is_active = True
            user.save()
            self.activated = True
            self.save()
            return True
        return False

    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                firstname = self.user.get_short_name()
                if not settings.DEBUG:
                    path = 'https://' + settings.ALLOWED_HOSTS[1]
                else:
                    path = 'http://127.0.0.1:8000'
                path = path + reverse("accounts:email-activation", kwargs={'key': self.key})
                context = {
                    'path': path,
                    'firstname': firstname,
                }
                verify_txt = get_template('registration/email/verify.txt').render(context)
                verify_html = get_template('registration/email/verify.html').render(context)
                sent_mail = send_mail(
                    subject='One-click Activation Email',
                    message=verify_txt,
                    from_email='Incentaving <no-reply@Incentaving.com>',
                    recipient_list=[self.email],
                    html_message=verify_html,
                    fail_silently=False,
                )
                return sent_mail


def pre_save_email_reciever(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key(instance)


pre_save.connect(pre_save_email_reciever, sender=EmailActivation)


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        obj.send_activation()


post_save.connect(post_save_user_receiver, sender=User)


class EmailSubscription(models.Model):
    full_name = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField()
    active = models.BooleanField(default=True, null=True, blank=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.email


def post_save_email_send(sender, instance, created, *args, **kwargs):
    if created:
        subject = 'Greetings From Incentaving.com...'
        context = {'firstname': instance.full_name}
        message_txt = get_template('subscription_templates/email_subscribed.txt').render(context=context)
        message_html = get_template('subscription_templates/email_subscribed.html').render(context=context)
        sent_mail = send_mail(
            subject=subject,
            message=message_txt,
            html_message=message_html,
            from_email='Incentaving <no-reply@Incentaving.com>',
            recipient_list=[instance.email],
            fail_silently=False,
        )
        return sent_mail


post_save.connect(post_save_email_send, sender=EmailSubscription)
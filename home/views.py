from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.core.mail import send_mail
from blogs.models import Blog


def home(request):
    return render(request, 'home/home.html')


def homepage(request):
    context = {}
    try:
        featured_blogs = Blog.objects.all().featured()[:6]
    except IndexError:
        featured_blogs = Blog.objects.all().featured()
    if featured_blogs.exists():
        context['feat_blogs'] = featured_blogs
    return render(request, 'home/homepage.html', context=context)


def coming_soon(request):
    return render(request, 'home/products/products.html')


@login_required
def contact(request):
    context = {
        'done': False,
    }
    if request.method == 'POST':
        data = request.POST
        subject = data.get('subject')
        user_name = data.get('user_name')
        subject = 'Sent by {name} for '.format(name=user_name) + str(subject)
        body = data.get('body')
        from_email = data.get('email', 'userContact@incentaving.com')
        if subject is not None and body is not None and email is not None:
            is_sent = send_mail(
                from_email=from_email,
                recipient_list=['help@incentaving.com'],
                fail_silently=False,
                subject=subject,
                message=body,
            )
            context['done'] = is_sent
            if is_sent:
                messages.success(request, mark_safe("You message has been sent successfully! Our team will contact you soon"))
                context['messages'] = messages.get_messages(request=request)
            return render(request, 'home/contact.html', context=context)
    return render(request, 'home/contact.html', context=context)


def about(request):
    return render(request, 'home/about.html')
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.safestring import mark_safe
from incentaving.mixins import RequestFormAttachMixin, NextUrlMixin
from . import forms
from django.views.generic.edit import FormMixin
from django.views.generic import CreateView, DetailView, View, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from .models import EmailSubscription, EmailActivation
from django.contrib import messages


User = settings.AUTH_USER_MODEL


class AccountsHome(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'
    context_object_name = 'account'

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        data = request.POST
        image = data.get('an_image')
        if image is not None:
            request.user.image = image
            request.user.save()
            return redirect('/')


class AccountsEmailActivation(FormMixin, View):
    success_url = '/user/login/'
    form_class = forms.ReactivateEmailForm
    key = None

    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, "Your account has been activated!")
                return HttpResponseRedirect(reverse('accounts:login'), {'messages': messages.get_messages(request)})
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    link = reverse("password-reset")
                    message = """Your email has already been activated. Do you want to <a href="{link}">reset your password ?</a>
                    """.format(link=link)
                    messages.success(request, mark_safe(message))
                    return HttpResponseRedirect(reverse('accounts:login'), {'messages': messages.get_messages(request)})
        context = {'form': self.get_form(), 'messages': messages.get_messages(request)}
        return render(request, 'accounts/email_activation.html', context=context)

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        email_act_obj = EmailActivation.objects.email_exists(email).first()
        user = email_act_obj.user
        new_obj = EmailActivation.objects.create(email=email, user=user)
        new_obj.send_activation()
        return super(AccountsEmailActivation, self).form_valid(form)

    def form_invalid(self, form):
        context = {'form': form, "key": self.key}
        return render(self.request, 'accounts/email_activation.html', context=context)

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class RegisterView(CreateView):
    form_class = forms.RegisterForm
    model = User
    template_name = 'accounts/signup.html'

    def get_success_url(self):
        url = '/user/login/'
        return url

    def form_valid(self, form):
        form.save()
        message = """You have been Signed Up! <strong>Please check your email for Activation Link</strong>"""
        messages.success(request=self.request, message=mark_safe(message))
        return HttpResponseRedirect('/user/login/', {'messages': messages.get_messages(self.request)})


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = forms.LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'
    default_next = '/'

    def form_valid(self, form):
        next_path = self.get_next_url()
        message = """You have been successfully <strong>Logged In</strong>"""
        messages.success(request=self.request, message=mark_safe(message))
        return HttpResponseRedirect(next_path, {'messages': messages.get_messages(self.request)})


def subscribe(request):
    if request.method == 'POST':
        news_form = request.POST
        email = news_form.get('email')
        full_name = news_form.get('fullName')
        try:
            fn, ln = full_name.split(' ')
            full_name = fn.title()+' '+ln.title()
        except AttributeError:
            pass
        email_news_object = EmailSubscription.objects.create(full_name=full_name, email=email)
        request.session['subscribed'] = True
        message_of = """<strong>You have been successfully subscribed to our newsletter</strong>"""
        messages.success(request, mark_safe(message_of))
        if request.is_ajax():
            return JsonResponse({'message': message_of})
        return HttpResponseRedirect('/', {'messages': messages.get_messages(request)})

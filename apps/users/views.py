from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.views.generic import TemplateView, UpdateView
from .forms import RegisterForm, ProfileUpdateForm
from .models import UserProfile
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth import login, logout


class UserRegistrationView(TemplateView, FormMixin):
    email_template = 'registration/activation_email.html'
    form_class = RegisterForm
    success_url = 'index'
    template_name = 'registration/user_creation.html'

    def post(self, request):
        form =self.get_form()
        if form.is_valid():
            email = form.cleaned_data['email']
            user = form.save(commit=False)
            user.is_active=False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string(self.email_template, {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'email': email
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, from_email='asharrahsa@mail.ru', to=[to_email])
            email.send()
            confirm_message = 'Check your email;'
            return render(request, self.template_name, {'message':confirm_message})
        return render(request, self.template_name, {'message': 'error', 'form':form})

    def get_object(self, queryset=None):
        pass

    def __str__(self):
        return UserProfile.objects.get(user_email=self)


class ActivationView(TemplateView):
    template_name = 'registration/activation_email.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        uidb64 = kwargs.get('uidb64', None)
        token = kwargs.get('token', None)
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user_profile = UserProfile.objects.get(pk=uid)
        except (TypeError,ValueError, OverflowError, UserProfile.DoesNotExist):
            user_profile = None
        if user_profile is not None and account_activation_token.check_token(user_profile, token):
            user_profile.is_active=True
            user_profile.save()
            login(request, user_profile)
            return redirect(reverse('index'))
        context['message'] = 'Activation url is wrong!'
        return self.render_to_response(context)


class IndexView(TemplateView):
    template_name = 'index.html'


class CabinetView(UpdateView, LoginRequiredMixin):
    model = UserProfile
    fields = ['email', 'username', 'image']
    template_name = 'registration/userprofile_form.html'

    def get_success_url(self):
        return reverse('cabinet', kwargs={'pk':self.object.id})

    def get_object(self):
        return self.request.user


class ProfileUpdateView(UpdateView):
    form_class = ProfileUpdateForm
    model = UserProfile
    success_url = reverse_lazy('cabinet')
    fields = ['user_email', 'username', 'password', 'image']


def logout(request):
    logout(request)
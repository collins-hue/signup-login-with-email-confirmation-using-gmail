from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model

from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str  # force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


def finalactivation(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('mainapp:login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('mainapp:login')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database  
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site  
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('mainapp/acc_active_email.html', {
                'user': user,
                'domain': localhost.com,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'mainapp/register.html', {'form': form})


def login_request(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password,
                                backend='django.contrib.auth.backends.ModelBackend')
            if user is not None:
                login(request, user)
                return redirect('mainapp:home')
            else:
                messages.error(request, 'Wrong Password or Username')
        else:
            messages.error(request, 'Wrong Password or Username')
    login_form = AuthenticationForm()
    return render(request, template_name='mainapp/login.html', context={'login_form': login_form})


# noinspection PyUnusedLocal
@login_required(login_url='mainapp:login')
def home(request):
    return HttpResponse('Thank you <body color:green >Have you Read the Nicomachean Ethics. <br>It is one of '
                        'Aristotle''s greatest works.</body>')

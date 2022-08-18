from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.urls import reverse

from .models import Token


def send_login_email(request):
    if request.method == 'POST':
        email = request.POST['email']
        token = Token.objects.create(email=email)

        url = request.build_absolute_uri(
            f'{reverse("login")}?token={token.uid}')
        message_body = f'Use this link to log in:\n\n{url}'

        send_mail(
            'Your login link for Lists-tdd',
            message_body,
            'noreply@liststdd',
            [email]
        )
        messages.success(
            request,
            'Check your email, we`ve sent you a link you can use to log in.'
        )

        return redirect('/')


def login(request):
    if request.method == 'GET':
        user = auth.authenticate(uid=request.GET.get('token'))
        if user:
            auth.login(request, user)
        return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('/')

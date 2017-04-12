from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from account.models import UserOtherDetails
from registration.forms import UserForm


class UserFormView(View):
    form_class = UserForm
    template_name = 'registration/registration_form.html'

    def get(self, request):
        return render(request, 'registration/register.html')

    # handle the form posting
    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email_address = request.POST['email_address']
        password = request.POST['password']

        u = User()
        u.first_name = first_name
        u.last_name = last_name
        u.username = username
        u.email = email_address
        u.set_password(password)
        u.save()

        u = authenticate(username=username, password=password)

        if u is not None:
            login(request, u)
            return redirect('/')
        else:
            return render(request, 'registration/register.html', {'error': 'An error has occured'})

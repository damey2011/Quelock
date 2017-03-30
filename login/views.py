from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from login.forms import LoginForm


class LoginView(View):

    form_class = LoginForm
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            print('42')
            login(request, user)
            return redirect('/')
        return render(request, self.template_name, {'form': self.form_class, 'account_active': 'active'})

from django.contrib.auth import authenticate, login
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
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            # Create a user other details
            other_details = UserOtherDetails()
            other_details.user = user
            other_details.save()
            # return user object if the details are then valid
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
        return render(request, self.template_name, {'form': form})




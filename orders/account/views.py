from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django import forms
from account.forms import LoginForm, UserRegistrationForm


# class GroupRegistrationForm(forms.ModelForm):
#     groups = forms.ModelChoiceField(queryset=Group.objects.all())
#


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])

            new_user.save()

            # specifically assign many-to-many fields after saving object
            new_user.groups.add(user_form.cleaned_data['groups'])

            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})





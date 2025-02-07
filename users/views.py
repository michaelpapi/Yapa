from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import (
    LoginForm, 
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm,
)
from .models import Profile


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password1'],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render (request, 'account/login.html', {'form': form})




def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but don't save yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password1'])
            # Save the User object
            new_user.save()
            # Creating a user profile
            Profile.objects.create(user=new_user)
            messages.success(
                request,
                'New User registered'
            )
            return render(request, 'account/register_done.html', {'new_user': new_user})
        else:
            print(user_form.errors)

    else:
        user_form = UserRegistrationForm()  # Ensure a form instance exists for GET requests

    return render(request, 'account/register.html', {'user_form': user_form})  # Always return a response


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request,
                'Profile updated successfully'
            )
        else:
            messages.error(request, 'Error updating your profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        'account/edit.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )

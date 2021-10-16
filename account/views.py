from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import CustomUserForm
from user.forms import *
from django.contrib.auth import login, logout


# Create your views here.


def account_login(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("admin panel "))
        else:
            return redirect(reverse("person panel "))

    context = {}
    if request.method == 'POST':
        if user != None:
            login(request, user)
            if user.user_type == '1':
                return redirect(reverse("admin panel"))
            else:
                return redirect(reverse("voter panel"))
        else:
            messages.error(request, "Invalid details")
            return redirect("/")

    return render(request, "login.html", context)


def account_register(request):
    userForm = CustomUserForm(request.POST or None)
    personForm = PersonForm(request.POST or None)
    context = {
        'form1': userForm,
        'form2': personForm
    }
    if request.method == 'POST':
        if userForm.is_valid() and personForm.is_valid():
            user = userForm.save(commit=False)
            person = personForm.save(commit=False)
            person.admin = user
            user.save()
            person.save()
            messages.success(request, "Account created. You can login now!")
            return redirect(reverse('account_login'))
        else:
            messages.error(request, "Provided data failed validation")
            # return account_login(request)
    return render(request, "register.html", context)


def account_logout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        messages.success(request, "Thank you for visiting us!")
    else:
        messages.error(
            request, "You need to be logged in to perform this action")

    return redirect(reverse("account_login"))
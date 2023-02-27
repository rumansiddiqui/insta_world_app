from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
def sign_up(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first-name"]
        last_name = request.POST["last-name"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        my_user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                           last_name=last_name, confirm_password=confirm_password)
        my_user.save()
        return redirect('signin')
    return render(request, "sign-up.html")


def sign_in(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "wrong information")
            return render(request, "sign-in.html")

    return render(request, "sign-in.html")

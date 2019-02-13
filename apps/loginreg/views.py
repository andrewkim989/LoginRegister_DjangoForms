from django.shortcuts import render, redirect
from .forms import Register, Login
from django.contrib import messages
import bcrypt

from .models import User

def index(request):
    if "login" not in request.session:
        request.session["login"] = "logout"
    if request.session["login"] == "login":
        return redirect("/home")

    registerform = Register()
    loginform = Login()
    context = {
        "register": registerform,
        "login": loginform
    }

    return render(request, "loginreg.html", context)

def registerUser(request):
    if request.method == "POST":
        form = Register(request.POST)
        errors = form.errors.items()

        if not form.is_valid():
            for key, value in errors:
                messages.error(request, value, extra_tags = "register")
            return redirect("/")
        else:
            request.session["login"] = "login"
            p = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())

            user = User.objects.create(name = request.POST["name"],
            email = request.POST["email"], password = p)

            request.session["id"] = user.id
            messages.success(request, "You have successfully registered!", extra_tags = "register")
        
            return redirect("/home")

def loginUser(request):
    if request.method == "POST":
        form = Login(request.POST)
        errors = form.errors.items()

        if not form.is_valid():
            for key, value in errors:
                messages.error(request, value, extra_tags = "login")
            return redirect("/")
        else:
            request.session["login"] = "login"
            user = User.objects.filter(email = request.POST["email"])[0]
            request.session["id"] = user.id

            messages.success(request, "You are logged in!", extra_tags = "login")

            return redirect("/home")

def home(request):
    if request.session["login"] == "logout":
        return redirect("/")
    else:
        user = User.objects.get(id = request.session["id"])
        info = {
            "u": user
        }
        return render(request, "home.html", info)

def logout(request):
    request.session["login"] = "logout"
    return redirect("/")

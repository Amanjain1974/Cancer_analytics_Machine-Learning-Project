from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

def register(request):
    form=UserCreationForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        user=form.save()
        login(request,user)
        return redirect("dashboard")
    return render(request,"authentication/register.html",{"form":form})

def user_login(request):
    form=AuthenticationForm(request,data=request.POST or None)
    if request.method=="POST" and form.is_valid():
        login(request,form.get_user())
        return redirect("dashboard")
    return render(request,"authentication/login.html",{"form":form})

def user_logout(request):
    logout(request)
    return redirect("home")

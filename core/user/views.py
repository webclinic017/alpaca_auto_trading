from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/api/docs/')
    return render(request, 'login.html')

def login_authenticate_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/api/docs/')
    else:
        return HttpResponseRedirect('/login/')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')

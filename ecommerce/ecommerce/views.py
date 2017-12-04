from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import LoginForm 
from django.contrib.auth import authenticate, login


def login_page(request):
	form = LoginForm(request.POST or None )
	context = {"form":form}
	print(request.user.is_authenticated())

	if form.is_valid():
		print(form.cleaned_data)
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(request,username=username,password=password)
		print(user)

		if user is not None:
			login(request,user)
			return redirect('/login')
		else:
			print('error')
	
	return render(request,'auth/login.html',context)

def register_page(request):
	form = LoginForm(request.POST or None )
	if form.is_valid():
		print(form.cleaned_data)
	context = {"form":form}
	return render(request,'auth/register.html',context)

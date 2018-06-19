from django.contrib.auth import (
		authenticate,
		get_user_model,
		login,
		logout
	)
from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegisterForm

# Create your views here.


def login_view(request):
	title = "Login"
	next = request.GET.get('next')
	form = UserLoginForm(request.POST or None)

	if form.is_valid():
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		login(request, user)
		print(next)
		if next:
			return redirect(next)
		return redirect('/posts')
	context = {
		'form': form,
		'title': title,
		'next': next,
	}
	return render(request, 'form.html', context)


def register_view(request):
	title = "Register"
	next = request.GET.get('next')
	form = UserRegisterForm(request.POST or None)

	print(request.user.is_authenticated)

	if form.is_valid():
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		user = form.save(commit=False)
		user.set_password(password)
		user.save()
		new_user = authenticate(username=username, password=password)
		login(request, new_user)
		if next:
			return redirect(next)
		return redirect('/posts')

	context = {
		'form': form,
		'title': title,
		'next': next,
	}
	return render(request, 'form.html', context)

def logout_view(request):
	logout(request)
	return redirect('/posts')
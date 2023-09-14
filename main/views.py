from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import signUpForm
from account.models import Account

def home(request):
    
    # Check to see if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return redirect('home')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('home')
	else:
		return render(request, 'home.html', {})
	
def login_user(request):
	return render(request, 'login.html')


def logout_user(request):
	logout(request)
	messages.success(request, 'You have been loggout.....')
	return redirect('home')

def register_user(request):
	if request.method == 'POST':
		form = signUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user_profile = Account.objects.create(
				user=user,
				ph_number = form.cleaned_data['ph_number'],
				address = form.cleaned_data['address'],
				user_type = form.cleaned_data['user_type'],
			)
			user_profile.save()
			authenticate(username=user.username, password = user.password)
			login(request, user)
			messages.success(request, 'You have successfully registered...')
			return redirect('home')
	else:
		form = signUpForm()
		return render(request, 'register.html', {'form':form})
	return render(request, 'register.html', {'form':form})


from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import signUpForm, userEditForm
from account.models import Account
from django.contrib.auth.models import User
from django.db.models import F
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.urls import reverse

def home(request):
	
    
	if request.method == 'POST':
		email = request.POST['email']
		
		password = request.POST['password']

		# Validate the email 
		email_validator = EmailValidator()
		try:
			email_validator(email)
		except ValidationError:
			messages.error(request, "Please enter a valid email address.")
			return redirect('home')
		try:
            # Attempt to retrieve the user by email (case-insensitive)
			user = User.objects.get(email__iexact=email)
		except User.DoesNotExist:
			messages.error(request, "User with this email does not exist.")
			return redirect('home')
		# Authenticate
		user = authenticate(request, username=user.username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return redirect('home')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('home')
	else:
		staffs_and_details = User.objects.select_related('account')
		context = {'staffs_and_details': staffs_and_details}
		return render(request, 'home.html', context)
	
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

def staffDashboard(request):
	return render(request, 'staffDashboard.html',{
		'staff' : User.objects.all()
	})


def view_staff(request, id):
  return HttpResponseRedirect(reverse('home'))

def edit(request, id):
	
    staff = User.objects.get(pk=id)

    if request.method == 'POST':
        form = userEditForm(request.POST, instance=staff)
        if form.is_valid():
            user = form.save()

            user_profile, created = Account.objects.get_or_create(user=user)
            user_profile.ph_number = form.cleaned_data['ph_number']
            user_profile.address = form.cleaned_data['address']
            user_profile.user_type = form.cleaned_data['user_type']
            user_profile.save()

            # Authenticate and log in the user
            authenticate(username=user.username, password=user.password)
            login(request, user)

            messages.success(request, 'You have successfully edited...')
            return redirect('home')
    else:
        form = userEditForm(instance=staff)

    return render(request, 'staffEdit.html', {'form': form})

def delete(request, id):
  if request.method == 'POST':
    staff = User.objects.get(pk=id)
    staff.delete()
  messages.success(request, staff.first_name+" has been deleted")
  return HttpResponseRedirect(reverse('home'))
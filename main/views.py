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
from django.contrib.auth.decorators import login_required

	
def login_user(request):
	if request.method == 'POST':
		email = request.POST['email']
		
		password = request.POST['password']

		# Validate the email 
		email_validator = EmailValidator()
		try:
			email_validator(email)
		except ValidationError:
			messages.error(request, "Please enter a valid email address.")
			return redirect('login.html')
		try:
            # Attempt to retrieve the user by email (case-insensitive)
			user = User.objects.get(email__iexact=email)
		except User.DoesNotExist:
			messages.error(request, "User with this email does not exist.")
			return redirect('login_page')
		# Authenticate
		user = authenticate(request, username=user.username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return redirect('staff_list')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('login_page')
	else:
		staffs = User.objects.select_related('account')
		admin_and_teacher_staffs = staffs.filter(account__user_type__in=['admin', 'teacher'])
		context = {'staffs': admin_and_teacher_staffs}
		return render(request, 'staff_list_display.html', context)



def staff_list_page(request):
    if request.user.is_authenticated:
        staffs = User.objects.select_related('account')
        admin_and_teacher_staffs = staffs.filter(account__user_type__in=['admin', 'teacher'])
        context = {'staffs': admin_and_teacher_staffs}
        return render(request, 'staff_list_display.html', context)
    else:
        # Redirect to the login page or display an error message
        return redirect('login')
	
def stu_list_page(request):
    if request.user.is_authenticated:
        students = User.objects.select_related('account')
        student_details = students.filter(account__user_type__in=['student'])
        context = {'students': student_details}
        return render(request, 'students_list_display.html', context)
    else:
        # Redirect to the login page or display an error message
        return redirect('login')


def login_page(request):
	return render(request, 'login.html')

def land_page(request):
    return render(request, 'landpage.html')


def logout_user(request):
	logout(request)
	messages.success(request, 'You have been loggout.....')
	return redirect('land_page')

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
			
			messages.success(request, 'You have successfully registered...Please login with your credentials...')
			return redirect('login_page')
	else:
		form = signUpForm()
		return render(request, 'register.html', {'form':form})
	return render(request, 'register.html', {'form':form})



def view_staff(request, id):
  return HttpResponseRedirect(reverse('land_page'))

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

            messages.success(request, 'You have successfully edited...')

            # Determine the user type and redirect accordingly
            if user_profile.user_type in ['staff', 'admin']:
                return redirect('staff_list')
            elif user_profile.user_type == 'student':
                return redirect('stu_list')
    else:
        form = userEditForm(instance=staff)

    return render(request, 'staffEdit.html', {'form': form})

def delete(request, id):
    if request.method == 'POST':
        staff = User.objects.get(pk=id)
        user_profile = Account.objects.get(user=staff)
        staff.delete()

        messages.success(request, staff.first_name + " has been deleted")

        # Determine the user type and redirect accordingly
        if user_profile.user_type in ['staff', 'admin']:
            return redirect('staff_list')
        elif user_profile.user_type == 'student':
            return redirect('stu_list')

    return HttpResponseRedirect(reverse('staff_list'))
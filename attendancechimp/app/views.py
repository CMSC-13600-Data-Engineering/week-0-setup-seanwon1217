from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django import forms
from django.contrib import messages
from .forms import SignUpForm, CourseForm
from .models import courses

instructor_group, created = Group.objects.get_or_create(name='Instructor')
student_group, created = Group.objects.get_or_create(name='Student')

def index(request):
    classdict = {'class1':'CMSC136'}
    return render(request, 'app/index.html', classdict)

def new(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Check if the email is already in use
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                # Return error state - email already in use
                return render(request, 'new.html', {'form': form, 'error': 'Email already in use'})

            # Create a new user object
            user = form.save()

            # Add the user to the appropriate group
            user_type = form.cleaned_data.get('user_type')
            if user_type == 'instructor':
                group = Group.objects.get(name='Instructor')
            else:
                group = Group.objects.get(name='Student')
            group.user_set.add(user)

            # Log the user in and redirect to success page
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            success_msg = 'User account created successfully.'
            return render(request, 'app/success.html', {'success_msg': success_msg})
    else:
        form = SignUpForm()
    return render(request, 'new.html', {'form': form})

def success(request):
    return render(request, 'app/success.html')

def create(request):
    classdict = {'class1':'CMSC136'}
    if request.user.groups.filter(name='Instructor').exists():
        if request.method == 'POST':
            form = CourseForm(request.POST)
            if form.is_valid():
                course = form.save(commit=False)
                #There is no identical course in the database.
                courseid = form.cleaned_data.get('courseid')
                if courses.objects.filter(courseid=courseid).exists():
                    return render(request, 'create.html', {'form': form, 'error': 'This course already exists.'})
                    #An instructor is not teaching another course at the same time.
                    #The end date is before the start date.
                course.save()
                #success_msg = 'Course created successfully.'
                #return render(request, 'app/success.html', {'success_msg': success_msg})
                return HttpResponseRedirect('success.html')
        else:
            form = CourseForm()
            return render(request, 'create.html', {'form': form})
        #return render(request, 'app/create.html', classdict)
    else:
        form = CourseForm()
        #return redirect('templates/registration/login.html')
    return render(request, 'create.html', {'form': form})

def create_test(request):
    if not request.user.is_instructor:
        return redirect('templates/registration/login.html')
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            # Check if there is an identical course in the database
            if Course.objects.filter(name=form.cleaned_data['name'], start_date=form.cleaned_data['start_date'], end_date=form.cleaned_data['end_date'], meeting_time=form.cleaned_data['meeting_time']).exists():
                messages.error(request, 'A course with the same name, start date, end date, and meeting time already exists.')
            # Check if the instructor is already teaching at this time
            elif Course.objects.filter(instructor=request.user, start_date__lte=form.cleaned_data['end_date'], end_date__gte=form.cleaned_data['start_date']).exists():
                messages.error(request, 'You are already teaching another course at this time.')
            # Check if end date is before start date
            elif form.cleaned_data['end_date'] < form.cleaned_data['start_date']:
                messages.error(request, 'End date cannot be before start date.')
            else:
                # Create a new course object and save it to the database
                course = form.save(commit=False)
                course.instructor = request.user
                course.save()
                messages.success(request, 'Course created successfully.')
                return redirect('success', course.code)
    else:
        form = CourseForm()
    #return render(request, 'create_course.html', {'form': form})


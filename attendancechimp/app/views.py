from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django import forms
from .forms import SignUpForm, CourseForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import user, Course
from django.urls import reverse


instructor_group, created = Group.objects.get_or_create(name='Instructor')
student_group, created = Group.objects.get_or_create(name='Student')

@login_required(login_url='/accounts/login/')
def join(request):
    if request.user.is_authenticated and request.user.groups.filter(name='Student').exists():
        #join course
        return redirect(reverse('login'))
def attendance(request):
    if request.user.is_authenticated and request.user.groups.filter(name='Instructor').exists():
        #display qr
        return redirect(reverse('login'))
def upload(request):
    if request.user.is_authenticated and request.user.groups.filter(name='Student').exists():
        #upload qr
        return redirect(reverse('login'))
def course_success(request):
    return render(request, 'app/course_success.html')
def course_successs(request, code):
    course = Course.objects.get(code=code)
    student_url = reverse('join') + '?course_id=' + str(course.id)
    instructor_url = reverse('attendance') + '?course_id=' + str(course.id)
    upload_url = reverse('upload') + '?course_id=' + str(course.id)

    return render(request, 'app/success.html',
                  {'course': course, 'student_url': student_url, 'instructor_url': instructor_url, 'upload_url': upload_url})
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

@login_required(login_url='/accounts/login/')

@login_required(login_url='/accounts/login/')
def created(request):
    classdict = {'class1': 'CMSC136'}
    
    if request.user.is_authenticated and request.user.groups.filter(name='Instructor').exists():
        return render(request, 'app/create.html', classdict)
    else:
        return redirect(reverse('login'))

@login_required(login_url='/accounts/login/')
def create(request):
    if request.user.is_authenticated and request.user.groups.filter(name='Instructor').exists():
        if request.method == 'POST':
            form = CourseForm(request.POST)
            if form.is_valid():
                course = form.save(commit=False)
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                start_time = form.cleaned_data['class_start_time']
                end_time = form.cleaned_data['class_end_time']
                meeting_days = form.cleaned_data['meeting_days']
                courseid = form.cleaned_data.get('courseid')
                #if Course.objects.filter(courseid=courseid).exists():
                    #messages.error(request, 'This course already exists.')
                    #return render(request, 'app/create.html', {'form': form})
                course.instructor = request.user
                course.save()
                messages.success(request, 'Course created successfully.')
            return render(request, 'app/course_success.html', {
                'course_code': course.courseid})
        else:
            form = CourseForm()
            return render(request, 'app/create.html', {'form': form})
    else:
        return redirect(reverse('login'))

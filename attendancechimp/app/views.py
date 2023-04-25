from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django import forms
from .forms import SignUpForm, CourseForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import user, Course, in_course, Attendance
from django.urls import reverse


instructor_group, created = Group.objects.get_or_create(name='Instructor')
student_group, created = Group.objects.get_or_create(name='Student')
@login_required(login_url='/accounts/login/')

#the button doesnt work yet
def join(request):
    course_code = request.GET.get('course_id', None) or request.POST.get('course_id', None)
    course = get_object_or_404(Course, course_id=course_code)
    if not course_code:
        return HttpResponse("Course id not found")
    try:
        course = Course.objects.get(course_id=course_code)
    except Course.DoesNotExist:
        return redirect(reverse('index'))
    if request.user.is_authenticated and request.user.groups.filter(name='Student').exists():
        student = request.user
        if not student.is_enrolled_in_course(course):
            if request.method == 'POST':
                if student.is_enrolled_in_course_at_same_time(course):
                    return HttpResponse("You are already enrolled in a course meeting at the same time.")
                course.students.add(student)
                course.save()
                return render(request, 'app/course_success.html', {'course_id': course.course_id, 'coursename': course.coursename})
            else:
                return render(request, 'app/join.html', {'course': course})
        else:
            return HttpResponse("You are already enrolled in this course.")
    else:
        return redirect(reverse('login'))

    
def attendance(request):
    if request.user.is_authenticated and request.user.groups.filter(name='Instructor').exists():
        #display qr
        return redirect(reverse('login'))
def upload(request):
    if request.user.is_authenticated and request.user.groups.filter(name='Student').exists():
        #upload qr
        return redirect(reverse('login'))

@login_required(login_url='/accounts/login/')
def course_success(request, course_id):
    courses = Course.objects.filter(course_id=course_id)
    if not courses:
        return redirect(reverse('login'))
    else:
        course = courses.first()
        student_url = reverse('join') + '?course_id=' + str(course.course_id)
        instructor_url = reverse('attendance') + '?course_id=' + str(course.course_id)
        upload_url = reverse('upload') + '?course_id=' + str(course.course_id)
        return render(request, 'app/course_success.html',
                  {'course': course, 'student_url': student_url, 'instructor_url': instructor_url, 'upload_url': upload_url,
                   'coursename': course.coursename, 'course_id': course.course_id})


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


def course_list(request):
    courses = Course.objects.all() # get all courses
    return render(request, 'app/course_list.html', {'courses': courses})


@login_required(login_url='/accounts/login/')
def create(request):
    if request.user.is_authenticated and request.user.groups.filter(name='Instructor').exists():
        if request.method == 'POST':
            form = CourseForm(request.POST)
            if form.is_valid():
                course = form.save(commit=False)
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                class_start_time = form.cleaned_data['class_start_time']
                coursename = form.cleaned_data['coursename']
                class_end_time = form.cleaned_data['class_end_time']
                meeting_days = form.cleaned_data['meeting_days']
                day_of_week = form.cleaned_data['day_of_week']
                course_id = form.cleaned_data.get('course_id')
                instructor = request.user
                
                # Check for identical course ID
                if Course.objects.filter(course_id=course_id).exists():
                    messages.error(request, 'This course already exists.')
                    return render(request, 'app/create.html', {'form': form})
                
                if in_course.objects.filter(course_id__day_of_week=day_of_week, course_id__class_start_time__lt=class_end_time, course_id__class_end_time__gt=class_start_time).exists():
                    messages.error(request, 'The instructor is already teaching a course at this time.')
                    return render(request, 'create_course.html', {'form': form})
            
                
                # Check that end date comes after start date
                if end_date < start_date:
                    messages.error(request, 'End date cannot precede start date.')
                    return render(request, 'app/create.html', {'form': form})
                
                # Check for schedule conflicts
                all_courses = Course.objects.filter(instructor=request.user)
                for c in all_courses:
                    if c.day_of_week == course.day_of_week and \
                       (c.start_date < course.end_date and c.end_date > course.start_date) and \
                       (c.class_start_time < course.class_end_time and c.class_end_time > course.class_start_time):
                        messages.error(request, f'Schedule conflict with {c.coursename}.')
                        return render(request, 'app/create.html', {'form': form})
                
                course.instructor = request.user
                course.save
                messages.success(request, 'Course created successfully.')
                return redirect(reverse('course_success', args=[course.course_id]))
                #return redirect('/app/course_success', course_id=new_course.id)
                #return render(request, 'app/success')
        else:
            form = CourseForm()
        return render(request, 'app/create.html', {'form': form})
    else:
        return redirect(reverse('login'))

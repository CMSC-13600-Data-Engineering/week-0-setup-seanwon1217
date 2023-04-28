from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
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
from datetime import datetime
import uuid

instructor_group, created = Group.objects.get_or_create(name='Instructor')
student_group, created = Group.objects.get_or_create(name='Student')
@login_required(login_url='/accounts/login/')

def join(request):
    user = request.user
    course_id = request.GET.get('course_id') or request.POST.get('course_id')
    if not course_id:
        return HttpResponse("Course id not found")

    try:
        course_id = Course.objects.get(course_id=course_id)
    except Course.DoesNotExist:
        return redirect(reverse('index'))

    if request.user.is_authenticated and request.user.groups.filter(name='Student').exists():
        student = user

        if request.method == 'POST':
            for enrolled_course in in_course.objects.filter(student=student):
                if set(enrolled_course.course_id.meeting_days) & set(course_id.meeting_days) and \
                   enrolled_course.course_id.class_start_time < course_id.class_end_time and \
                   enrolled_course.course_id.class_end_time > course_id.class_start_time:
                    return HttpResponse(f"You cannot join this course because it conflicts with another course you are enrolled in. ({enrolled_course.course_id.coursename})")

            in_course.objects.create(course_id=course_id, student=student)
            success_msg = 'You have successfully joined the course'
            messages.success(request, f"You have successfully joined {course_id.coursename}.")
            return render(request, 'app/success.html', {'success_msg': success_msg})
        else:
            return render(request, 'app/join.html', {'coursename': course_id.coursename, 'course_id': course_id.course_id})
    else:
        return redirect(reverse('login'))

@login_required(login_url='/accounts/login/')  
def attendance(request):
    if request.user.is_authenticated and request.user.groups.filter(name='Instructor').exists():
        course_instructor = request.user
        course_id = request.GET.get('course_id', None)
        course = Course.objects.get(course_id=course_id)
     
        if course_instructor != course.instructor:
            return HttpResponseNotFound("You are not the instructor of this course.") 

        class_code = uuid.uuid4()
        new_attendance = Attendance(class_code=class_code, course_id=course, time=datetime.now())
        new_attendance.save()   
             
        return render(request, 'app/QRCode.html', {'class_code':class_code})
    else:
        return redirect(reverse('login'))

def upload(request):
    if request.user.is_authenticated and request.user.groups.filter(name='Student').exists():
        # upload qr
        return redirect(reverse('login'))
    else:
        return redirect(reverse('login'))

def upload(request):
    if request.user.is_authenticated and request.user.groups.filter(name='Student').exists():
        #upload qr
        return redirect(reverse('login'))

@login_required(login_url='/accounts/login/')
def course_success(request, course_id):
    if not request.user.is_authenticated:
        return redirect(reverse('create'))
    
    courses = Course.objects.filter(course_id=course_id)
    if not courses:
        return redirect(reverse('create'))
    
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
def created(request):
    classdict = {'class1': 'CMSC136'}

    if request.user.is_authenticated and request.user.groups.filter(name='Instructor').exists():
        return render(request, 'app/create.html', classdict)
    else:
        return redirect(reverse('login'))

def student_list(request):
    in_courses = in_course.objects.all()
    return render(request, 'app/student_list.html', {'in_courses': in_courses})

def course_list(request):
    courses = Course.objects.all() # get all courses
    course_list = []
    for course in courses:
        student_url = reverse('join') + '?course_id=' + str(course.course_id)
        instructor_url = reverse('attendance') + '?course_id=' + str(course.course_id)
        student_list_url = reverse('student_list') + '?course_id=' + str(course.course_id)
        upload_url = reverse('upload') + '?course_id=' + str(course.course_id)
        course_dict = {'course': course, 'student_url': student_url, 'instructor_url': instructor_url, 'student_list_url': student_list_url, 'upload_url': upload_url,
                       'coursename': course.coursename, 'course_id': course.course_id, 'instructor': course.instructor,
                       'day_of_week': course.day_of_week, 'students': course.students, 'class_start_time': course.class_start_time,
                       'class_end_time': course.class_end_time, 'meeting_days' : course.meeting_days,}
        course_list.append(course_dict)
    return render(request, 'app/course_list.html', {'courses': course_list})


##def course_list(request):
##    courses = Course.objects.all() # get all courses
##    courses = Course.objects.filter(course_id=course_id)
##    student_url = reverse('join') + '?course_id=' + str(course.course_id)
##    instructor_url = reverse('attendance') + '?course_id=' + str(course.course_id)
##    upload_url = reverse('upload') + '?course_id=' + str(course.course_id)
##    return render(request, 'app/course_list.html',
##                  {'courses': courses'course': course, 'student_url': student_url, 'instructor_url': instructor_url, 'upload_url': upload_url,
##                   'coursename': course.coursename, 'course_id': course.course_id})


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
                class_end_time = form.cleaned_data['class_end_time']
                day_of_week = form.cleaned_data['day_of_week']
                courseid = form.cleaned_data.get('course_id')
                course_instructor = request.user
                
                # Check for identical course ID
                query1 = Course.objects.filter(course_id=courseid)
                if query1.exists():
                    messages.error(request, 'This course already exists.')
                    return render(request, 'app/create.html', {'form': form})
                
                # Check for identical course ID during the same time
                #query1 = Course.objects.filter(course_id=courseid, start_date__lte=course.end_date, end_date__gte=course.start_date, class_start_time = class_start_time, class_end_time = class_end_time, day_of_week = day_of_week) or Course.objects.filter(course_id=courseid, end_date__gte=course.start_date, start_date__lte=course.end_date, class_start_time = class_start_time, class_end_time = class_end_time, day_of_week = day_of_week)
                #if query1.exists():
                    #messages.error(request, 'This course already exists.')
                    #return render(request, 'app/create.html', {'form': form})
                
                # Check for instructor schedule conflict
                query2 = Course.objects.filter(instructor = course_instructor)
                query2_1 = query2.filter(class_start_time__lte=course.class_end_time, class_end_time__gte=course.class_start_time) | query2.filter(class_end_time__gte=course.class_start_time, class_start_time__lte=course.class_end_time)
                query2_2 = query2_1.filter(day_of_week = day_of_week, start_date__lte=course.end_date, end_date__gte=course.start_date) | query2_1.filter(day_of_week = day_of_week, end_date__gte=course.start_date, start_date__lte=course.end_date)
                if query2_2.exists():
                    messages.error(request, 'You are already teaching a course at this time.')
                    return render(request, 'app/create.html', {'form': form})
            
                # Check that end date comes after start date
                if end_date < start_date:
                    messages.error(request, 'End date must be after start date.')
                    return render(request, 'app/create.html', {'form': form})
                
                # Check that end time comes after start time
                if class_end_time < class_start_time:
                    messages.error(request, 'End time must be after start time.')
                    return render(request, 'app/create.html', {'form': form})
               
                course.instructor = request.user
                course.save()
                #messages.success(request, 'Course created successfully.')
                success_msg = 'User account created successfully.'
                student_url = reverse('join') + '?course_id=' + str(course.course_id)
                instructor_url = reverse('attendance') + '?course_id=' + str(course.course_id)
                upload_url = reverse('upload') + '?course_id=' + str(course.course_id)
                return render(request, 'app/course_success.html', {'success_msg': success_msg, 'course': course, 'student_url': student_url, 'instructor_url': instructor_url, 'upload_url': upload_url,
                   'coursename': course.coursename, 'course_id': course.course_id})
        else:
            form = CourseForm()
        return render(request, 'app/create.html', {'form': form})
    else:
        return redirect(reverse('login'))

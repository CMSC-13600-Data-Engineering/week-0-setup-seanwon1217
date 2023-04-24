from django.db import models

# Create your models here.
# There will be two classes of users: students and instructorss.
# Both students and instructors should be Django users and
# should be able to login through /accounts/login

# Instructor can create courses at /app/create, which should open a form that creates a course in
# the database. For simplicity, courses have only a single instructor, but instructors
# can teach multiple courses. After creation, the page should generate three unique URLS tied to the course:
# /app/join?course_id=xyz ==> A logged in student can join the course
# /app/attendance?course_id=xyz ==> A logged in instructor can display a QR code
# /app/upload?course_id=xyz ==> A logged in student can upload a picture of the QR code


## models.py creates a catalog of users, courses, qrCodes per course, and
## of people within each course. The in_course class refers to users and courses
## to list who is enrolled or teaching each course. The qrCode class contains a
## list of the qrCodes generated for each class and userid.

# the class user creates a table with each user's name and assigns them an ID
class user(models.Model):
    username = models.CharField(max_length=256, null=False)
    userid = models.AutoField(primary_key=True)
    is_instructor = models.BooleanField()

# the class courses creates a table of courses
days_of_week = [('Monday','Monday'),('Tuesday','Tuesday'),('Wednesday','Wednesday'),('Thursday','Thursday'),('Friday','Friday'),('Saturday','Saturday'),('Sunday','Sunday')]
class courses(models.Model):
    coursename = models.CharField(max_length=256, null=False)
    courseid = models.IntegerField(unique=True, primary_key=True)
    start_date = models.DateField()#verbose_name='Start date (MM/DD/YY)')
    end_date = models.DateField()#verbose_name='End date (MM/DD/YY)')
    class_start_time = models.TimeField(verbose_name='Class start time (e.g. 14:00)', error_messages={'null':'Please enter a start time.'})
    class_end_time = models.TimeField(verbose_name='Class end time (e.g. 15:20)', error_messages={'null':'Please enter an end time.'})
    day_of_week = models.CharField(max_length = 255, choices = days_of_week)

# the class in_course creates a table with course's and the people in the course. It then
# says whether the user is an instructor
class in_course(models.Model):
    courseid = models.ForeignKey(courses, on_delete=models.SET_NULL, null=True)
    userid = models.ForeignKey(user, on_delete=models.SET_NULL, null=True)

# the class qrCode creates a table with a unique id for each qrCode and with courseid,
# userid, and time.
class Attendance(models.Model):
    qrid = models.AutoField(primary_key=True)
    courseid = models.ForeignKey(courses, on_delete=models.SET_NULL, null=True)
    userid = models.ForeignKey(user, on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField(auto_now=False, auto_now_add=False)

# the definition addqrCode makes a new qrCode when called.
def addqrCode (qrid, courseid, userid):
    if in_course.objects.filter(userid=userid).count() == 0:
        raise ValueError('No user with the userid' + userid + ' exists in this class')
    if courses.objects.filter(courseid=courseid).count() == 0:
        raise ValueError('No course with the courseid' + courseid + ' exists')
    new_qrCode = Attendance(qrid=qrid, courseid=courseid, userid=userid, time=datetime.date.today())
    new_qrCode.save()


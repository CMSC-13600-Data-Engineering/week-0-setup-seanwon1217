from django.db import models
from django.contrib.auth.models import User

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
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    )
    userid = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_instructor = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    username = models.CharField(max_length=256, null=False)

# the class courses creates a table with each course name and assigns them an ID
days_of_week = [(1,'Monday'),(2,'Tuesday'),(3,'Wednesday'),(4,'Thursday'),(5,'Friday'),(6,'Saturday'),(7,'Sunday')]

class Course(models.Model):
    coursename = models.CharField(max_length=256, null=False)
    courseid = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)

    #def __str__(self):
        #return self.name

    #def save(self, *args, **kwargs):
        #if not self.code:
            # Generate a unique course code
            #self.code = str(uuid.uuid4()).replace('-', '')[:16]
        #super().save(*args, **kwargs)
             
# the class in_course creates a table with course's and the people in the course. It then
# says whether the user is an instructor
class in_course(models.Model):
    courseid = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    userid = models.ForeignKey(user, on_delete=models.SET_NULL, null=True)

# the class qrCode creates a table with a unique id for each qrCode and with courseid,
# userid, and time.
class Attendance(models.Model):
    qrid = models.AutoField(primary_key=True)
    courseid = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    userid = models.ForeignKey(user, on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField(auto_now=False, auto_now_add=False)

# the definition addqrCode makes a new qrCode when called.
def addqrCode (qrid, courseid, userid):
    if in_course.objects.filter(userid=userid).count() == 0:
        raise ValueError('No user with the userid' + userid + ' exists in this class')
    if Course.objects.filter(courseid=courseid).count() == 0:
        raise ValueError('No course with the courseid' + courseid + ' exists')
    new_qrCode = Attendance(qrid=qrid, courseid=courseid, userid=userid, time=datetime.date.today())
    new_qrCode.save()


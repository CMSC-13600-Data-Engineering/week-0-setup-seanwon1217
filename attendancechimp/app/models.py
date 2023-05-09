from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.crypto import get_random_string


# Create your models here.
# There will be two classes of users: students and instructorss.
time = timezone.now()

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
days_of_week = [('Mon','Mon'),('Tues','Tues'),('Wed','Wed'),('Thurs','Thurs'),('Fri','Fri'),('Sat','Sat'),('Sun','Sun'),('Mon,Wed,Fri','Mon,Wed,Fri'),('Mon,Wed','Mon,Wed'),('Tues,Thurs','Tues,Thurs')]
class Course(models.Model):
    coursename = models.CharField(max_length=256, null=False)
    course_id = models.CharField(max_length=255)
    #course_code = models.CharField(primary_key=True, max_length=256)
    start_date = models.DateField()
    end_date = models.DateField()
    class_start_time = models.TimeField()
    class_end_time = models.TimeField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length = 255, choices = days_of_week)
    meeting_days = models.CharField(max_length=255)
    students = models.ManyToManyField(User, related_name='courses_taken')


# the class in_course creates a table with course's and the people in the course. It then
# says whether the user is an instructor
class in_course(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, default='default_course_id')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('course_id', 'student')

    def __str__(self):
        return f"{self.course_id.coursename} - {self.student.username}"
    
# the class qrCode creates a table with a unique id for each qrCode and with course_id,
# userid, and time.
class Attendance(models.Model):
    qrid = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    userid = models.ForeignKey(user, on_delete=models.CASCADE)
    class_code = models.CharField(max_length=64)
    time = models.DateTimeField()
    @classmethod
    def generate_class_code(cls, course_id):
        # Generate a random string for class code
        class_code = get_random_string(length=32)
        # Create an Attendance object with course, class code, and time
        attendance = cls(course_id=course_id, class_code=class_code)
        attendance.save()
        # Return the class code
        return class_code

# the definition Addqrcode makes a new qrCode when called.
class Addqrcode(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    user= models.ForeignKey(user, on_delete=models.CASCADE)
    time = models.DateTimeField()
    qr_code_image = models.ImageField(upload_to='qrcodes/')
##    if in_course.objects.filter(userid=userid).count() == 0:
##        raise ValueError('No user with the userid' + userid + ' exists in this class')
##    if Course.objects.filter(course_id=course_id).count() == 0:
##        raise ValueError('No course with the course_id' + course_id + ' exists')
##    new_qrCode = Attendance(qrid=qrid, course_id=course_id, userid=userid, time=datetime.date.today())
##    new_qrCode.save()

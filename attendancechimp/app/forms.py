from django import forms
from django.forms import ModelForm
from app.models import courses

class CourseForm(ModelForm):
    class Meta:
        model = courses
        fields = ["coursename", "courseid", "start_date", "end_date", 'meeting_time', 'day_of_week']

# Creating a form to add a course.
form = CourseForm()


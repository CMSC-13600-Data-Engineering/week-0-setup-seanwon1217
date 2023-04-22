from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from app.models import courses

class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=60, required=True, help_text='Required.')
    USER_TYPE_CHOICES = (
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    )
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid school email address.')
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'user_type', 'password1', 'password2', )

class CourseForm(ModelForm):
    class Meta:
        model = courses
        fields = ["coursename", "courseid", "start_date", "end_date", 'meeting_time', 'day_of_week']

# Creating a form to add a course.
form = CourseForm()
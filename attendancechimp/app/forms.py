from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from app.models import Course
from django.core.exceptions import ValidationError

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
        model = Course
        fields = ["coursename", "courseid", "start_date", "end_date"]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if Course.objects.filter(code=code).exists():
            raise ValidationError("A course with this code already exists.")
        return code

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise ValidationError('End date must be after start date.')
        
# Creating a form to add a course.
form = CourseForm()

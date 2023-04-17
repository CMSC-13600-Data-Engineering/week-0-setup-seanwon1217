from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def index(request):
    classdict = {'class1':'CMSC136'}
    return render(request, 'app/index.html', classdict)

def new(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Check if the email is already in use
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                # Return error state - email already in use
                return render(request, 'new.html', {'form': form, 'error': 'Email already in use'})

            # Create a new user object
            user = form.save()

            # Add the user to the appropriate group
            user_type = request.POST.get('user_type')
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
            return redirect('success')
    else:
        form = UserCreationForm()
    return render(request, 'new.html', {'form': form})


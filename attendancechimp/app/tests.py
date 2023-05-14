from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Course, Attendance, in_course, Addqrcode
from datetime import datetime, timezone, timedelta

class OverviewTestCase(TestCase):
    def setUp(self):
        # Create a user and assign them to the 'Instructor' group
        self.user = User.objects.create_user(username='instructor', password='password')
        instructor_group = Group.objects.create(name='Instructor')
        self.user.groups.add(instructor_group)

        # Create a course
        now = datetime.now(timezone.utc)

        start_date = now
        end_date = now + timedelta(days=1)
        self.course = Course.objects.create(course_id='239', coursename='Gah', start_date=start_date, end_date=end_date, class_end_time=datetime.now(timezone.utc), class_start_time=datetime.now(timezone.utc))

        # Create some attendance records for the course
        Attendance.objects.create(qrid='1', class_code='0dd9e3b1-01cc-4cd9-b04b-9a72e0d9fc19')
        Attendance.objects.create(qrid='2', class_code='2abfb206-2320-4763-9256-124e93b6784c')
        Attendance.objects.create(qrid='3', class_code='f212926d-b290-416c-aa3b-86451bfedf08')

        # Create some in-course records for the course
        in_course.objects.create(course_id=self.course, user=self.user)

        # Create some Addqrcode records for the course
        Addqrcode.objects.create(course_id=self.course, class_code='xyz', user=self.user)
        Addqrcode.objects.create(course_id=self.course, class_code='xyz', user=self.user)

    def test_overview_view_with_instructor(self):
        # Log in as the instructor
        self.client.login(username='instructor', password='password')

        # Access the overview view with the course code '239'
        response = self.client.get(reverse('overview') + '?course_id=239')

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the course name/number is displayed in the response
        self.assertContains(response, 'Gah 239')

        # Check that the total number of students in the class is displayed
        self.assertContains(response, 'Number of Students in Class: 1')

    def test_overview_view_without_login(self):
        # Access the overview view without logging in
        response = self.client.get(reverse('overview') + '?course_id=239')

        # Check that the response redirects to the login view
        self.assertRedirects(response, reverse('login'))

    def test_overview_view_with_non_instructor(self):
        # Create a user without the 'Instructor' group
        user = User.objects.create_user(username='student', password='password')

        # Log in as the student
        self.client.login(username='student', password='password')

        # Access the overview view with the course code '239'
        response = self.client.get(reverse('overview') + '?course_id=239')

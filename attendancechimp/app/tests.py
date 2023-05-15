from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Course, Attendance, in_course, Addqrcode
from datetime import datetime, timezone, timedelta

#step 3/4. Testing Plan: testing for this project is done in two ways.
# The main way testing in done is through the creation of different webpages such
# as our course list page which will show a table with all of the course specific links
# hyperlinked. Additionally the Qr list is using if this example as it returns all of the
# qr codes that have been made. We tested our functionality by doing this and we begin tocheck 
# other features in the tests.py by using the TestCase django.test. The results of this are that one
# test fails.

class OverviewTestCase(TestCase):

    def with_instructor(self):
        user = User.objects.create_user(username='instructor', password='password')
        self.client.login(username='instructor', password='password')

        response = self.client.get(reverse('overview') + '?course_id=239')

        self.assertContains(response, '239')

        self.assertContains(response, '1')

    def without_login(self):

        response = self.client.get(reverse('overview') + '?course_id=239')


        self.assertRedirects(response, reverse('login'))

    def not_instructor(self):
        user = User.objects.create_user(username='student', password='password')

        self.client.login(username='student', password='password')
        response = self.client.get(reverse('overview') + '?course_id=239')

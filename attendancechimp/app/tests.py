from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Course, Attendance, in_course, Addqrcode
from datetime import datetime, timezone, timedelta

class OverviewTestCase(TestCase):

    def test_overview_view_with_instructor(self):
        user = User.objects.create_user(username='instructor', password='password')
        self.client.login(username='instructor', password='password')

        response = self.client.get(reverse('overview') + '?course_id=239')

        self.assertContains(response, '239')

        self.assertContains(response, '1')

    def test_overview_view_without_login(self):

        response = self.client.get(reverse('overview') + '?course_id=239')


        self.assertRedirects(response, reverse('login'))

    def test_overview_view_with_non_instructor(self):
        user = User.objects.create_user(username='student', password='password')

        self.client.login(username='student', password='password')
        response = self.client.get(reverse('overview') + '?course_id=239')

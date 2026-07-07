from django.test import TestCase
from django.urls import reverse


class TeacherRegistrationTests(TestCase):
    def test_teacher_registration_page_redirects_to_student_registration(self):
        response = self.client.get(reverse('teacher_register'))

        self.assertRedirects(response, reverse('student_register'))

    def test_teacher_registration_post_redirects_to_student_registration(self):
        response = self.client.post(
            reverse('teacher_register'),
            data={
                'username': 'teacheruser',
                'email': 'teacher@example.com',
                'password1': 'StrongPass123',
                'password2': 'StrongPass123',
            },
        )

        self.assertRedirects(response, reverse('student_register'))

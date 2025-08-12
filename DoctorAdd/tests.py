from django.test import TestCase
from django.contrib.auth.models import User
from .models import Doctor

class DoctorModelTest(TestCase):

    def setUp(self):
       
        self.user = User.objects.create_user(
            username="testdoctor",
            password="testpass123",
            first_name="John",
            last_name="Doe"
        )
       
        self.doctor = Doctor.objects.create(
            user=self.user,
            address="123 Test Street",
            mobile="0123456789",
            department="Cardiologist",
            status=True
        )

    def test_doctor_name(self):
        self.assertEqual(self.doctor.get_name(), "John Doe")

    def test_doctor_id(self):
        self.assertEqual(self.doctor.get_id(), self.user.id)

    def test_doctor_str(self):
        self.assertEqual(str(self.doctor), "John (Cardiologist)")

    def test_doctor_department_choice(self):
        self.assertIn(self.doctor.department, dict(Doctor._meta.get_field('department').choices))


# Create your tests here.

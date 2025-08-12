from django.test import TestCase
from django.contrib.auth.models import User
from .models import DoctorAdd

class DoctorAddTest(TestCase):
    def test_create_doctor(self):
        user = User.objects.create(first_name="John", last_name="Doe", username="johndoe")
        doctor = DoctorAdd.objects.create(
            user=user,
            id="221156"
            department="Cardiology",
            specialization="Heart Specialist",
            schedule="Mon-Fri, 10AM-5PM",
            mobile="1234567890"
        )
        self.assertEqual(str(doctor), "John Doe")

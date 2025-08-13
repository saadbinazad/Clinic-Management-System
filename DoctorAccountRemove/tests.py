from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import DoctorAccountRemove

class DoctorAccountRemoveTest(TestCase):
    def test_create_removal(self):
        record = DoctorAccountRemove.objects.create(doctor_name="Dr. Test", reason="Retired")
        self.assertEqual(record.doctor_name, "Dr. Test")


from django.test import TestCase
from django.urls import reverse
from .models import Doctor

class DoctorAddTests(TestCase):
    def test_add_doctor_success(self):
        resp = self.client.post(reverse("add_doctor"), {
            "name": "Dr. A",
            "specialization": "Cardiology",
            "email": "a@example.com",
            "phone": "0123456789",
            "active": True
        })
        self.assertRedirects(resp, reverse("doctor_list"))
        self.assertEqual(Doctor.objects.count(), 1)

    def test_duplicate_email_blocked(self):
        Doctor.objects.create(name="X", specialization="Derm", email="dup@ex.com", phone="11111111")
        resp = self.client.post(reverse("add_doctor"), {
            "name": "Y",
            "specialization": "Derm",
            "email": "dup@ex.com",
            "phone": "22222222",
            "active": True
        })
        self.assertContains(resp, "System error", status_code=200)

    def test_invalid_phone_format(self):
        resp = self.client.post(reverse("add_doctor"), {
            "name": "Z",
            "specialization": "Neuro",
            "email": "z@ex.com",
            "phone": "abcd",
            "active": True
        })
        self.assertContains(resp, "digits only", status_code=200)

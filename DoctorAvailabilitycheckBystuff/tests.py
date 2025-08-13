from datetime import date, time
from django.test import TestCase
from django.urls import reverse
from DoctorAddByAdmin.models import Doctor
from .models import AvailabilitySlot, Appointment

class AvailabilityTests(TestCase):
    def setUp(self):
        self.doc = Doctor.objects.create(
            name="Dr. Ava", specialization="ENT",
            email="ava@ex.com", phone="0123456789", active=True
        )
        self.today = date.today()
        AvailabilitySlot.objects.create(
            doctor=self.doc, date=self.today, start_time=time(9,0), end_time=time(10,0), slot_minutes=30
        )

    def test_view_shows_slots(self):
        resp = self.client.get(reverse("check_availability"), {"date": self.today.isoformat()})
        self.assertContains(resp, "09:00")
        self.assertContains(resp, "09:30")

    def test_booking_updates_availability(self):
        # book 09:00
        resp = self.client.post(reverse("book_appointment", args=[self.doc.id]), {
            "date": self.today.isoformat(),
            "time": "09:00",
            "patient_name": "John"
        }, follow=True)
        self.assertContains(resp, "Appointment booked.")
        # 09:00 should disappear
        resp2 = self.client.get(reverse("check_availability"), {"date": self.today.isoformat()})
        self.assertNotContains(resp2, "09:00")

    def test_invalid_past_date_blocked(self):
        past = date(2000,1,1).isoformat()
        resp = self.client.get(reverse("check_availability"), {"date": past})
        self.assertContains(resp, "Past date is not allowed.", status_code=200)

    def test_no_availability_message(self):
        # Different date where no slots exist
        resp = self.client.get(reverse("check_availability"), {"date": date(2100,1,1).isoformat()})
        self.assertContains(resp, "No availability.")

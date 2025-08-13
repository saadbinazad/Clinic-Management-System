from django.core.management.base import BaseCommand
from hospital.models import Doctor

class Command(BaseCommand):
    help = 'Create dummy doctors for the hospital management system'

    def handle(self, *args, **options):
        # Check if doctors already exist
        if Doctor.objects.exists():
            self.stdout.write(
                self.style.WARNING('Doctors already exist in the database. Skipping creation.')
            )
            return

        # Create dummy doctors
        doctors_data = [
            {'name': 'Sarah Johnson', 'specialty': 'Cardiology'},
            {'name': 'Michael Chen', 'specialty': 'Neurology'},
            {'name': 'Emily Rodriguez', 'specialty': 'Pediatrics'},
            {'name': 'David Thompson', 'specialty': 'Orthopedics'},
            {'name': 'Lisa Patel', 'specialty': 'Dermatology'},
            {'name': 'James Wilson', 'specialty': 'General Medicine'},
        ]

        created_count = 0
        for doctor_data in doctors_data:
            doctor, created = Doctor.objects.get_or_create(
                name=doctor_data['name'],
                specialty=doctor_data['specialty']
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created doctor: Dr. {doctor.name} ({doctor.specialty})')
                )

        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created {created_count} doctors!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('All doctors already existed in the database.')
            )

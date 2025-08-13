from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Feedback
from .forms import FeedbackForm
from django.utils import timezone

class FeedbackModelTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testpatient',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create a test feedback
        self.feedback = Feedback.objects.create(
            user=self.user,
            category='complaint',
            messages='Test feedback message'
        )

    def test_feedback_creation(self):
        """Test that a feedback instance is created correctly"""
        self.assertEqual(self.feedback.user.username, 'testpatient')
        self.assertEqual(self.feedback.category, 'complaint')
        self.assertEqual(self.feedback.messages, 'Test feedback message')
        self.assertTrue(isinstance(self.feedback.created_at, type(timezone.now().date())))

    def test_feedback_str_representation(self):
        """Test the string representation of feedback"""
        expected_str = f"{self.user.username} - {self.feedback.category}"
        self.assertEqual(str(self.feedback), expected_str)

class FeedbackFormTests(TestCase):
    def test_feedback_form_valid_data(self):
        """Test form with valid data"""
        form_data = {
            'category': 'suggestion',
            'messages': 'This is a test suggestion'
        }
        form = FeedbackForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_feedback_form_invalid_data(self):
        """Test form with invalid data"""
        form_data = {
            'category': 'invalid_category',  # Invalid category
            'messages': ''  # Empty message
        }
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

class FeedbackViewTests(TestCase):
    def setUp(self):
        # Create a test user and client
        self.user = User.objects.create_user(
            username='testpatient',
            password='testpass123'
        )
        self.client = Client()

    def test_feedback_view_requires_login(self):
        """Test that feedback view requires login"""
        response = self.client.get(reverse('submit_feedback'))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)

    def test_feedback_submission_logged_in(self):
        """Test feedback submission when logged in"""
        # Log in the user
        self.client.login(username='testpatient', password='testpass123')
        
        # Submit feedback
        feedback_data = {
            'category': 'other',
            'messages': 'Test feedback submission'
        }
        response = self.client.post(reverse('submit_feedback'), feedback_data)
        
        # Should redirect after successful submission
        self.assertEqual(response.status_code, 302)
        
        # Check if feedback was created
        self.assertTrue(Feedback.objects.filter(
            user=self.user,
            category='other',
            messages='Test feedback submission'
        ).exists())

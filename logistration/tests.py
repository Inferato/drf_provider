import json
from unittest.mock import MagicMock
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from .views import LoginView, ProcessPaymentView, RegistrationView, UserProfileView, UploadDocuments, CheckUserExistsView
from django.contrib.messages.storage.fallback import FallbackStorage


class TestViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.login_url = reverse('login')
        self.payment_url = reverse('payment')
        self.register_url = reverse('register')
        self.profile_url = reverse('user_profile')
        self.document_url = reverse('upload_document')
        self.check_user_url = reverse('check_user_exists')
        self.test_file = SimpleUploadedFile("file.txt", b"file_content")
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
    
    @staticmethod
    def set_middleware_obj(request):
        setattr(request, 'session', MagicMock())
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
    
    def test_login_view_get(self):
        request = self.factory.get(self.login_url)
        request.user = self.user
        self.set_middleware_obj(request)
        response = LoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)
    
    def test_login_view_post(self):
        request = self.factory.post(self.login_url, {'username': 'testuser', 'password': 'testpass'})
        # request.user = self.user
        self.set_middleware_obj(request)
        response = LoginView.as_view()(request)
        self.assertEqual(response.status_code, 302)
    
    def test_process_payment_view_get(self):
        request = self.factory.get(self.payment_url)
        request.user = self.user
        self.set_middleware_obj(request)
        response = ProcessPaymentView.as_view()(request)
        self.assertEqual(response.status_code, 200)
    
    def test_process_payment_view_post(self):
        request = self.factory.post(self.payment_url, {'amount': 100})
        request.user = self.user
        self.set_middleware_obj(request)
        response = ProcessPaymentView.as_view()(request)
        self.assertEqual(response.status_code, 200)
    
    def test_registration_view_get(self):
        request = self.factory.get(self.register_url)
        self.set_middleware_obj(request)
        response = RegistrationView.as_view()(request)
        self.assertEqual(response.status_code, 200)
    
    def test_registration_view_post(self):
        request = self.factory.post(self.register_url, {'username': 'newuser', 'password1': 'newpass123', 'password2': 'newpass123', 'email': 'newuser@example.com'})
        self.set_middleware_obj(request)
        response = RegistrationView.as_view()(request)
        self.assertEqual(response.status_code, 302)
    
    def test_user_profile_view_get(self):
        request = self.factory.get(self.profile_url)
        request.user = self.user
        self.set_middleware_obj(request)
        response = UserProfileView.as_view()(request)
        self.assertEqual(response.status_code, 200)
    
    def test_user_profile_view_post(self):
        request = self.factory.post(self.profile_url, {'field1': 'value1'})
        request.user = self.user
        self.set_middleware_obj(request)
        response = UserProfileView.as_view()(request)
        self.assertEqual(response.status_code, 302)
    
    def test_upload_documents_view_get(self):
        request = self.factory.get(self.document_url)
        self.set_middleware_obj(request)
        response = UploadDocuments.as_view()(request)
        self.assertEqual(response.status_code, 200)
    
    def test_upload_documents_view_post(self):
        request = self.factory.post(self.document_url, {'title': 'test title'})
        request.user = self.user
        request.FILES['file'] = self.test_file
        self.set_middleware_obj(request)
        response = UploadDocuments.as_view()(request)
        self.assertEqual(response.status_code, 302)
    
    def test_check_user_exists_view_get(self):
        request = self.factory.get(self.check_user_url, {'username': 'testuser', 'email': 'new_email@test.com'})
        self.set_middleware_obj(request)
        response = CheckUserExistsView.as_view()(request)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data.get('data'), dict)
        self.assertEqual(response_data['data'].get('username_exists'), True)
        self.assertEqual(response_data['data'].get('email_exists'), False)
        self.assertIsNot(response_data['data'].get('email_exists'), True)

from django.urls import path
from .views import (
    LoginView, 
    RegistrationView, 
    logout_view, 
    UserProfileView,
    ProcessPaymentView,
    UploadDocuments,
    CheckUserExistsView
)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('user-profile/', UserProfileView.as_view(), name='user_profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('payment/', ProcessPaymentView.as_view(), name='payment'),
    path('upload-document/', UploadDocuments.as_view(), name='upload_document'),
    path('check_user_exists/', CheckUserExistsView.as_view(), name='check_user_exists'),
]

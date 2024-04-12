from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required  # noqa
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from .forms import PaymentForm, RegistrationForm, UserProfileForm, DocumentForm
from .models import UserProfile

User = get_user_model()


class LoginView(View):
    template_name = 'login.html'
    form_class = AuthenticationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('payment')
        return render(request, self.template_name, {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


class ProcessPaymentView(LoginRequiredMixin, View):
    template_name = 'payment/process_payment.html'
    success_template_name = 'payment/success.html'
    form_class = PaymentForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, f'Платіж на суму {transaction.amount} був успішно здійснений. ID операції: {transaction.id}')
            return render(request, self.success_template_name, {'transaction': transaction})
        return render(request, self.template_name, {'form': form})


class RegistrationView(View):
    template_name = 'registration/register.html'
    form_class = RegistrationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # user = form.save()
            # login(request, user)
            messages.success(request, 'Ваш обліковий запис був успішно створений. Увійдіть зараз!')
            return redirect('login')
        return render(request, self.template_name, {'form': form})


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'user_profile.html'
    form_class = UserProfileForm

    def get(self, request, *args, **kwargs):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = self.form_class(instance=user_profile)
        return render(request, self.template_name, {'form': form, 'user_profile': user_profile})

    def post(self, request, *args, **kwargs):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = self.form_class(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш обліковий запис був успішно оновлений!')
            return redirect('user_profile')
        return render(request, self.template_name, {'form': form, 'user_profile': user_profile})


class UploadDocuments(View):
    form = DocumentForm

    def get(self, request, *args, **kwargs):
        return render(request, 'upload_document.html', {'form': self.form()})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('payment')


class CheckUserExistsView(View):
    def get(self, request):
        username_exists = False
        email_exists = False

        username = request.GET.get('username', None)
        email = request.GET.get('email', None)

        if username:
            username_exists = User.objects.filter(username=username).exists()

        if email:
            email_exists = User.objects.filter(email=email).exists()

        user_check_response = {
            'user_check_errors': username_exists or email_exists
        }

        data = {
            'user_check_errors': username_exists or email_exists,
            'username_exists': username_exists,
            'email_exists': email_exists
        }
        user_check_response['data'] = data

        return JsonResponse(user_check_response)


def some_useless_func():
    return "Some output"

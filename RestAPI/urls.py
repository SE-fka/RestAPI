"""RestAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import ChangePasswordView, HomeView, SignupView, UserLoginView,  PasswordResetView, PasswordResetConfirmView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', HomeView.as_view(), name='home_api'),

    #Social Google siginup and login
    path('accounts/google/callback/', include('allauth.urls')),
    path('accounts/google/callback/signup/', include('allauth.urls')),
    path('accounts/google/callback/login/', include('allauth.urls')),
 
    #Social Facebook siginup and login
    path('accounts/facebook/login/callback/', include('allauth.urls')),
    path('accounts/facebook/login/signup/', include('allauth.urls')),
    path('accounts/facebook/login/', include('allauth.urls')),
    
    #For user siginup and login
    path('api/auth/signup/', SignupView.as_view(), name='signup'),
    path('api/auth/login/', UserLoginView.as_view(), name='login'),

    #For password rest
    path('api/auth/password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('api/password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    #For password change
    path('api/auth/change-password', ChangePasswordView.as_view(), name='change-password'),
    path('api/auth/logout', UserLoginView.as_view(), name='user-logout'),
]

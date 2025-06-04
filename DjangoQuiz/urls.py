"""DjangoQuiz URL Configuration
 
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from Quiz.views import *
from django.conf import settings
from django.conf.urls.static import static
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('quiz/', quiz, name='quiz'),
    path('quiz/<int:category_id>/', quiz, name='quiz_category'),
    path('addQuestion/', addQuestion, name='addQuestion'),
    path('addCategory/', addCategory, name='addCategory'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutPage, name='logout'),
    path('register/', registerPage, name='register'),
    path('profile/', user_profile, name='profile'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('password-reset/', password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
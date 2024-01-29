"""
URL configuration for CRMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from CourseReg import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', views.index, name='index'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('student/login/', views.student_login, name='student_login'),
    path('student/courses/', views.student_courses, name='courses'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('student/<int:student_id>/', views.student_profile, name='student-profile'),
    path('student/register/', views.student_register, name='student-register'),
    path('course-enrollment/', views.course_enrollment, name='course_enrollment'),
    path('register-course/<int:class_id>/', views.register_course, name='register_course'),
    path('unregister-course/<int:class_id>/', views.unregister_course, name='unregister_course'),
    path('student-tables/', views.student_tables, name='student_tables'),
    path('ws/group/<int:group_id>/', views.chatPage, name='chatPage'),
    

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

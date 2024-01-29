from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Course, Student, schedule, Class, Group, Message
from django.contrib import messages
from django.urls import reverse

def index(request):
    return render(request, 'index.html')

def admin_login(request):
    return render(request, 'crms/pages-login-admin.html')

def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print('username', username)
        print('password', password)
        
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            # check if user is a student
            if user.user_type=='student':
                login(request, user)
                # redirect to student dashboard
                return redirect('dashboard')
            else:
                # display error message
                error_message = 'You do not have permission to access this page.'
                print('error', error_message)
                return render(request, 'crms/pages-login-student.html', {'error_message': error_message})
        else:
            # display error message
            error_message = 'Invalid username or password.'
            print('error', error_message)
            return render(request, 'crms/pages-login-student.html', {'error_message': error_message})
    else:
        return render(request, 'crms/pages-login-student.html')


@login_required
def dashboard(request):
    context = student_details(request)
    return render(request, 'crms/student-dashboard.html', context)

@login_required
def student_profile(request, student_id):
    student = Student.objects.get(id=student_id)
    return render(request, 'crms/student-profile.html', {'student': student})

@login_required
def student_register(request):
    context = student_details(request)
    return render(request, 'crms/student-register.html', context)

def course_enrollment(request):
    context = student_details(request)
    return render(request, 'crms/course-enrollment.html', context)

def register_course(request, class_id):
    student = Student.objects.get(id=request.user.id)
    course = Class.objects.get(id=class_id)
    if student.register_for_course(course):
        messages.success(request, f'You have successfully registered for {course}.')
    else:
        messages.warning(request, f'You are already registered for {course}.')
    return redirect('course_enrollment')

def unregister_course(request, class_id):
    student = Student.objects.get(id=request.user.id)
    course = Class.objects.get(id=class_id)
    student.unregister_from_course(course)
    messages.success(request, f'You have successfully unregistered from {course}.')
    return redirect('course_enrollment')

def student_tables(request):
    context = student_details(request)
    return render(request, 'crms/student-tables-data.html', context)

def student_details(request):
    student = Student.objects.get(id=request.user.id)
    courses = student.get_semester_courses()
    registered_courses = student.get_registered_courses()
    available_courses = student.get_available_courses()
    groups = student.get_group_list()
    
    context = {
        'student':student,
        'schedule': schedule(student),
        'courses': courses,
        'registered_courses': registered_courses,
        'available_courses': available_courses,
        'groups':groups,
    }
    return context

def chatPage(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    context = student_details(request)
    context['group_id'] = group_id
    context['group_name'] = group.name
    context['messages'] = group.messages.all()
    return render(request, 'group.html', context)

def group_list(request):
    groups = Group.objects.all()
    return render(request, 'group_list.html', {'groups': groups})

def group_chat(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    messages = group.messages.all()
    return render(request, 'group_chat.html', {'group': group, 'messages': messages})

def student_courses(request):
    context = student_details(request)
    return render(request, 'student-courses.html', context)


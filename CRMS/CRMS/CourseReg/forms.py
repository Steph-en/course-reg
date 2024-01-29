from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class StudentCreationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    student_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    program = forms.ModelChoiceField(queryset=Program.objects.all())
    
    class Meta:
        model = Student
        fields = ('student_id','first_name', 'last_name')

class StudentChangeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True), required=False)
    #completed_courses = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Student
        fields = ('student_id', 'first_name', 'last_name', 'program', 'password','current_semester', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #if self.instance.pk:
            #completed_courses = self.instance.get_completed_courses()
            #courses_str = ", ".join(str(course) for course in completed_courses)
            #self.initial['completed_courses'] = courses_str
            #self.fields['completed_courses'].widget.attrs['readonly'] = True



class LecturerChangeForm(forms.ModelForm):
    class Meta:
        model = Lecturer
        fields = ('first_name', 'last_name', 'email', 'password','is_active')

class AdminChangeForm(forms.ModelForm):
    class Meta:
        model = Administrator
        fields = ('first_name', 'last_name', 'email',  'password','is_active')

class ClassInlineForm(forms.ModelForm):
    def get_courses(self,obj):
        return [(i.course,i.course) for i in Class.objects.filter(Lecturer !=obj)]

    classes = forms.Select(choices=[(i,i) for i in Class.objects.all()])
    
    class Meta:
        model = Class
        fields = ('course', 'campus')

    
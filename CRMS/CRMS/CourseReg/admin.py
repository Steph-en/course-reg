from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *
from django.db import IntegrityError
from django.contrib import messages
from .forms import *


class ClassInline(admin.TabularInline):
    model = Class
    extra = 0
    classes = ('collapse',)

class CourseRegistrationInline(admin.TabularInline):
    model = CourseRegistration
    extra = 0
    classes = ('collapse',)

class RoomInline(admin.TabularInline):
    model = Room
    extra = 0
    classes = ('collapse',)
    
class PeriodInline(admin.TabularInline):
    model = Period
    extra = 0
    classes = ('collapse',)

class ProgramInline(admin.TabularInline):
    model = Program
    extra = 0
    classes = ('collapse',)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title',  'description','get_campus','get_programs')
    search_fields = ('code', 'title', )
    list_filter = ('is_core','classes__campus', 'programs_offering')

    def get_campus(self, obj):
        return [i.campus for i in obj.classes.all()]
    get_campus.short_description = 'Active Campus'

    def get_programs(self, obj):
        return list(obj.programs_offering.all())
    get_programs.short_description = 'Programs'




class Admin(admin.ModelAdmin):
    def get_first_name(self, obj):
        return obj.first_name.title()
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.last_name.title()
    get_last_name.short_description = 'Last Name'
    
    def is_active(self, obj):
        return obj.is_active
    is_active.short_description = 'Active'
    
class StudentAdmin(Admin):
    add_form = StudentCreationForm
    form = StudentChangeForm
    list_display = ('student_id', 'get_first_name', 'get_last_name', 'program', 'is_active')
    search_fields = ('student_id', 'first_name', 'last_name',)
    list_filter = ('program', )
    ordering = ('student_id',)

    inlines=[CourseRegistrationInline,]

class AdministratorAdmin(Admin):
    form = AdminChangeForm
    list_display = ('username','get_first_name', 'get_last_name', 'email', 'is_active')
    search_fields = ('username','first_name', 'last_name',)
    ordering = ('first_name',)

class LecturerAdmin(Admin):
    form = LecturerChangeForm
    list_display = ('username','get_first_name', 'get_last_name', 'email', 'get_class_count')
    search_fields = ('username','first_name', 'last_name',)
    ordering = ('first_name',)
    list_filter = ('assigned_classes__campus',)
    inlines=[ClassInline,]

    def get_class_count(self, obj):
        return list(obj.assigned_classes.all())
    get_class_count.short_description = 'Classes'

class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'registered_class', 'semester', 'status')
    search_fields = ('student__student_id', 'registered_class__course__code',)
    list_filter = ('status','semester__name','registered_class__campus', )


class GroupChatAdmin(admin.ModelAdmin):
    list_display = ('course', 'admin', 'description', 'created_at', )
    search_fields = ('course__code', 'description', )


class SlotAdmin(admin.ModelAdmin):
    list_display = ('day', 'period',)
    search_fields = ('day', 'period',)
    list_filter = ('day', )

class ClassAdmin(admin.ModelAdmin):
    list_display = ('course', 'slot', 'room')
    search_fields = ('course', 'slot', 'room')

class CampusAdmin(admin.ModelAdmin):
    list_display = ('name', 'type','get_room_count', 'get_period_count', 'get_class_count')
    search_fields = ('name', 'type',)
    
    inlines=[PeriodInline, RoomInline, ClassInline]

    def get_room_count(self, obj):
        return len(obj.rooms.all())
    get_room_count.short_description = 'Rooms'

    def get_period_count(self, obj):
        return len(obj.periods.all())
    get_period_count.short_description = 'Periods'

    def get_class_count(self, obj):
        return len(obj.classes.all())
    get_class_count.short_description = 'Active Classes'


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'code',)
    search_fields = ('name', 'code',)
    inlines=[ProgramInline,]

class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'campus','is_active')
    search_fields = ('name', 'campus',)
    list_filter = ('campus', 'is_active')

#admin.site.register(User)
admin.site.register(Lecturer, LecturerAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(CourseRegistration, CourseRegistrationAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Campus, CampusAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Administrator, AdministratorAdmin)
admin.site.register(Group)
admin.site.register(Message)






from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


DAY_CHOICES = (
    ('Mon', 'Monday'),
    ('Tue', 'Tuesday'),
    ('Wed', 'Wednesday'),
    ('Thu', 'Thursday'),
    ('Fri', 'Friday'),
    ('Sat', 'Saturday'),
    ('Sun', 'Sunday')
)

# def transform_to_choices(choices_dict):
#     choices = [(k, v) for k,v in choices_dict.items()]
#     return choices


# class UserManager(BaseUserManager):
#     def create_user(self, username, password=None, **extra_fields):
#         """
#         Creates and saves a new user with the given email and password.
#         """
#         if not username:
#             raise ValueError('Users must have a username')
#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
        
#         return user
    
#     def create_superuser(self, username, password):
#         """
#         Creates and saves a new superuser with the given email and password.
#         """
#         user = self.create_user(username, password,user_type='administrator',is_staff=True)
        
#         user.save(using=self._db)
#         return user
    

# class UserMan():
#     def c_user(self, uname, password=None, **extrafields):
#         if not uname:
#             raise ValueError('User must have a username')
#         user = self.model(uname = uname, **extrafields) # type: ignore
#         usser.set_password(password)
        # user.save(using=self._db)  

class User(AbstractUser):
    USER_CHOICES = {
    'administrator': 'Administrator',
    'lecturer': 'Lecturer',
    'student': 'Student'
}
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(_("password"), max_length=128)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=13, choices = USER_CHOICES, default='student')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)
    
    USERNAME_FIELD = 'username'
    
    def __str__(self):
        return self.username

# class Course(models.Model):
   

#     def get_full_name(self):
#         return f'{self.first_name.title()} {self.last_name.title()}'

#     def get_first_name(self):
#         return self.first_name.title()
    
#     def get_last_name(self):
#         return self.last_name.title()

#     def has_perm(self, perm, obj=None):
#         return True

#     def has_module_perms(self, app_label):
#         return True
    
#     def save(self, *args, **kwargs):
#         self.first_name = self.first_name.title()
#         self.last_name = self.last_name.title()
#         self.set_password(self.password)
#         super().save(*args, **kwargs)

class Administrator(User):
    
    is_staff = True

    def save(self, *args, **kwargs):
        self.username = self.email.lower()
        self.user_type = 'administrator'
        super().save(*args, **kwargs)

class Lecturer(User):
    
    def save(self, *args, **kwargs):
        self.username = self.email.lower()
        self.user_type = 'lecturer'
        super().save(*args, **kwargs)
    
    

class Student(User):
    student_id = models.CharField(max_length=20)
    program = models.ForeignKey('Program', on_delete=models.SET_NULL, null=True)
    classes = models.ManyToManyField('Class', through='CourseRegistration', related_name='registered_students')
    current_semester = models.IntegerField(choices=[(i, str(i)) for i in range(1,17)])
    
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
    
    def __str__(self):
        return f'{self.student_id.upper()}'

    def save(self, *args, **kwargs):
        self.student_id = self.student_id.upper()
        self.email = f'{self.student_id.lower()}@ait.edu.gh'
        if not self.password:
            self.set_password('default')
        self.username = self.student_id.lower()
        self.user_type = 'student'
        super().save(*args, **kwargs)
    
    def register_for_course(self, course):
        registration, created = CourseRegistration.objects.update_or_create(
            student=self, registered_class=course, defaults={'status': 'registered', 'semester':Semester.objects.get(campus=course.campus, is_active=True)})
        if created or registration.status == 'dropped':
            registration.status = 'registered'
            registration.save()
            return True
        return False

    def unregister_from_course(self, course):
        registration = CourseRegistration.objects.filter(student=self, registered_class=course, status='registered')
        if registration:
            registration[0].status = 'dropped'
            registration[0].save()

    def get_completed_courses(self):
        completed = CourseRegistration.objects.filter(student=self, status='completed')
       
        return [c.registered_class for c in completed]
    
    def get_registered_courses(self):
        completed = CourseRegistration.objects.filter(student=self, status='registered')
        
        return [c.registered_class for c in completed]
    
    def get_dropped_courses(self):
        dropped = CourseRegistration.objects.filter(student=self, status='dropped')
        return [c.registered_class for c in dropped]
    
    def get_semester_courses(self):
        available = []
        if self.program.available_courses:
            for course in list(self.program.available_courses.all()):
                if self.current_semester >= course.semester:
                    if course not in self.get_completed_courses():
                        available.append(course)
        return available

    def get_available_courses(self):
        available = []
        registered = [i.course for i in self.get_registered_courses()]
        for course in self.get_semester_courses():
            for i in course.classes.all():
                if i and i.lecturer and course not in available and course not in registered and i.campus.has_active_semester():
                    available.append(course)
        return available
    
    def get_group_list(self):
        groups = []
        registered_courses = CourseRegistration.objects.filter(student=self, status='registered')

        for course in registered_courses:
            c = course.registered_class.class_groups.filter(semester=course.semester)
            if c:
                groups.append(c[0])
                
        return groups 
 
class Program(models.Model):
    name = models.CharField(max_length=50)
    available_courses = models.ManyToManyField('Course',related_name='programs_offering',blank=True)
    school = models.ForeignKey('School', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.name.title()}'
    
    def save(self, *args, **kwargs):    
        self.name = self.name.title()
        super().save(*args, **kwargs)

    
class School(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=6)

    def __str__(self):
        return f'{self.code.title()}'
    
    def save(self, *args, **kwargs):
        self.code = self.code.upper()        
        self.name = self.name.title()
        super().save(*args, **kwargs)



class Campus(models.Model):
    CAMPUS_CHOICES = [
        ('regular', 'Regular'),
        ('weekend', 'Weekend')
    ]
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=CAMPUS_CHOICES, editable=True)
    
    def __str__(self):
        return f'{self.name.title()}'
    
    def has_active_semester(self):
        semester = self.semesters.get(is_active=True)
        if semester:
            return semester
        else:
            return False
    class Meta:
        verbose_name_plural = 'Campus'

    

class Period(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    campus = models.ForeignKey('Campus',on_delete=models.CASCADE, related_name='periods')

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

    def create_time_slots(self):
        if self.campus.type == 'regular':
            for day in ['Monday', 'Tuesday', 'Wednesday','Thursday','Friday']:
                Slot.objects.create(day=day, period=self)
        elif self.campus.type == 'weekend':
            for day in ['Saturday', 'Sunday']:
                Slot.objects.create(day=day, period=self)
    
    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
        self.create_time_slots()
        



class Slot(models.Model):
    day = models.CharField(choices=DAY_CHOICES, max_length=10)
    period = models.ForeignKey('Period', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.day} ({self.period})"

    
class Room(models.Model):
    name = models.CharField(max_length=50)
    campus = models.ForeignKey('Campus',on_delete=models.CASCADE, related_name='rooms')
    
    def __str__(self):
        return f'{self.name.upper()}'

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super().save(*args, **kwargs)

class Class(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='classes')
    slot = models.ForeignKey('Slot', on_delete=models.SET_NULL, null=True)
    lecturer = models.ForeignKey('Lecturer',on_delete=models.SET_NULL, null=True, related_name='assigned_classes')
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True)
    campus = models.ForeignKey('Campus', on_delete=models.CASCADE, related_name='classes')

    class Meta:
        verbose_name_plural = 'Classes'
        unique_together = ['course','campus']
    
    def __str__(self):
        return f'{self.course} - {self.campus}'
    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    is_core = models.BooleanField(default=False)
    semester = models.IntegerField(choices=[(i, str(i)) for i in range(1,9)])

    def save(self, *args, **kwargs):
        self.code = self.code.upper()  
        self.title = self.title.title()
        self.description = self.description.title()
        if self.is_core != Course.objects.get(id=self.id).is_core:
            if self.is_core:
                update_program_courses(self, add=True)
            else:
                update_program_courses(self, remove=True)

        super(Course, self).save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.code.upper()}'
    

class Semester(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    campus = models.ForeignKey('Campus', related_name='semesters', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name.title()}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_active:
            for sem in Semester.objects.filter(campus=self.campus):
                print(sem)
                if sem.id != self.id :
                    sem.is_active=False
                    sem.save()
            self.create_groups()
    
    def create_groups(self):
        for course in self.campus.classes.all():
            group = Group.objects.create(class_group = course)
            membership = Membership.objects.create(user = course.lecturer, group=group, is_student=False)
            
        
        
class CourseRegistration(models.Model):
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('dropped', 'Dropped'),
        ('completed','Completed'),
        ('failed', 'Failed')
    ]

    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    registered_class = models.ForeignKey("Class", on_delete=models.CASCADE)
    date_registered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['student','registered_class']

    def __str__(self):
        return f'{self.student}-{self.registered_class}-{self.semester}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group = self.registered_class.class_groups.filter(semester=self.semester)
        if not group:
            group = Group.objects.create(class_group = self.registered_class, semester = self.semester)
        else:
            group = group[0]
        
        membership = Membership.objects.create(user = self.student, group=group, is_student=True)


def update_program_courses(course, add=False, remove=False):
    for program in Program.objects.all():
        program.available_courses.add(course)
    program.save()

def schedule(student):
    classes = student.get_registered_courses()

    sorted_classes = sorted(classes, key=lambda x: (x.slot.day, x.slot.period))

    return sorted_classes

class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    semester = models.CharField(max_length=255)
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='class_groups')
    administrators = models.ManyToManyField(Administrator, related_name='groups_managed', blank=True)
    members = models.ManyToManyField(User, through='Membership', related_name='groups_joined')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.class_group:
            if not self.name:
                self.name = f'{self.class_group} - {self.class_group.campus.has_active_semester()}'
            if not self.description:
                self.description = self.class_group.course.description
            if not self.semester:
                self.semester = self.class_group.campus.has_active_semester()

        super().save(*args, **kwargs)

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.group.name}'

class Message(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} - {self.group.name}'
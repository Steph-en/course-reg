# Generated by Django 4.2.1 on 2023-05-16 03:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CourseReg', '0003_alter_campus_options_alter_class_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('CourseReg.user',),
        ),
        migrations.AddField(
            model_name='campus',
            name='type',
            field=models.CharField(choices=[('weekday', 'Weekday'), ('weekend', 'Weekend')], default='weekday', editable=False, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.IntegerField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8)], default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='period',
            name='campus',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='CourseReg.campus'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='campus',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='CourseReg.campus'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='current_semester',
            field=models.IntegerField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10), ('11', 11), ('12', 12), ('13', 13), ('14', 14), ('15', 15), ('16', 16)], default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='class',
            name='campus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_classes', to='CourseReg.campus'),
        ),
        migrations.AlterField(
            model_name='class',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='CourseReg.course'),
        ),
        migrations.AlterField(
            model_name='class',
            name='lecturer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_classes', to='CourseReg.lecturer'),
        ),
        migrations.AlterField(
            model_name='period',
            name='end_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='period',
            name='start_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='program',
            name='available_courses',
            field=models.ManyToManyField(blank=True, related_name='programs_offering', to='CourseReg.course'),
        ),
        migrations.AlterField(
            model_name='slot',
            name='day',
            field=models.CharField(choices=[('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'), ('Thu', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday'), ('Sun', 'Sunday')], max_length=10),
        ),
        migrations.AlterField(
            model_name='student',
            name='program',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='CourseReg.program'),
        ),
    ]

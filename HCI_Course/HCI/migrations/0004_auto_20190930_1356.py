# Generated by Django 2.2.5 on 2019-09-30 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HCI', '0003_topic_course'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='Course Code',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='Core for Major?',
            new_name='core_for_major',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='Course Description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='Instructor',
            new_name='instructor',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='Last Taught',
            new_name='last_taught',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='Learning Goals',
            new_name='learning_goals',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='Course Name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='Course Prerequisites',
            new_name='prerequisites',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='University',
            new_name='university',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='Course Website',
            new_name='url',
        ),
        migrations.RenameField(
            model_name='criteria',
            old_name='Course',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='criteria',
            old_name='Criteria Name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='criteria',
            old_name='Criteria Weight',
            new_name='weight',
        ),
        migrations.RenameField(
            model_name='university',
            old_name='University Name',
            new_name='name',
        ),
    ]

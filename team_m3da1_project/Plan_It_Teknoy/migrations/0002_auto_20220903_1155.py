# Generated by Django 3.2.6 on 2022-09-03 03:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Plan_It_Teknoy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='StudentID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Plan_It_Teknoy.users'),
        ),
        migrations.AlterField(
            model_name='teachers',
            name='TeacherID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Plan_It_Teknoy.users'),
        ),
    ]
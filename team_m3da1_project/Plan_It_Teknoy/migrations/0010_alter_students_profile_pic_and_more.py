# Generated by Django 4.1 on 2022-09-26 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Plan_It_Teknoy', '0009_auto_20220923_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='profile_pic',
            field=models.ImageField(default='Not set', null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='teachers',
            name='profile_pic',
            field=models.ImageField(default='Not set', null=True, upload_to='images/'),
        ),
    ]

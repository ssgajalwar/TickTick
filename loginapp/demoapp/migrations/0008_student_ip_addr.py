# Generated by Django 5.0.1 on 2024-03-24 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp', '0007_student_city_student_latitude_student_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='ip_addr',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
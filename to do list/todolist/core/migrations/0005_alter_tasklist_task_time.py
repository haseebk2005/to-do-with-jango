# Generated by Django 5.0.7 on 2024-09-29 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_tasklist_task_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasklist',
            name='task_time',
            field=models.DateTimeField(default='1900-01-01 00:00:00'),
        ),
    ]
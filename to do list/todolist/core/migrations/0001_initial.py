# Generated by Django 5.0.7 on 2024-09-29 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.TextField()),
                ('task_type', models.CharField(choices=[('work', 'Work'), ('urgent', 'Urgent'), ('personal', 'Personal')], default='work', max_length=10)),
            ],
        ),
    ]

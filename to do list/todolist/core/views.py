from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomLoginForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from core.models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from celery import shared_task

@shared_task
def send_due_soon_notifications():
    now = timezone.now()
    one_hour_later = now + timezone.timedelta(hours=1)
    
    tasks_due_soon = TaskList.objects.filter(
        task_time__lte=one_hour_later, task_time__gte=now
    )
    
    for task in tasks_due_soon:
        user_email = task.user.email
        task_name = task.task
        task_time = task.task_time.strftime('%Y-%m-%d %H:%M:%S')
        
        send_mail(
            'Task Due Soon!',
            f'You have a task "{task_name}" due at {task_time}. Please complete it within the next hour.',
            'rookiehaseeb2005@example.com',  # Replace with your sender email
            [user_email],
            fail_silently=False,
        )
@login_required
def home(request):
    if request.method == "POST":
        task_name = request.POST.get("task")
        task_type = request.POST.get("task_type")
        task_date = request.POST.get("task_date")
        task_time = request.POST.get("task_time")

        if task_date and task_time:
            task_datetime = timezone.make_aware(
                timezone.datetime.fromisoformat(f"{task_date} {task_time}")
            )

            # Validate that the task datetime is not in the past
            if task_datetime < timezone.now():
                return JsonResponse({'error': "Error: You cannot add a task with a due date or time in the past."}, status=400)

            # Create the task if validation passes
            TaskList.objects.create(
                task = task_name,
                task_time = task_datetime,
                task_type = task_type,
                user = request.user # Associate task with the logged-in user
                )  
            return JsonResponse({'success': "Task added successfully!"})

    no_of_tasks = TaskList.objects.filter(user=request.user).count()
    nearest_task = TaskList.objects.filter(user=request.user,task_time__gte=timezone.now()).order_by('task_time').first()

    return render(request, 'index.html', {
        'user': request.user,
        'task_count': no_of_tasks,
        'nearest_task': nearest_task
    })

@login_required
def urgent(request):
    tasks = TaskList.objects.filter(task_type='urgent',user=request.user)  # Filter tasks by 'urgent' type
    context = {
        "tasks": tasks,  # Pass the filtered tasks to the template
    }
    return render(request, 'urgent.html', context)


@login_required
def work(request):
    tasks = TaskList.objects.filter(task_type='work',user=request.user)  # Filter tasks by 'urgent' type
    context = {
        "tasks": tasks,  # Pass the filtered tasks to the template
    }
    return render(request, 'work.html', context)



@login_required
def personal(request):
    tasks = TaskList.objects.filter(task_type='personal',user=request.user)  # Filter tasks by 'urgent' type
    context = {
        "tasks": tasks,  # Pass the filtered tasks to the template
    }
    return render(request, 'personal.html', context)

    
@login_required
def delete_task(request, id):
    # Get the task object
    task = get_object_or_404(TaskList, id=id)
    
    # Get the task_type before deleting the task
    task_type = task.task_type
    
    # Delete the task
    task.delete()
    
    # Redirect based on the task_type
    if task_type == 'urgent':
        return redirect('urgent')  # Redirect to urgent page
    elif task_type == 'work':
        return redirect('work')  # Redirect to work page
    elif task_type == 'personal':
        return redirect('personal')  # Redirect to personal page

# views.py

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful. You are now logged in.')
            login(request, user)  # Automatically log in the user after registration
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid credentials.')
    else:
        form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')

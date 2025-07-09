from django.shortcuts import render
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task

from django.utils.timezone import is_naive, make_aware
from django.utils.dateparse import parse_datetime

dt = parse_datetime(request.POST['due_at'])
if is_naive(dt):
    dt = make_aware(dt)

due_at = dt

# Create your views here.
def index(request):
    if request.method == 'POST':
        task = Task(title=request.POST['title'],
                    due_at=make_aware(parse_datetime(request.POST['due_at'])))
        task.save()
    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    else:
        tasks = Task.objects.order_by('-posted_at')
    
    tasks=Task.objects.all()

    contexst = { 'tasks': tasks }
    return render(request, 'todo/index.html', contexst)

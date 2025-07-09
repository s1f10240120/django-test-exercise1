from django.shortcuts import render
from django.utils.timezone import make_aware, is_naive
from django.utils.dateparse import parse_datetime
from todo.models import Task
# Create your views here.
def index(request):
    if request.method == 'POST':
        raw_due_at = parse_datetime(request.POST['due_at'])
        if is_naive(raw_due_at):
            due_at = make_aware(raw_due_at)
        else:
            due_at = raw_due_at

        task = Task(
            title=request.POST['title'],
            due_at=due_at
        )
        task.save()

    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    else:
        tasks = Task.objects.order_by('-posted_at')
    
    tasks=Task.objects.all()

    contexst = { 'tasks': tasks }
    return render(request, 'todo/index.html', contexst)

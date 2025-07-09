# todo/views.py

from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_naive, make_aware
from todo.models import Task

def index(request):
    # POSTリクエストで新しいタスクを作成
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

    # 並び順を GET パラメータで切り替え
    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    else:
        tasks = Task.objects.order_by('-posted_at')

    context = {
        'tasks': tasks
    }
    return render(request, 'todo/index.html', context)
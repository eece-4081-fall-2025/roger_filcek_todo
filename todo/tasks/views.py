from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Task

def task_list(request):
    tasks = Task.objects.filter(archived=False).order_by("-created_at")
    return render(request, "tasks/task_list.html", {"tasks": tasks})

@require_http_methods(["GET", "POST"])
def task_create(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        details = request.POST.get("details", "").strip()
        if not title:
            return render(request, "tasks/task_form.html", {
                "errors": ["Title is required."],
                "title": title, "details": details
            })
        Task.objects.create(title=title, details=details)
        return redirect("task_list")
    return render(request, "tasks/task_form.html", {"title": "", "details": ""})

@require_http_methods(["GET", "POST"])
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, archived=False)
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        details = request.POST.get("details", "").strip()
        if not title:
            return render(request, "tasks/task_form.html", {
                "errors": ["Title is required."],
                "task": task, "title": title, "details": details
            })
        task.title = title
        task.details = details
        task.save()
        return redirect("task_list")
    return render(request, "tasks/task_form.html", {"task": task})

@require_http_methods(["POST"])
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, archived=False)
    task.completed = True
    task.save()
    return redirect("task_list")

@require_http_methods(["POST"])
def task_archive(request, pk):
    task = get_object_or_404(Task, pk=pk, archived=False)
    task.archived = True
    task.save()
    return redirect("task_list")

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student
import json


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'students/login.html')

def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'students/register.html', {'form': form})

@login_required
def home_view(request):
    return render(request, 'students/home.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def get_students(request):
    if request.user.is_authenticated:
        students = Student.objects.filter(user=request.user)
        data = list(students.values())
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

@csrf_exempt
def save_student(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        student_id = data.get("id")
        if student_id:
            student = Student.objects.get(id=student_id, user=request.user)
            student.name = data["name"]
            student.subject = data["subject"]
            student.mark = data["mark"]
            student.save()
        else:
            Student.objects.create(
                user=request.user,
                name=data["name"],
                subject=data["subject"],
                mark=data["mark"]
            )
        return JsonResponse({"status": "success"})

@csrf_exempt
def delete_student(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        student_id = data.get("id")
        Student.objects.filter(id=student_id, user=request.user).delete()
        return JsonResponse({"status": "deleted"})
from django.urls import path
from . import views
from .api import views as api_views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),

    # API routes
    path('api/students/', api_views.StudentListCreateAPI.as_view(), name='student-list'),
    path('api/students/<int:pk>/', api_views.StudentUpdateDeleteAPI.as_view(), name='student-detail'),

    path("get-students/", views.get_students, name="get_students"),
    path("save-student/", views.save_student, name="save_student"),
    path("delete-student/", views.delete_student, name="delete_student"),
]

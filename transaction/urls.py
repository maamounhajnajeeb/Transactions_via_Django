from django.urls import path
from . import views


app_name = "transaction"

urlpatterns = [
    path("success_atomic/", views.success_atomic, name="success_atomic"),
    path("un_success_atomic/", views.un_success_atomic, name="un_success_atomic"),
    path("atomic_commit_no_param/", views.atomic_commit_no_param, name="atomic_commit_no_param"),
    path("atomic_commit_with_param/", views.atomic_commit_with_param, name="atomic_commit_with_param"),
]

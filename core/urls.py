from django.urls import path
from core import views


urlpatterns = [
    path('departments/', views.DepartmentView.as_view(), name='departments'),
]

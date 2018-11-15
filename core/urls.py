from django.urls import path
from core import views


urlpatterns = [
    path('departments/', views.DepartmentView.as_view(), name='departments'),
    path('consumer/registration/',views.ConsumerRegistrationView.as_view(), name='consumer-registration'),
    path('consumer/authorization/', views.ConsumerAuthorizationView.as_view(), name='consumer-authorization')
]

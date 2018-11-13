from django.urls import path
from api import views


urlpatterns = [
    path('departments/', views.DepartmensListView.as_view(), name='departments-list'),
    path('products/', views.ProductListWithFilterView.as_view(), name='products-list'),
    path('group-of-products/<int:pk>/products/', views.ProductsFromGroupOfProducts.as_view(), name='products-from-group'),
    path('courier/', views.CourierListView.as_view(), name='courier-list'),
    path('worker/', views.WorkerListView.as_view(), name='worker-list'),
    path('department-of-products/<int:pk>/products/', views.DepartmentListOfGroup.as_view(), name='department-from-group'),
    path('characteristic', views.CharacteristicListView.as_view(), name='characteristic-list')
]

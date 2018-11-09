from rest_framework.generics import ListAPIView

from api.serializers import DepartmentSerializer, ProductsSerializer, CourierSerializer, WorkerSerializer
from core.models import Department, Product, Courier, Worker


class DepartmensListView(ListAPIView):
    serializer_class = DepartmentSerializer
    paginate_by = 2

    def get_queryset(self):
        return Department.objects.all()


class ProductListView(ListAPIView):
    serializer_class = ProductsSerializer

    def get_queryset(self):
        return Product.objects.all()


class ProductsFromGroupOfProducts(ListAPIView):
    serializer_class = ProductsSerializer

    def get_queryset(self):
        return Product.objects.filter(group_of_products__id=self.kwargs.get('pk'))


class CourierListView(ListAPIView):
    serializer_class = CourierSerializer

    def get_queryset(self):
        return Courier.objects.all()


class WorkerListView(ListAPIView):
    serializer_class = WorkerSerializer

    def get_queryset(self):
        return Worker.objects.all()


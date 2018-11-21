from django.db.models import Q

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import (
    Department, Product, Courier, Worker, Characteristic,
)

from .utils import (
    get_available_filters, filter_by_price, filter_by_brand,
    filter_by_country,
)
from .pagination import (
    PostLimitOffsetPagination, PostPageNumberPagination,
)
from .serializers import (
    DepartmentSerializer, ProductsSerializer, CourierSerializer,
    WorkerSerializer, GroupOfProductsSerializer, CharacteristicSerializer,
)


class DepartmentsListView(ListAPIView):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        return Department.objects.all()


class ProductListView(ListAPIView):
    serializer_class = ProductsSerializer
    pagination_class = PostPageNumberPagination

    def get_queryset(self):
        return Product.objects.all()


class ProductsFromGroupOfProducts(ListAPIView):
    serializer_class = ProductsSerializer
    pagination_class = PostLimitOffsetPagination

    def get_queryset(self):
        return Product.objects.filter(
            group_of_products__id=self.kwargs.get('pk')
        )


class CourierListView(ListAPIView):
    serializer_class = CourierSerializer

    def get_queryset(self):
        return Courier.objects.all()


class WorkerListView(ListAPIView):
    serializer_class = WorkerSerializer

    def get_queryset(self):
        return Worker.objects.all()


class ListOfGroupForDepartment(ListAPIView):
    serializer_class = GroupOfProductsSerializer

    def get_queryset(self):
        return Department.objects.get(
            pk=self.kwargs.get('pk')).group_of_products.all()


class CharacteristicListView(ListAPIView):
    serializer_class = CharacteristicSerializer

    def get_queryset(self):
        return Characteristic.objects.all()


class ProductListWithFilterView(APIView):

    def post(self, request):
        qs = Product.objects.filter(
            Q(group_of_products__pk=request.data.get('group_id')) |
            Q(group_of_products__department__pk=request.data.get(
                'department_id'
            ))
        )
        response = {
            "available_filters": get_available_filters(qs)
        }
        filters = request.data.get('filters', [])
        for f in filters:
            if f['name'] == "price":
                print(f['values'])
                qs = filter_by_price(qs, f['values'])
            if f['name'] == 'brand':
                qs = filter_by_brand(qs, f['values'])
            if f['name'] == "country":
                qs = filter_by_country(qs, f['values'])
        response["products"] = ProductsSerializer(qs, many=True).data
        return Response(response)


class AddProductFromBasket(ListAPIView):
    def post(self, request):
        pass

from django.db.models import Q

from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import (
    Department, Product, Courier, Worker, Characteristic,
    Basket, PositionInTheBasket)

from .utils import (
    get_available_filters, filter_by_price, filter_by_brand,
    filter_by_country,
    filter_by_name_of_product)
from .pagination import (
    PostLimitOffsetPagination, PostPageNumberPagination,
)
from .serializers import (
    DepartmentSerializer, ProductsSerializer, CourierSerializer,
    WorkerSerializer, GroupOfProductsSerializer,
    CharacteristicSerializer, PositionInTheBasketSerializer,
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
            if f["name"] == 'name':
                qs = filter_by_name_of_product(qs, f['value'])
            if f['name'] == "price":
                qs = filter_by_price(qs, f['values'])
            if f['name'] == 'brand':
                qs = filter_by_brand(qs, f['values'])
            if f['name'] == "country":
                qs = filter_by_country(qs, f['values'])
        response["products"] = ProductsSerializer(qs, many=True).data
        return Response(response)


class AddProductInBasketListView(APIView):

    def dispatch(self, request, *args, **kwargs):
        self.basket = get_object_or_404(
            Basket, consumer__pk=kwargs.get('pk')
        )
        return super(
            AddProductInBasketListView,
            self).dispatch(request, *args, **kwargs
                           )

    def get(self, request, *args, **kwargs):
        total_price = 0
        for item in self.basket.position_in_the_basket.all():
            total_price += item.product.price * item.quantity_of_product
        return Response({
            'products': PositionInTheBasketSerializer(
                self.basket.position_in_the_basket.all(), many=True
            ).data,
            'total_cost': total_price
        })

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(pk=request.data.get('product_id'))
        self.basket.position_in_the_basket.add(
            PositionInTheBasket.objects.create(
                product=product, quantity_of_product=1
            )
        )
        self.basket.save()
        total_price = 0
        for item in self.basket.position_in_the_basket.all():
            total_price += item.product.price * item.quantity_of_product
        return Response({
            'products': PositionInTheBasketSerializer(
                self.basket.position_in_the_basket.all(), many=True
            ).data,
            'total_cost': total_price
        })

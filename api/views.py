from django.db.models import Q, Min, Max
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import DepartmentSerializer, ProductsSerializer, CourierSerializer, WorkerSerializer, \
    GroupOfProductsSerializer, CharacteristicSerializer
from core.forms import ConsumerRegistrationForm
from core.models import Department, Product, Courier, Worker, Characteristic


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


class DepartmentListOfGroup(ListAPIView):
    serializer_class = GroupOfProductsSerializer

    def get_queryset(self):
        return Department.objects.get(pk=self.kwargs.get('pk')).group_of_products.all()


class CharacteristicListView(ListAPIView):
    serializer_class = CharacteristicSerializer

    def get_queryset(self):
        return Characteristic.objects.all()


class ProductListWithFilterView(APIView):

    def post(self, request, *args, **kwargs):
        qs = Product.objects.filter(
            Q(group_of_products__pk=request.data.get('group_id')) |
            Q(group_of_products__department__pk=request.data.get(
                'department_id'
            ))
        )
        response = {
            "products": ProductsSerializer(qs, many=True).data,
            "available_filters": [
                {
                    "name": "price",
                    "type": "diapason",
                    "values": [qs.aggregate(Min("price"))['price__min'],
                               qs.aggregate(Max("price"))['price__max']]
                }
            ]
        }
        return Response(response)


class ConsumerRegistrationView(TemplateView):
    template_name = 'core/registration.html'

    def get_context_data(self, **kwargs):
        return {'form': ConsumerRegistrationForm()}

    def post(self, request):
        form = ConsumerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(
                request, self.template_name,
                {'errors': form.errors, 'form': form}
            )


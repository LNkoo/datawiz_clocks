from django.urls import reverse
from rest_framework import serializers

from core.models import (
    Department, GroupOfProducts, Product, Courier, Worker,
    Characteristic,
)


class GroupOfProductsSerializer(serializers.ModelSerializer):
    products_url = serializers.SerializerMethodField('get_product_url')

    class Meta:
        model = GroupOfProducts
        fields = '__all__'

    def get_product_url(self, object):
        return reverse('products-from-group', kwargs={'pk': object.pk})


class DepartmentSerializer(serializers.ModelSerializer):
    groups_url = serializers.SerializerMethodField()

    class Meta:
        model = Department
        exclude = ('group_of_products',)

    @staticmethod
    def get_groups_url(object):
        return reverse(
            'groups-from-department', kwargs={'pk': object.pk}
        )


class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    characteristic = CharacteristicSerializer(read_only=True)

    class Meta:
        model = Product
        exclude = ('group_of_products',)


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User


class Characteristic(models.Model):
    brand = models.CharField(verbose_name='Бренд', max_length=255)
    country = models.CharField(verbose_name='Країна', max_length=255)
    weight = models.FloatField(verbose_name='Вага', max_length=255)
    text = models.TextField(verbose_name='Опис', blank=True, null=True)

    def __str__(self):
        return '{0}'.format(self.brand, self.country, self.weight)

    class Meta:
        verbose_name = "характеристика"
        verbose_name_plural = "Характеристики"


class Product(models.Model):
    name = models.CharField(verbose_name='Назва товару', max_length=255)
    price = models.FloatField(verbose_name='Вартість')
    picture = models.ImageField(
        verbose_name='Фото товару', default='default.jpg', blank=True
    )
    bar_code = models.IntegerField(
        verbose_name='Штрих код'
    )
    accessibility = models.BooleanField(
        verbose_name='Доступність', default=False
    )
    characteristic = models.OneToOneField(
        to=Characteristic, verbose_name='Характеристика', null=True,
        blank=True, on_delete=models.SET_NULL
    )
    group_of_products = models.ForeignKey(
        to="GroupOfProducts", verbose_name='Група товару',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "Товари"


class Department(models.Model):
    name = models.CharField(verbose_name='Назва', max_length=255)
    group_of_products = models.ManyToManyField(
        to="GroupOfProducts", verbose_name='Підкатегорія', blank=True
    )
    picture = models.ImageField(
        verbose_name='Логотип відділу',
        null=True, blank=True
    )

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        verbose_name = "відділ"
        verbose_name_plural = "Відділи"


class GroupOfProducts(models.Model):
    name = models.CharField(verbose_name='Назва групи', max_length=255)
    picture = models.ImageField(
        upload_to='groups_photo',
        verbose_name='Логотип групи',
        null=True, blank=True
    )

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        verbose_name = "група товару"
        verbose_name_plural = "Групи товарів"

    def get_goods(self):
        return Product.objects.filter(group_of_goods=self)


class PositionInTheBasket(models.Model):
    product = models.ForeignKey(to=Product, verbose_name='Товар',
                                on_delete=models.CASCADE)
    quantity_of_product = models.FloatField(
        verbose_name='Кількість товару')


class Basket(models.Model):
    position_in_the_basket = models.ManyToManyField(
        to=PositionInTheBasket, verbose_name='Позиція в корзині')
    client = models.ForeignKey(to="Consumer", verbose_name='Клієнт',
                               on_delete=models.CASCADE)


class Consumer(models.Model):
    name = models.CharField(verbose_name="Ім'я", max_length=255)
    surname = models.CharField(verbose_name='Прізвище', max_length=255)
    phone = models.CharField(verbose_name='Номер телефону',
                             max_length=15)
    account = models.OneToOneField(verbose_name="Акаунт", to=User,
                                   related_name='consumer',
                                   on_delete=models.PROTECT)

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        verbose_name = "користувач"
        verbose_name_plural = "Користувачі"


class Worker(AbstractBaseUser):
    USERNAME_FIELD = 'login'
    login = models.CharField(verbose_name='Логін', max_length=50)
    surname = models.CharField(verbose_name='Прізвище', max_length=255)
    name = models.CharField(verbose_name="Ім'я", max_length=255)

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        verbose_name = 'робітник'
        verbose_name_plural = 'Робітники'


class Courier(AbstractBaseUser):
    USERNAME_FIELD = 'login'
    login = models.CharField(verbose_name='Логін', max_length=50)
    surname = models.CharField(verbose_name='Прізвище', max_length=255)
    name = models.CharField(verbose_name="Ім'я", max_length=255)
    phone = models.CharField(verbose_name='Номер телефону',
                             max_length=15)

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        verbose_name = 'кур’єр'
        verbose_name_plural = 'Кур’єри'


class Order(models.Model):
    position_in_the_basket = models.ManyToManyField(
        to=PositionInTheBasket, verbose_name='Позиція в корзині')
    client = models.ForeignKey(to=Consumer,
                               verbose_name='Клієнт',
                               on_delete=models.CASCADE)


class Response(models.Model):
    text = models.TextField(verbose_name='Відгук')
    product = models.ForeignKey(to=Product, verbose_name='Товар',
                                on_delete=models.CASCADE)
    client = models.ForeignKey(to=Consumer, verbose_name='Клієнт',
                               on_delete=models.CASCADE)

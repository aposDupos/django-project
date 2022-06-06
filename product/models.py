from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=12)
    first_name = models.CharField(verbose_name='Имя', max_length=255)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255)
    delivery_address = models.CharField(verbose_name='Адрес доставки', max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Provider(models.Model):
    title = models.CharField(verbose_name='Имя поставщика', max_length=255)
    address = models.CharField(verbose_name='Адрес офиса', max_length=255)
    contact_phone = models.CharField(verbose_name='Контактный номер телефона', max_length=12)
    contact_email = models.EmailField(verbose_name='Контактная почта', max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'


class Product(models.Model):
    title = models.CharField(verbose_name='Название товара', max_length=255)
    description = models.TextField(verbose_name='Описание товара')
    provider = models.ForeignKey(to=Provider, verbose_name='Поставщик', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='Цена')
    count = models.IntegerField(verbose_name='Количество')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Order(models.Model):
    user = models.ForeignKey(to=User, verbose_name='Пользователь', on_delete=models.CASCADE)
    product = models.ManyToManyField(Product,  verbose_name='Продукт')
    created_at = models.DateTimeField(verbose_name='Дата, время создания заказа', auto_now=False, auto_now_add=True)
    STATUS_CHOICES = (('CREATED', 'Создан'), ('PROCESSING', 'Выполняется'), ('CANCELED', 'Отменён'), ('DONE', 'Выполнен'))
    status = models.CharField(verbose_name='Статус', choices=STATUS_CHOICES, default='CREATED',max_length=50)

    def get_total_price(self):
        sum = 0
        for product in self.product.all():
            sum += product.price
        return sum

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

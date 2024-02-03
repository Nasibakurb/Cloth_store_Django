from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    SIZE_CHOICES = (
        ('', ''),
        ('S', '42'),
        ('M', '44'),
        ('L', '46'),
        ('XL', '48'),
        ('XXL', '50'),
        ('XXXL', '52'),
    )
    BRAND_CHOICES = (
        ('', ''),
        ('adidas', 'Адидас'),
        ('Nike', 'Найк'),
    )

    size = models.CharField(max_length=100, choices=SIZE_CHOICES, default='')
    brand = models.CharField(max_length=100, choices=BRAND_CHOICES, default='')
    color = models.CharField(max_length=25, default='')
    min_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий от: {self.user.username} на {self.product.name}'


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')


class BankCard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    expiration_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return f'Карта {self.card_number} пользователя {self.user.username}'


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)

    STATUS_CHOICES = (
        ('processing', 'Обрабатывается'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('returned', 'Возвращен'),
        ('return_request', 'Запрос на возврат'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)

    def get_total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=10, default=None)
    street = models.CharField(max_length=10, default=None)
    postcode = models.CharField(max_length=10, default=None)
    bank_card = models.ForeignKey(BankCard, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(CartItem)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.id}'


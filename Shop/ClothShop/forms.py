from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Comment, BankCard, Order


class ProductForm(forms.ModelForm):
    min_price = forms.DecimalField(label='Минимальная цена', required=False)
    max_price = forms.DecimalField(label='Максимальная цена', required=False)

    class Meta:
        model = Product
        fields = ['name', 'image', 'price', 'description',
                  'size', 'brand', 'color']

        labels = {
            'name': 'Название',
            'price': 'Цена',
            'description': 'Описание',
            'image': 'Изображение',
            'size': 'Размер',
            'brand': 'Бренд',
            'color': 'Цвет',
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['size'].required = False
        self.fields['brand'].required = False
        self.fields['color'].required = False


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class OrderForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=15)
    last_name = forms.CharField(label='Фамилия', max_length=15)
    phone_number = forms.CharField(label='Номер телефона', max_length=15)
    city = forms.CharField(label='Город', max_length=10)
    street = forms.CharField(label='Улица', max_length=10)
    postcode = forms.CharField(label='Почтовый индекс', max_length=10)


class BankCardForm(forms.ModelForm):
    class Meta:
        model = BankCard
        fields = ['card_number', 'expiration_date', 'cvv']

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from ClothShop.forms import ProductForm, CommentForm, OrderForm, BankCardForm, RegistrationForm
from .mixins import LogoutMixin
from .models import Product, Comment, Cart, CartItem, Order, BankCard

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .serializers import ChangePasswordSerializer
from .utils import generate_invoice_pdf


# Добавление в корзину
@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('carts')


# Корзина
@login_required
def carts(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    return render(request, 'cart/carts.html', {'cart_items': cart_items, 'total_price': total_price,  'username': username})


# Удаление из корзины
def delete_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    if cart_item:
        cart_item.delete()
        messages.success(request, 'Продукт успешно удален из корзины.')
    else:
        messages.error(request, 'Продукт не найден в корзине.')
    return redirect('carts')


# Обновление в коризне
def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Количество успешно обновлено.')
        else:
            messages.error(request, 'Неверное значение количества.')

    return redirect('carts')


# Оформление заказа
def checkout(request):
    if request.user.is_authenticated:
        username = request.user.username
        bank_card = BankCard.objects.filter(user=request.user).first()
    else:
        username = None

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order(
                bank_card=bank_card,
                user=request.user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone_number=form.cleaned_data['phone_number'],
                city=form.cleaned_data['city'],
                street=form.cleaned_data['street'],
                postcode=form.cleaned_data['postcode']
            )
            order.save()

            cart = Cart.objects.get(user=request.user)

            cart_items = cart.cartitem_set.all()
            order.items.set(cart_items)

            cart_items.update(cart=None)

            pdf_response = generate_invoice_pdf(order)

            form = OrderForm()
            return render(request, 'cart/checkout.html', {'form': form,
            'thank_you_message': 'Спасибо за покупку!',
            'username': username, 'bank_card': bank_card, 'pdf_response': pdf_response})
    else:
        form = OrderForm()

    return render(request, 'cart/checkout.html', {'form': form,
                'username': username, 'bank_card': bank_card})


# Скачивание чеков
def download_invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    pdf_response = generate_invoice_pdf(order)

    return pdf_response


# Смена статуса заказа
def change_cart_item_status(request,  cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        cart_item.status = new_status
        cart_item.save()

        order = Order.objects.filter(items=cart_item).first()
        if order:
            return redirect('order_detail', order_id=order.id)

    return redirect('order_detail')


def delete_order_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    if request.method == 'POST':
        order = Order.objects.filter(items=cart_item).first()
        cart_item.delete()
        if order:
            return redirect('order_detail', order_id=order.id)
    return redirect('order_detail')


# Возврат заказа
def return_order_item(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)

    cart_item.status = 'return_request'
    cart_item.save()
    messages.success(request, 'Запрос на возврат успешно отправлен.')
    order = Order.objects.filter(items=cart_item).first()
    if order:
        return redirect('order_detail', order_id=order.id)

    return redirect('order_detail')


def order_detail(request, order_id):
    if request.user.is_authenticated:
        username = request.user.username
        order = Order.objects.get(id=order_id)
        order_items = order.items.all()
        STATUS_CHOICES = (
            ('processing', 'Обрабатывается'),
            ('shipped', 'Отправлен'),
            ('delivered', 'Доставлен'),
            ('returned', 'Возвращен'),
            ('return_request', 'Запрос на возврат'),
        )
    else:
        username = None
    context = {
        'order': order,
        'order_items': order_items,
        'username': username,
        "STATUS_CHOICES": STATUS_CHOICES,
    }
    return render(request, 'order_detail.html', context)


# Смена пароля
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")

            if not user.check_password(old_password):
                return Response({"detail": "Неверный текущий пароль."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)

            response_data = {"detail": "Пароль успешно изменен."}
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Профиль
def profile(request):
    if request.user.is_authenticated:
        users = User.objects.all()
        orders = Order.objects.all()
        bank_card, created = BankCard.objects.get_or_create(user=request.user)

        return render(request, 'profile.html', {'bank_card': bank_card, 'orders': orders, 'users': users,
            'username': request.user.username})
    else:
        return render(request, 'profile.html', {'username': None})


# Удалить заказ
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        order.delete()
        return redirect('profile')

    return render(request, 'delete_order.html', {'order': order})


# Создание бк
@login_required
def add_bank_card(request):
    try:
        bank_card = BankCard.objects.get(user=request.user)
    except BankCard.DoesNotExist:
        bank_card = None

    if request.method == 'POST':
        form = BankCardForm(request.POST, instance=bank_card)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            if bank_card:
                messages.success(request, 'Данные банковской карты обновлены.')
            else:
                messages.success(request, 'Банковская карта добавлена.')
            return redirect('profile')
    else:
        form = BankCardForm(instance=bank_card)

    return render(request, 'profile.html', {'form': form, 'bank_card': bank_card, 'username': request.user.username})


# Удаление пользователя
@login_required
def delete_user(request, user_id):
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, id=user_id)
            user.delete()
            return redirect('profile')
        except User.DoesNotExist:
            return render(request, 'error.html', {'message': 'User not found.'})
    else:
        return render(request, 'error.html', {'message': 'Invalid request method.'})


# Сделать админом
@login_required
def make_admin(request, user_id):
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, id=user_id)
            user.is_superuser = True
            user.save()
            return redirect('profile')
        except User.DoesNotExist:
            return render(request, 'error.html', {'message': 'User not found.'})
    else:
        return render(request, 'error.html', {'message': 'Invalid request method.'})


# Редактирование продукта
@login_required
def edit_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProductForm(instance=product)
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    return render(request, 'edit_product.html', {'form': form, 'product': product, 'username': username})


# Добавление продукта
@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProductForm()
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    return render(request, 'create_product.html', {'form': form, 'username': username})


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
    return redirect('index')


# Главная
def index(request):
    username = None
    products = Product.objects.all()
    form = ProductForm(request.GET)

    filters = {}
    filter_fields = ['size', 'brand', 'color']

    for field in filter_fields:
        value = request.GET.get(field)
        if value:
            filters[field] = value
            products = products.filter(**{field: value})

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    products_per_page = 6
    paginator = Paginator(products, products_per_page)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        username = request.user.username

    return render(request, 'index.html', {'username': username, 'form': form,
                                           'products': products, 'filters': filters})

# Авторизация
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


# Выход из системы через Миксин
class logout_view(LogoutMixin, View):
    def get(self, request, *args, **kwargs):
        return self.logout(request)


def register_view(request):
    error = None
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login_view')
        else:
            error = "Ошибка ! Пожалуйста, проверьте введенные данные."
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form, 'error': error})


# Детализация продукта
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    comments = Comment.objects.filter(product=product)
    comments_per_page = 2

    paginator = Paginator(comments, comments_per_page)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    return render(request, 'product_detail.html', {'product': product,
        'comments': comments, 'username': username})


# Добавление комментариев
def add_comment(request, product_id):
    product = Product.objects.get(pk=product_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()
            return redirect('product_detail', product_id=product_id)
    else:
        form = CommentForm()

    comments = Comment.objects.filter(product=product)

    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None
    return render(request, 'product_detail.html', {'product': product, 'form': form, 'comments': comments, 'username': username})


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        comment.delete()
        return redirect('product_detail', product_id=comment.product.id)

    return redirect('product_detail', product_id=comment.product.id)



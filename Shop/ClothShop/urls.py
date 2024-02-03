
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from ClothShop import views
from ClothShop.views import edit_product, ChangePasswordView, profile, \
    delete_user, make_admin, add_to_cart, carts, delete_cart_item, update_cart_item, checkout, delete_order, \
    add_bank_card, order_detail, change_cart_item_status, delete_order_item, return_order_item, logout_view, \
    download_invoice_pdf

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('', views.index, name='index'),
    path('logout/', logout_view.as_view(), name='logout_view'),
    path('register/', views.register_view, name='register_view'),

    path('create_product/', views.create_product, name='create_product'),
    path('edit_product/<int:product_id>/', edit_product, name='edit_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_comment/<int:product_id>/', views.add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),

    path('profile/', profile, name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password_api'),
    path('profile/delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('profile/make_admin/<int:user_id>/', make_admin, name='make_admin'),
    path('profile/add_bank_card/', add_bank_card, name='add_bank_card'),
    path('profile/delete_order/<int:order_id>/', delete_order, name='delete_order'),

    path('order_detail/<int:order_id>/', order_detail, name='order_detail'),
    path('order_detail/change_cart_item_status/<int:cart_item_id>/', change_cart_item_status, name='change_cart_item_status'),
    path('order_detail/delete_order_item/<int:cart_item_id>/', delete_order_item, name='delete_order_item'),
    path('order_detail/return_order_item/<int:cart_item_id>/', return_order_item, name='return_order_item'),
    path('order_detail/download_invoice/<int:order_id>/', download_invoice_pdf, name='download_invoice_pdf'),

    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('view_cart/', carts, name='carts'),
    path('delete_cart_item/<int:cart_item_id>/', delete_cart_item, name='delete_cart_item'),
    path('update_cart_item/<int:cart_item_id>/', update_cart_item, name='update_cart_item'),

    path('checkout/', checkout, name='checkout'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


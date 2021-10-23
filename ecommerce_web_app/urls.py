from django.urls import path
from .views import *

urlpatterns = [
    path('', login, name='login'),
    path('user_logout', user_logout, name='user_logout'),
    path('signup', signup, name='signup'),
    path('check_email', check_email, name='check_email'),
    path('check_username', check_username, name='check_username'),
    path('admin_login', admin_login, name='admin_login'),
    path('admin_logout', admin_logout, name='admin_logout'),
    path('user_data', user_data, name='user_data'),
    path('user_data_update/<int:id>', user_data_update, name='user_data_update'),
    path('user_data_delete/<int:id>', user_data_delete, name='user_data_delete'),
    path('add_item', add_item, name='add_item'),
    path('add_category', add_category, name='add_category'),
    path('item_data', item_data, name='item_data'),
    path('home', home, name='home'),
    path('cart', cart, name='cart'),
    path('updater', updater, name='updater'),
    path('remove_cart', remove_cart, name='remove_cart'),
    path('place_order', place_order, name='place_order'),
    path('list_of_order', list_of_order, name='list_of_order'),
]

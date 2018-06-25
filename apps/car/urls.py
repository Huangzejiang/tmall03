from django.conf.urls import url

from apps.car import views

urlpatterns = [
    url('add/', views.add_car, name='add'),
    url('shop/', views.shop_car, name='shop'),
    url('buy/', views.buy_shop, name='buy'),
    url('confirm/', views.confirm_buy_shop, name='confirm'),
]

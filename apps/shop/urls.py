from django.conf.urls import url
from apps.shop import views

urlpatterns = [
    url('index/', views.index, name='index'),
    # url('index02/', views.index02, name='index02'),
    url('search/', views.search, name='search'),
    url('cate/', views.cate),
    url('login/', views.login, name='login'),
    url('loginout/', views.loginout, name='loginout'),
    url('register/', views.register, name='register'),
    url('detail/(\d+)/', views.shop_detail, name='detail')
]

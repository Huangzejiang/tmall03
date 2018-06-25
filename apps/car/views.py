import json
from django.http import HttpResponse
from django.shortcuts import render,redirect
from apps.shop.models import ShopCar, Shop


def add_car(request):
    try:
        num = request.GET.get('num')
        shop_id = request.GET.get('shop_id')
        shop = Shop.objects.get(pk=int(shop_id))
        if 0 < int(num) < shop.stock:
            ShopCar.objects.create(number=int(num), shop_id=int(shop_id), user_id=1)
    except:
        pass
    return render(request, '', {'msg': 'success'})



def shop_car(request):
    req_session = request.session
    temp = req_session.get('userinfo')
    user_id = temp.get("uid")
    if user_id:
        # cars = ShopCar.objects.filter(user_id=user_id, status=1)
        cars = ShopCar.objects.filter(user_id=user_id)
        # cars = ShopCar.objects.filter(user_id=1, status=1)
        for car in cars:
            car.shop.image = car.shop.shopimage_set.filter(type='type_single').first()
    return render(request, 'cart1.html', {'cars': cars})



def buy_shop(request):
    if request.method == 'POST':
        # 获取用户提交的数据
        cars = request.POST.get('cars')
        cars = json.loads(cars)
        for car in cars:
            num = car['num']
            car_id = car['car_id']
            ShopCar.objects.filter(car_id=car_id).update(number=num, status=2)

    #重定向到确认登录界面
    return redirect('/car/confirm/')


def confirm_buy_shop(request):
    user_id = request.session.get('userinfo').get('uid')
    if user_id:
        cars = ShopCar.objects.filter(user_id=user_id, status=2)
        for car in cars:
            car.shop.image = car.shop.shopimage_set.filter(type='type_single').first()
    return render(request, 'buy_page.html', {'cars': cars})






















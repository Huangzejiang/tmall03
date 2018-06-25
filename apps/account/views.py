from django.shortcuts import render, redirect
from apps.shop.models import models #导入models模型
from apps.shop.models import User,ShopCar

#登录
def login(request):
    if request.method == "GET":
        return render(request,"login.html")
    elif request.method == "POST":
        #获取form表单中数据
        username = request.POST.get("name")
        password = request.POST.get("password")
        #判断用户名和密码不能为空
        if username and password:
            users = User.objects.filter(name=username)
            print(type(users),users)
            if users: #判断users用户是否存在
                user = users.first()
                if user.password == password: #判断密码是否存在
                    #表示用户登录成功
                    #作用:查询用户购物车的商品总数量  (利用外键关联进行查询)
                    # count = user.shopcar_set.count()  #方法1
                    count = ShopCar.objects.filter(user=user.uid).count()    #方法2
                    #用户信息
                    userinfo = {
                        "uid": user.uid,
                        "name": user.name,
                        "count": count,
                    }
                    request.session["userinfo"] = userinfo
                    return redirect("/shop/index")
                else:
                    return render(request,"login.html",{"msg":"用户名或者密码错误"})

            else:
                return render(request,"login.html",{"msg":"用户不存在"})

        else:
            return render(request,"login.html",{"msg":"错误的请求方式"})

#注册
def register(request):
    if request.method == "GET":
        return render(request,"register.html")
    elif request.method == "POST":
        username = request.POST.get("name")
        password = request.POST.get("password")
        user = User.objects.filter(name=username)
        if not user:
            User.objects.create(name=username,password=password,status=1)
            user = User.objects.filter(name=username).first()
            # count = ShopCar.objects.filter(uid=user.uid).count()
            userinfo = {
                "uid": user.uid,
                "name": user.name,
                "count": 0,
            }
            request.session["userinfo"] = userinfo
            return redirect("/shop/index/")
        else:
            return render(request,"register.html",{"msg":"用户已经存在"})
    else:
        return render(request,"register.html",{"msg":"错误的请求方式"})


#退出
def loginout(request):
    del request.session["userinfo"]   #删除session缓存中存储的信息
    return redirect("/shop/index/")
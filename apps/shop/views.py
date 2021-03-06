import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from tmall import settings
from tmall.settings import TEMP_MEDIA_URL
"""
创建自定义的apps
1.通过命令创建模块   startapp app_name
2.配置二级路由
2.1> 在apps下面新建一个urls.py文件
2.2> 在根目录的urls.py中使用include引入
注意:
如果项目比较大的,最好是在apps下面新建一个templates的文件夹
1>根目录的templates文件夹一般放一些公共的模板文件 母版 需要include的模板

配置项目后台管理
1> 导入xamdin 
2> 在setting中添加xamin项目 sys.path.insert(0,os.path.join(BASE_DIR,'xadmin'))
3> 导入xadmin需要的依赖包
3.1> 需要安装第三方的app   requirements
3.2> 通过命令  pip install requirements(如果已经安装可以跳过)
3.3> 先将xadmin下面的requirements.txt文件复制到工程中
3.4> 通过命令   pip install -r  目录/xxx.txt
     例如: pip install -r requirements/xadmin.txt
3.5 通过  pip list 查看是否安装成功
4> 注册
    # 必须
    'xadmin',
    'crispy_forms',
    # 可选
    # 扩展主题包
    'reversion'
5> 解决冲突
5.1> 在根目录在新建一个ext_apps
5.2> 将xmadin的源代码 赋值到 ext_apps下面
5.3> 将ext_apps 加入到项目 sys.path.insert(0, os.path.join(BASE_DIR, 'ext_apps'))
6> 使用xadmin代替django admin  
    在根urls.py中 
     url('xadmin/', xadmin.site.urls), 
7 系统表迁移
1> makemigrations
2> migrations

8>创建超级用户
python manage.py createsuperuser

9> 启动项目测试是否安装成功
9.1> http://127.0.0.1:8000/xadmin/
9.2> 使用第8步的账号密码登录

10> 定义全局的模板变量 
备注    当我们的每个界面都需要用到某些数据的时候 可以定义全局的
1>在项目的settings
MTV开发
1>在models中建立模型对象
2>迁移
t
v
"""
from .models import Navigation, Category, Banner, Shop, Property, PropertyValue, Review,SubMenu,SubMenu2

def index(request):
    navigations = Navigation.objects.all()
    # 查询一级分类菜单数据
    cate_list = Category.objects.all()
    # 动态语言 可以动态的添加属性
    for cate in cate_list:
        # 获取二级菜单的数据
        submenus = cate.submenu_set.all()
        for menu in submenus:
            # 将二级菜单对象的多条三级菜单数据绑定到 subs2属性
            menu.subs2 = menu.submenu2_set.all()
        cate.subs = submenus
        # 商品信息
        shops = cate.shop_set.all()
        for shop in shops:
            shop.image = shop.shopimage_set.filter(type='type_single').first()
        cate.shops = shops
    # 获取轮播图的数据
    banners = Banner.objects.all()
    # 获取商品信息
    # cate_shops = Category.objects.all()
    # for cate in cate_shops:
    #     shops = cate.shop_set.all()
    #     for shop in shops:
    #         shop.images = shop.shopimage_set.all()
    #     cate.shops = shops
    return render(request, 'index.html', {'navigations': navigations,
                                          'cate_list': cate_list,
                                          'banners': banners,
                                          })

def cate(request):
    result = {}
    # 需要把对象转化字典
    cates = Category.objects.all()
    cate_list = []
    # 对象要转化成字典 cate-----> 字典
    for cate in cates:
        menus = cate.submenu_set.all()  # QS
        li = []
        # 将二级菜单的数据转化字典  submenu--->字典
        for menu in menus:
            li2 = []
            for menu2 in menu.submenu2_set.all():
                li2.append(model_to_dict(menu2))
            menu.subs2 = li2
            li.append(model_to_dict(menu))
        cate.subs = li
        cate_list.append(model_to_dict(cate))

    result.update(status=200, msg='success', data=cate_list)
    return HttpResponse(json.dumps(result), content_type='application/json')

def model_to_dict(model):
    # vars(对象)获取对象所有的属性
    dic = {}
    keys = vars(model).keys()
    for key in keys:
        if not key.startswith('_'):
            if isinstance(getattr(model, key), datetime.date):
                getattr(model, key).strtime('%Y-%m-%d')
            elif isinstance(getattr(model, key), datetime.datetime):
                dic[key] = getattr(model, key).strtime('%Y-%m-%d %H%m%s')
            else:
                # getattr(key) 获取属性的值
                dic[key] = getattr(model, key)
    return dic


def shop_detail(request, sid):
    shop = Shop.objects.get(pk=int(sid))
    shop.imgs = shop.shopimage_set.all()
    # 通过分类菜单获取商品的参数
    properties = Property.objects.filter(cate_id=shop.cate.cate_id)
    for property in properties:
        # 获取商品的参数通过shop_id 商品 propertyvalue
        property.value = PropertyValue.objects.filter(property=property, shop=shop).first()
    # 获取商品的评论信息
    reviews = Review.objects.filter(shop=shop)
    return render(request, 'shop_page.html', {'shop': shop, 'properties': properties, 'reviews': reviews})

def search(request):
    key = request.POST.get('keyword')
    shops = Shop.objects.filter(name__icontains=key)
    for shop in shops:
        # select  * from  shop_img  where type='type_single'
        shop.images = shop.shopimage_set.filter(type='type_single').values('shop_img_id', 'shop_id')
        shop.count = shop.review_set.count()
    return render(request, 'shop_page.html', {'shops': shops})

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html');

def loginout(request):
    del request.session["userinfo"]   #删除session缓存中存储的信息
    return redirect("/shop/index/")


from django import template
#实例化模板注册器
register = template.Library()

#使用过滤器来进行注册
@register.filter
def get_ride_num(x,y):
    """
    计算两个值相乘
    :param x:
    :param y:
    :return:
    """
    return int(x) * int(y)


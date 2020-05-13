from django.http import JsonResponse
from django.db.models import F
from django.db import IntegrityError, transaction

# 导入 Order 对象定义
from common.models import Order, OrderMedicine

import json


def dispatcher(request):
    # 根据session判断用户是否是登录的管理员用户
    if 'usertype' not in request.session:
        return JsonResponse({
            'ret': 302,
            'msg': '未登录',
            'redirect': '/mgr/sign.html'},
            status=302)

    if request.session['usertype'] != 'mgr':
        return JsonResponse({
            'ret': 302,
            'msg': '用户非mgr类型',
            'redirect': '/mgr/sign.html'},
            status=302)

    # 将请求参数统一放入request 的 params 属性中，方便后续处理

    # GET请求 参数 在 request 对象的 GET属性中
    if request.method == 'GET':
        request.params = request.GET

    # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
    elif request.method in ['POST', 'PUT', 'DELETE']:
        # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
        request.params = json.loads(request.body)

    # 确保action有被赋值
    action = request.params.get('action', None)
    if not action:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})

    # 根据不同的action分派给不同的函数进行处理
    if action == 'list_order':
        return listorder(request)
    elif action == 'add_order':
        return addorder(request)

    # 订单 暂 不支持修改 和删除

    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


def addorder(request):
    info = request.params['data']

    # 从请求消息中 获取要添加订单的信息
    # 并且插入到数据库中

    with transaction.atomic():
        new_order = Order.objects.create(name=info['name'],
                                         customer_id=info['customerid'])

        batch = [OrderMedicine(order_id=new_order.id, medicine_id=mid, amount=1)
                 for mid in info['medicineids']]
        OrderMedicine.objects.bulk_create(batch)

    return JsonResponse({'ret': 0, 'id': new_order.id})


def listorder(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = Order.objects\
            .annotate(
                customer_name=F('customer__name'),
                medicines_name=F('medicines__name')
            )\
            .values(
                'id','name','create_date','customer_name','medicines_name'
            )

    # 将 QuerySet 对象 转化为 list 类型
    retlist = list(qs)

    # 可能有 ID相同，药品不同的订单记录， 需要合并
    newlist = []
    id2order = {}
    for one in retlist:
        orderid = one['id']
        if orderid not in id2order:
            newlist.append(one)
            id2order[orderid] = one
        else:
            id2order[orderid]['medicines_name'] += ' | ' + one['medicines_name']

    return JsonResponse({'ret': 0, 'retlist': newlist})

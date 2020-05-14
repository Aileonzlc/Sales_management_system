from django.http import JsonResponse
from django.db.models import F
from django.db import transaction

# 导入 Order 对象定义
from common.models import Order, OrderMedicine
import traceback
import json


# def dispatcher(request):
#     # 根据session判断用户是否是登录的管理员用户
#     if 'usertype' not in request.session:
#         return JsonResponse({
#             'ret': 302,
#             'msg': '未登录',
#             'redirect': '/mgr/sign.html'},
#             status=302)
#
#     if request.session['usertype'] != 'mgr':
#         return JsonResponse({
#             'ret': 302,
#             'msg': '用户非mgr类型',
#             'redirect': '/mgr/sign.html'},
#             status=302)
#
#     # 将请求参数统一放入request 的 params 属性中，方便后续处理
#
#     # GET请求 参数 在 request 对象的 GET属性中
#     if request.method == 'GET':
#         request.params = request.GET
#
#     # POST/PUT/DELETE 请求 参数 从 request 对象的 body 属性中获取
#     elif request.method in ['POST', 'PUT', 'DELETE']:
#         # 根据接口，POST/PUT/DELETE 请求的消息体都是 json格式
#         request.params = json.loads(request.body)
#
#     # 确保action有被赋值
#     action = request.params.get('action', None)
#     if not action:
#         return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})
#
#     # 根据不同的action分派给不同的函数进行处理
#     if action == 'list_order':
#         return listorder(request)
#     elif action == 'add_order':
#         return addorder(request)
#
#     # 订单 暂 不支持修改 和删除
#
#     else:
#         return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


def addorder(request):
    info = request.params['data']
    with transaction.atomic():
        medicinelist = info['medicinelist']
        new_order = Order.objects.create(name=info['name'],
                                         customer_id=info['customerid'],
                                         # 写入json格式的药品数据到 medicinelist 字段中
                                         medicinelist=json.dumps(medicinelist, ensure_ascii=False), )

        batch = []
        for medicine in medicinelist:
            batch.append(OrderMedicine(order_id=new_order.id,
                                       medicine_id=medicine['id'],
                                       amount=medicine['amount']))

        OrderMedicine.objects.bulk_create(batch)

    return JsonResponse({'ret': 0, 'id': new_order.id})


# 增加对分页的支持
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q


def listorder(request):
    try:
        # 返回一个 QuerySet 对象 ，包含所有的表记录
        qs = Order.objects \
            .annotate(customer_name=F('customer__name'), ) \
            .values('id', 'name', 'create_date', 'customer_name', 'medicinelist') \
            .order_by('-id')

        # 查看是否有 关键字 搜索 参数
        keywords = request.params.get('keywords', None)
        if keywords:
            conditions = [Q(name__contains=one) for one in keywords.split(' ') if one]
            query = Q()
            for condition in conditions:
                query &= condition
            qs = qs.filter(query)

        # 要获取的第几页
        pagenum = request.params['pagenum']

        # 每页要显示多少条记录
        pagesize = request.params['pagesize']

        # 使用分页对象，设定每页多少条记录
        pgnt = Paginator(qs, pagesize)

        # 从数据库中读取数据，指定读取其中第几页
        page = pgnt.page(pagenum)

        # 将 QuerySet 对象 转化为 list 类型
        retlist = list(page)

        # total指定了 一共有多少数据
        return JsonResponse({'ret': 0, 'retlist': retlist, 'total': pgnt.count})
    except EmptyPage:
        return JsonResponse({'ret': 0, 'retlist': [], 'total': 0})
    except Exception:
        return JsonResponse({'ret': 2, 'msg': f'未知错误\n{traceback.format_exc()}'})


def deleteorder(request):
    # 获取订单ID
    oid = request.params['id']
    try:
        one = Order.objects.get(id=oid)
        with transaction.atomic():

            # 一定要先删除 OrderMedicine 里面的记录
            OrderMedicine.objects.filter(order_id=oid).delete()
            # 再删除订单记录
            one.delete()

        return JsonResponse({'ret': 0, 'id': oid})

    except Order.DoesNotExist:
        return JsonResponse({
            'ret': 1,
            'msg': f'id 为`{oid}`的订单不存在'
        })
    except:
        err = traceback.format_exc()
        return JsonResponse({'ret': 1, 'msg': err})


from lib.handler import dispatcherBase

Action2Handler = {
    'list_order': listorder,
    'add_order': addorder,
    'delete_order': deleteorder,
}


def dispatcher(request):
    return dispatcherBase(request, Action2Handler)

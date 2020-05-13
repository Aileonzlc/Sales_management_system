from django.http import JsonResponse

# 导入 Medicine 对象定义
from common.models import Medicine

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
    if action == 'list_medicine':
        return listmedicine(request)
    elif action == 'add_medicine':
        return addmedicine(request)
    elif action == 'modify_medicine':
        return modifymedicine(request)
    elif action == 'del_medicine':
        return deletemedicine(request)

    else:
        return JsonResponse({'ret': 1, 'msg': '不支持该类型http请求'})


def listmedicine(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = Medicine.objects.values()

    # 将 QuerySet 对象 转化为 list 类型
    # 否则不能 被 转化为 JSON 字符串
    retlist = list(qs)

    return JsonResponse({'ret': 0, 'retlist': retlist})


def addmedicine(request):
    info = request.params['data']

    # 从请求消息中 获取要添加客户的信息
    # 并且插入到数据库中
    medicine = Medicine.objects.create(name=info['name'],
                                       sn=info['sn'],
                                       desc=info['desc'])
    return JsonResponse({'ret': 0, 'id': medicine.id})


def modifymedicine(request):
    # 从请求消息中 获取修改客户的信息
    # 找到该客户，并且进行修改操作

    medicineid = request.params['id']
    newdata = request.params['newdata']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        medicine = Medicine.objects.get(id=medicineid)
    except Medicine.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{medicineid}`的药品不存在'
        }

    if 'name' in newdata:
        medicine.name = newdata['name']
    if 'sn' in newdata:
        medicine.sn = newdata['sn']
    if 'desc' in newdata:
        medicine.desc = newdata['desc']

    # 注意，一定要执行save才能将修改信息保存到数据库
    medicine.save()

    return JsonResponse({'ret': 0})


def deletemedicine(request):
    medicineid = request.params['id']

    try:
        # 根据 id 从数据库中找到相应的药品记录
        medicine = Medicine.objects.get(id=medicineid)
    except Medicine.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id 为`{medicineid}`的客户不存在'
        }

    # delete 方法就将该记录从数据库中删除了
    medicine.delete()

    return JsonResponse({'ret': 0})

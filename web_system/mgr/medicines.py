from django.http import JsonResponse

# 导入 Medicine 对象定义
from common.models import Medicine

import json


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


from lib.handler import dispatcherBase

Action2Handler = {
    'list_medicine': listmedicine,
    'add_medicine': addmedicine,
    'modify_medicine': modifymedicine,
    'del_medicine': deletemedicine,
}

def dispatcher(request):
    return dispatcherBase(request, Action2Handler)


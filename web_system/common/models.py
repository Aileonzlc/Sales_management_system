from django.db import models


# Create your models here.
class Customer(models.Model):
    # 客户名称
    name = models.CharField(max_length=200)

    # 联系电话
    phonenumber = models.CharField(max_length=200)

    # 地址
    address = models.CharField(max_length=200)
    # #  qq
    # QQ = models.CharField(max_length=20, null=True, blank=True, default='NO')


class Medicine(models.Model):
    # 药品名
    name = models.CharField(max_length=200)
    # 药品编号
    sn = models.CharField(max_length=200)
    # 描述
    desc = models.CharField(max_length=200)


import datetime


class Order(models.Model):
    # 订单名
    name = models.CharField(max_length=200, null=True, blank=True)
    # 创建日期
    create_date = models.DateTimeField(default=datetime.datetime.now)
    # 客户
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    # 订单购买的药品，和Medicine表是多对多 的关系,多对多关系 是 通过另外一张表， 也就是 through 参数 指定的 OrderMedicine 表 来确定的。
    medicines = models.ManyToManyField(Medicine, through='OrderMedicine')

    # 为了提高效率，这里存放 订单 medicines 冗余数据
    medicinelist = models.CharField(max_length=2000, null=True, blank=True)


class OrderMedicine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)

    # 订单中药品的数量
    amount = models.PositiveIntegerField()

# 国家表
class Country(models.Model):
    name = models.CharField(max_length=100)

# 学生表， country 字段是国家表的外键，形成一对多的关系
class Student(models.Model):
    name = models.CharField(max_length=100)
    grade = models.PositiveSmallIntegerField()
    country = models.ForeignKey(Country,
                                on_delete=models.PROTECT)
from django.urls import path

from . import customers, medicines, order
from . import sign_in_out

urlpatterns = [
    # 注意customers后没有加/，代表是api/mgr/customers....形式的url，加了/就是api/mgr/customers/....形式的url
    path('customers', customers.dispatcher),
    path('medicines', medicines.dispatcher),
    path('orders', order.dispatcher),
    path('signin', sign_in_out.signin),
    path('signout', sign_in_out.signout),
]
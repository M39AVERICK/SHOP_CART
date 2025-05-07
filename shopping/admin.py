from django.contrib import admin
from shopping.models import PRODUCT,Contact,Orders,OrderUpdate


admin.site.register(PRODUCT)
admin.site.register(Contact)
# Register your models here.


from django.contrib import admin
from .models import Orders, OrderUpdate

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'name', 'email', 'paymentstatus', 'amount']
    search_fields = ['name', 'email', 'oid']
    list_filter = ['paymentstatus', 'shipment_date']

@admin.register(OrderUpdate)
class OrderUpdateAdmin(admin.ModelAdmin):
    list_display = ['order', 'update_desc', 'timestamp', 'delivered']
    search_fields = ['update_desc']

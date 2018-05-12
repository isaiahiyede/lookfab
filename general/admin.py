from __future__ import unicode_literals

from django.contrib import admin
from models import UserAccount, Category, Item, Payments, OrderItem, Packages, PackageInvoice, CostSetting


# Register your models here.


# Register your models here.
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('user','created_on','phone_number','profile_updated',)
    search_fields = ['user__email','created_on','phone_number','profile_updated', ]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    search_fields = ['category_name', ]

class PackagesAdmin(admin.ModelAdmin):
    list_display = ('user','tracking_number','created_on','status','payment_status','shipping_status',)
    search_fields = ['user__user__email','tracking_number','created_on','status','payment_status','shipping_status',]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('name','created_on')
    search_fields = ['name', 'created_on']


admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item)
admin.site.register(PackageInvoice)
admin.site.register(Payments)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Packages,PackagesAdmin)
admin.site.register(CostSetting)
# Register your models here.

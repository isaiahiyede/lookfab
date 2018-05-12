from django.conf.urls import patterns, include, url
from django.conf import settings
import views

urlpatterns = [
			url(r'^paystackpay/$',views.mainPay, name="mainPay"),
            url(r'^verify_payment/$', views.verify_payment, name='verify_payment'),
            # url(r'^signup/Page/$', views.register,  name="register"),
            # url(r'^login/Page/$', views.user_login,  name="login"),
            # url(r'^user-logout/$', views.user_logout,  name="logout"),
            # url(r'^admin-page/$', views.admin,  name="admin"),
            # url(r'^all-orders/$',views.all_orders, name = "all_orders"),
            # url(r'^all-payments/$',views.all_payments, name = "all_payments"),
            # url(r'^add-item/$',views.add_item, name = "add_item"),
            # url(r'^new-category/$',views.add_category, name = "add_category"),
            # url(r'^delete-item/(?P<pk>[-\w]+)/$',views.delete_item, name = "delete_item"),
            # url(r'^get-item/$',views.getItem, name = "get_item"),
            # url(r'^edit-item/$',views.edit_item, name = "edit_item"),
            # url(r'^shoppingCart/$',views.view_cart, name = "view_cart"),
            # url(r'^categoryLive/(?P<value>.+)$',views.getLiveCategory, name = "getLiveCategory"),
            # url(r'^categoryPassed/(?P<value>.+)$',views.getPassedCategory, name = "getPassedCategory"),
            # url(r'^confirm-order/$',views.get_confirmation_order, name = "get_confirmation_order"),
            # url(r'^Contact-us/$',views.contact, name = "contact"),
            # url(r'^customer-list/$',views.all_customers, name = "all_customers"),
            # url(r'^userComment/$',views.user_comment, name = "user_comment"),
            # url(r'^search-results/(?P<action>[-\w]+)/$',views.user_search, name = "user_search"),
            # url(r'^remove-from-cart/(?P<item_pk>[-\w]+)/$',views.remove_from_cart, name = "remove_from_cart"),
            # url(r'cart-box/$',views.cart_box, name = "cart_box"),
            # url(r'^items/(?P<category>[-\w]+)/$',views.allStoreItems, name = "all-items"),
            # url(r'^details/(?P<slug>[-\w]+)/(?P<pk>.+)/$',views.itemDetails, name = "item_details"),
            # url(r'^storeitems/(?P<category>[-\w]+)/(?P<subcategory>[-\w]+)/$',views.storeItems, name = "store-items"),
            # url(r'invoice/(?P<tracking_id>.+)/$', views.package_invoice_page, name="package_invoice"),
            # url(r'^calculator/$', calculator, name ="calculator"),
            # url(r'^export/csv/$', export_csv, name='export_csv'),
            # url(r'^staff-login-access/$', views.staff_login_access, name="staff_login_access"),
            # url(r'^customer-orders/$', views.customer_orders, name="all_customer_orders"),
            # url(r'^packages/$', views.customer_packages, name="all_customer_packages"),
            # url(r'^vendor/play/$', views.get_play_event, name="get_play_event"),   
            # url(r'^export/tradingDetails/(?P<useracc_obj>[-\w]+)/$', views.tradingDetails, name='tradingDetails'),
            # url(r'^closing/djp/$', views.close_djp_client, name="close_djp_client"),
            # url(r'^confirm_paypal_payment/$', views.confirm_paypal_payment, name="confirm_paypal_payment"),

            
]


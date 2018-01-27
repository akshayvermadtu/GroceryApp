from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/', views.UserSignUp.as_view()),
    url(r'^login/', views.UserLogIn.as_view()),
    url(r'^boyLogin/', views.DeliveryBoyLogIn.as_view()),
    url(r'^items/', views.GetItem.as_view()),
    url(r'^showCat/', views.ViewCategories.as_view()),
    url(r'^showSubCat/', views.ViewSubCategories.as_view()),
    url(r'^showCart/', views.ShowCart.as_view()),
    url(r'^addCart/', views.AddCart.as_view()),
    url(r'^placeOrder/', views.PlaceOrder.as_view()),
    url(r'^viewOrders/', views.ViewOrders.as_view()),
    url(r'^viewPendingOrders/', views.ViewPendingOrders.as_view()),
    url(r'^viewDeliveredOrders/', views.ViewDeliveredOrders.as_view()),
    url(r'^viewProgressOrders/', views.ViewProgressOrders.as_view()),
    url(r'^removeCart/', views.RemoveFromCart.as_view()),
    url(r'^myDetails/', views.MyDetails.as_view()),
    url(r'^myOrders/', views.MyOrders.as_view()),
    url(r'^search/', views.SearchItems.as_view()),
    url(r'^editItem/', views.EditItemDetails.as_view()),
    url(r'^revenue/', views.Revenue.as_view()),
    url(r'^changeStatus/', views.ChangeStatus.as_view()),
    url(r'^forwardOrder/', views.ForwardOrder.as_view()),
    url(r'^myBoys/', views.DeliveryBoyDetails.as_view()),
    url(r'^boyOrders/', views.DeliveryBoyOrders.as_view()),
    url(r'^locationUpdate/', views.DelivererLocation.as_view()),
    url(r'^bill/', views.NetBillAmount.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

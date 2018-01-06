from django.conf.urls import url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/', views.UserResponse.as_view()),
    url(r'^login/', views.UserCheck.as_view()),
    url(r'^items/', views.GetItem.as_view()),
    url(r'^showCat/', views.ViewCategories.as_view()),
    url(r'^showSubCat/', views.ViewSubCategories.as_view()),
    url(r'^showCart/', views.ShowCart.as_view()),
    url(r'^addCart/', views.AddCart.as_view()),
    url(r'^image/', views.image),
    url(r'^placeOrder/', views.PlaceOrder.as_view()),
    url(r'^viewOrders/', views.ViewOrders.as_view()),
    url(r'^removeCart/', views.RemoveFromCart.as_view()),
    url(r'^myDetails/', views.MyDetails.as_view()),
    url(r'^myOrders/', views.MyOrders.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

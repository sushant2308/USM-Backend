
from django.urls import path
from rest_framework import views
from . import views
urlpatterns = [
    
    path('all/', views.OrderedList.as_view(),name="AllCustomer"),
    path('all/<slug:slug>/',views.api_list_customer_view,name="api_list_customer_view"),
    path('all/filter/team/<slug:slug>/', views.api_customer_filter_team_view,name="AllCustomer"),
    path('all/filter/label/<slug:slug>/', views.api_customer_filter_label_view,name="AllCustomer"),
    path('all/filter/firsttag/<slug:slug>/', views.api_customer_filter_firsttag_view,name="AllCustomer"),
    path('customer_detail/<slug:slug>/', views.api_detail_customer_view,name="Customer_detail"),
    path('customer_comments/<slug:slug>/', views.api_all_customer_comment_view,name="Customer_Comments"),
    path('create_customer_comment/<slug:slug>/', views.api_create_customer_comment_view,name="create_Comments"),
    path('create_customer/<slug:slug>/', views.api_create_customer_view,name="Customer_create"),
    path('login/', views.GoogleSocialAuthView.as_view(),name="login"),
    path('user_detail/<slug:slug>/',views.api_detail_employee_view,name='user'),
    path('user_update/<slug:slug>/',views.api_update_employee_view,name='update'),
    path('data_detail/<slug:slug>/',views.api_detail_data_view,name='update')
]
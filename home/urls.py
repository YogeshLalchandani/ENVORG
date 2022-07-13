from django.contrib import admin
from django.urls import path
from home import views



urlpatterns = [
    path("",views.index,name='home'),
    path("about",views.about,name='about'),
    path("do",views.do,name='do'),
    path("projects",views.projects,name='projects'),
    path("blog",views.blog,name='blog'),
    path("contact",views.contact,name='contact'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path("donation",views.donation,name='donation'),
    
]
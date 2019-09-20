# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
__author__ = 'qing.li'
"""
from django.conf.urls import url
from crm import views

urlpatterns = [
    url('^login/', view=views.login, name='login'),
    url('^index/', view=views.index, name='index'),
    url('^reg/', view=views.register, name='register'),
    url('^checkUser/', views.check_name, name='check_name'),
]
# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
__author__ = 'qing.li'
"""
from django.conf.urls import url, include
from rbac import views

urlpatterns = [
    url(r'^role/list/', views.role_list, name='role_list'),
    url(r'^role/add/', views.role, name='role_add'),
    url(r'^role/edit/(?P<role_id>\d+)', views.role, name='role_edit'),
    url(r'^role/del/(?P<role_id>\d+)', views.role_del, name='role_del'),

    url(r'^menu/list/', views.menu_list, name='menu_list'),
    url(r'^menu/add/', views.menu, name='menu_add'),
    url(r'^menu/edit/(?P<edit_id>\d+)', views.menu, name='menu_edit'),
    url(r'^menu/del/(?P<del_id>\d+)', views.menu_del, name='menu_del'),

    url(r'^permission/add/', views.permission, name='permission_add'),
    url(r'^permission/edit/(?P<edit_id>\d+)', views.permission, name='permission_edit'),
    url(r'^permission/del/(?P<del_id>\d+)', views.permission_del, name='permission_del'),

    url(r'^user/list/', views.user_list, name='user_list'),
    url(r'^user/add/', views.user, name='user_add'),
    url(r'^user/edit/(?P<edit_id>\d+)', views.user, name='user_add'),
    url(r'^multi/permissions/', views.multi_permissions, name='multi_permissions'),
]
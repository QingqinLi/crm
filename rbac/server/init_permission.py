# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
__author__ = 'qing.li'
"""
from django.conf import settings


# 解耦
def init_permission(user, request):
    # 查询当前登录用户有的权限, 跨表查询
    permission_query = user.user.roles.all().filter(permissions__url__isnull=False).values('permissions__url',
                                                                                      'permissions__title',
                                                                                      'permissions__name',
                                                                                      'permissions__menu_id',
                                                                                      'permissions__menu__title',
                                                                                      'permissions__menu__icon',
                                                                                      'permissions__menu__weight',
                                                                                      'permissions__parent_id',
                                                                                      'permissions__id',
                                                                                      'permissions__parent__name',
                                                                                      ).distinct()
    permission_dict = {}
    # 存在菜单信息
    menu = {}
    for i in permission_query:
        permission_dict[i['permissions__name']] = {'url': i['permissions__url'],
                                                   'pid': i['permissions__parent_id'],
                                                   'id': i['permissions__id'],
                                                   'title': i['permissions__title'],
                                                   'pname': i['permissions__parent__name'],
                                                   }
        if i['permissions__menu_id']:
            # 用字典，查询速度快
            # if menu_list
            if i['permissions__menu_id'] in menu:
                menu[i['permissions__menu_id']]['children'].append(
                    dict(url=i['permissions__url'], title=i['permissions__title'],
                         id=i['permissions__id']))
            else:
                menu[i['permissions__menu_id']] = {'title': i['permissions__menu__title'],
                                                   'icon': i['permissions__menu__icon'],
                                                   'id': i['permissions__id'],
                                                   'weight': i['permissions__menu__weight'],
                                                   'children': [{'url': i['permissions__url'],
                                                                 'title': i['permissions__title'],
                                                                 'id': i['permissions__id'],
                                                                 }]
                                                   }
            # menu_list.append({'url': i['permissions__url'], 'menu': i['permissions__menu__title'],
            #                   'title': i['permissions__title']})

    # 过滤空权限，重复权限
    # 将权限信息写入session,会自动进行序列化, permission_list应该是可配置的，setting
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
    request.session[settings.MENU_SESSION_KEY] = menu

# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
__author__ = 'qing.li'
"""
from django.http import QueryDict
from django.db.models import Q


def get_url(request):
    url = request.get_full_path()
    qd = QueryDict()
    qd._mutable = True
    qd['next_page'] = url
    # query_params = qd.urlencode()

    return qd


def get_query_condition(request, query_list):
    query = request.GET.get("query", '')
    q = Q()
    q.connector = 'OR'
    for i in query_list:
        q.children.append(Q(('{}__icontains'.format(i), query)))

    return q
# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
__author__ = 'qing.li'
"""
from django.http import QueryDict
from django.utils.safestring import mark_safe


# 封装分页，显示
class Pagination:
    def __init__(self, request, num, max_page, show_data, query_params=QueryDict()):
        self.query_params = query_params
        self.query_params._mutable = True
        try:
            current_page = int(request.GET.get('page'))
        except TypeError:
            current_page = 1

        if divmod(len(show_data), num)[1] == 0:
            end = len(show_data) // num
        else:
            end = len(show_data) // num + 1
        range_start = current_page - max_page//2
        range_end = current_page + max_page // 2
        if range_start < 1:
            range_start = 1
            if range_end > end:
                range_end = end
            else:
                range_end = max_page
        if range_end > end:
            range_end = end
            if range_start < 1:
                range_start = 1
            else:
                range_start = range_end - max_page + 1

        page = range(range_start, range_end + 1)

        data = show_data[(current_page - 1) * num:current_page * num]
        if current_page == 1:
            previous = 1
            if current_page == end:
                next = current_page
            else:
                next = current_page + 1
        elif current_page == end:
            if current_page == 1:
                previous = 1
            else:
                previous = current_page - 1
            next = current_page
        else:
            previous = current_page - 1
            next = current_page + 1
        self.data = data
        self.page = page
        self.previous = previous
        self.next = next
        self.current_page = current_page
        self.base_url = request.path_info
        self.end = end

    @property
    def show_list(self):
        return self.data

    @property
    def show_li(self):
        # 存放li标签的列表
        html_list = []

        self.query_params['page'] = 1
        # query=alex&page=1

        first_li = '<li><a href="{}?{}">首页</a></li>'.format(self.base_url, self.query_params.urlencode())
        html_list.append(first_li)

        if self.current_page == 1:
            prev_li = '<li class="disabled"><a><<</a></li>'
        else:
            self.query_params['page'] = self.current_page - 1
            prev_li = '<li><a href="{0}?{1}"><<</a></li>'.format(self.base_url, self.query_params.urlencode())
        html_list.append(prev_li)

        for num in self.page:
            self.query_params['page'] = num
            if self.current_page == num:
                li_html = '<li class="active"><a href="{0}?{1}">{2}</a></li>'.format(self.base_url,
                                                                                     self.query_params.urlencode(), num)
            else:
                li_html = '<li><a href="{0}?{1}">{2}</a></li>'.format(self.base_url,
                                                                      self.query_params.urlencode(), num)
            html_list.append(li_html)

        if self.current_page == self.end:
            next_li = '<li class="disabled"><a>>></a></li>'
        else:
            self.query_params['page'] = self.current_page + 1
            next_li = '<li><a href="{0}?{1}">>></a></li>'.format(self.base_url, self.query_params.urlencode())

        html_list.append(next_li)

        self.query_params['page'] = self.end
        last_li = '<li><a href="{0}?{1}">尾页</a></li>'.format(self.base_url, self.query_params.urlencode())
        html_list.append(last_li)

        return mark_safe(''.join(html_list))
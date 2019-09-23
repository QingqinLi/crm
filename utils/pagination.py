# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
__author__ = 'qing.li'
"""


# 封装分页，显示
class Pagination:
    def __init__(self, request, num, max_page, show_data):
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

    def show_list(self):

        data = {
            "data": self.data,
            "page": self.page,
            "previous": self.previous,
            "next": self.next,
        }

        return data
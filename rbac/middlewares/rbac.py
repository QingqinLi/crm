from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import HttpResponse
import re


# class PermissionMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         # 对权限进行校验
#         # 1. 当前访问的URL
#         current_url = request.path_info
#
#         # 白名单的判断
#         for i in settings.WHITE_URL_LIST:
#             if re.match(i,current_url):
#                 return
#
#         # 2. 获取当前用户的所有权限信息
#
#         permission_list = request.session.get(settings.PERMISSION_SESSION_KEY)
#         # 3. 权限的校验
#         print(current_url)
#
#         for item in permission_list:
#             url = item[0]
#             if re.match("^{}$".format(url), current_url):
#                 return
#         else:
#             return HttpResponse('没有权限')

class PermissionMiddle(MiddlewareMixin):
    def process_request(self, request):
        #  对权限进行校验，1、当前访问的url，白名单的判断 2、获取当前用户的所有权限信息，3、权限的校验
        url = request.path_info
        permission_list = request.session.get(settings.PERMISSION_SESSION_KEY)
        request.breadcrumb_list = [
            {
                'title': '首页',
                'url': '#',
            }
        ]
        for white in settings.WHITE_URL_LIST:
            if re.match(white, url):
                return
        print(permission_list)
        for item in permission_list.values():

            my_url = item['url']

            if re.match(my_url, url):

                if item['pid']:
                    request.current_menu_id = item['pid']
                    request.breadcrumb_list.append({
                        'title': permission_list[item['pname']]['title'],
                        'url': permission_list[item['pname']]['url'],
                    })
                else:
                    request.current_menu_id = item['id']
                request.breadcrumb_list.append({
                    'title': item['title'],
                    'url': item['url'],
                })

                print(request.breadcrumb_list)
                return
        # if [url] in permission_list:
        #     return
        else:
            return HttpResponse('无访问权限')

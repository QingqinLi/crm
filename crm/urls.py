# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
__author__ = 'qing.li'
"""
from django.conf.urls import url
from crm.views import consultant_views, teacher_views

urlpatterns = [
    # url('^login/', view=consultant_views.login, name='login'),
    url('^index/', view=consultant_views.index, name='index'),
    url('^reg/', view=consultant_views.register, name='register'),
    url('^checkUser/', consultant_views.check_name, name='check_name'),
    url('^customer_list/', view=consultant_views.Customer.as_view(), name="customer"),
    # url('^customer_list/', views.user_list, name="customer"),
    url('^customer/add/', view=consultant_views.add_customer, name="add_customer"),
    url('^my_customer/', view=consultant_views.Customer.as_view(), name="my_customer"),
    url('^customer/edit/(\d+)', view=consultant_views.edit_customer, name="edit_customer"),


    # 跟进记录
    # 展示跟进记录
    url('^consult_record_list/', consultant_views.ConsultRecord.as_view(), name='consult_record'),
    # 添加跟进记录
    url('^consult_record/add/', consultant_views.add_consult_record, name='add_consult_record'),
    url('^consult_record/edit/(?P<consult_record_id>\d+)', consultant_views.edit_consult_record, name='edit_consult_record'),

    # 报名记录
    # 展示报名记录
    url('^enrollment_list/(?P<student_id>\d+)', consultant_views.Enrollment.as_view(), name='enrollment'),
    url('^enrollment/add/(?P<student_id>\d+)', consultant_views.enrollment, name='add_enrollment'),
    url('^enrollment/edit/(?P<edit_id>\d+)', consultant_views.enrollment, name='edit_enrollment'),

    # 班主任
    # 班级的管理
    url('^class_list/', teacher_views.Classes.as_view(), name='classes'),
    url('^class/add/', teacher_views.classes, name='add_class'),
    url('^class/edit/(?P<class_id>\d+)', teacher_views.classes, name='edit_class'),

    # 课程的管理
    url('^course_list/(?P<class_id>\d+)', teacher_views.Course.as_view(), name='course'),
    url('^course/add/(?P<class_id>\d+)', teacher_views.course, name='add_course'),
    url('^course/edit/(?P<course_id>\d+)', teacher_views.course, name='edit_course'),

    # 学习记录的管理
    url('^study_record_list/(?P<course_id>\d+)', teacher_views.study_record, name='study_record'),
    url('^study_record/', teacher_views.study_record_list, name='study_record_list'),



]
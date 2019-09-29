# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
__author__ = 'qing.li'
"""
from django.views import View
from django.shortcuts import HttpResponse, redirect, reverse, render
from crm.form.teacher_form import Class, CourseForm, StudyRecordForm
from crm import models
from django.http import QueryDict
from utils.pagination import Pagination
from django.db.models import Q
from utils.get_utils import get_query_condition, get_url
from django.forms import modelformset_factory


class Classes(View):
    def get(self, request):
        query_list = ['course', 'semester']
        q = get_query_condition(request, query_list)
        # class_obj = request.user.classlist_set.all()
        class_obj = models.ClassList.objects.filter(q, teachers=request.user)
        query_params = request.GET.copy()

        next_url = get_url(request)
        print(next_url)
        c = Pagination(request, 10, 10, class_obj, query_params)
        class_data = c.show_li
        # class_obj = models.ClassList.objects.filter(teachers=request.user)
        return render(request, 'crm/teacher/class_list.html', {'data': c.show_list,
                                                               'page': class_data,
                                                               'next_url': next_url})

    def post(self, request):
        pass


def classes(request, class_id=None):
    class_obj = models.ClassList.objects.filter(id=class_id).first()
    form_obj = Class(instance=class_obj)
    if request.method == 'POST':
        form_obj = Class(request.POST, instance=class_obj)
        if form_obj.is_valid():
            form_obj.save()
            next = request.GET.get("next_page")
            print("next", next)
            if next:
                return redirect(next)
            return redirect(reverse("crm:classes"))
    return render(request, 'crm/teacher/class_add.html', {'form_obj': form_obj,
                                                          })


class Course(View):

    def get(self, request, class_id):
        if class_id == '0':
            course_obj = models.CourseRecord.objects.all()
        else:
            course_obj = models.CourseRecord.objects.filter(re_class_id=class_id)
        query_params = get_url(request)
        next_url = query_params.urlencode()
        c = Pagination(request, 5, 10, course_obj, query_params)
        page = c.show_li
        data = c.show_list
        return render(request, 'crm/teacher/course_list.html', {'data': data,
                                                                'page': page,
                                                                'next_url': next_url,
                                                                'class_id': class_id,

                                                                })

    def post(self, request, class_id):
        action = request.POST.get('action')

        print(action)
        if not hasattr(self, action):
            return HttpResponse("illegal operation")
        ret = getattr(self, action)()

        if ret:
            return ret
        else:
            return self.get(request, class_id)

    def multi_init(self):
        """
        根据当前提交的课程id批量初始化学生的学习记录
        :return:
        """
        course_ids = self.request.POST.getlist('id')
        course_obj_list = models.CourseRecord.objects.filter(id__in=course_ids)

        for course in course_obj_list:
            all_student = course.re_class.customer_set.filter(status='studying')
            student_list = []
            for student in all_student:
                student_list.append(models.StudyRecord(course_record=course, student=student))
            models.StudyRecord.objects.bulk_create(student_list)


def course(request, class_id=None, course_id=None):
    course_obj = models.CourseRecord.objects.filter(id=course_id).first() or models.CourseRecord(
        re_class_id=class_id,
        teacher=request.user)
    # 在内存中创建 没有保存写进数据库中
    form_obj = CourseForm(instance=course_obj)
    if request.method == 'POST':
        form_obj = CourseForm(request.POST, instance=course_obj)
        if form_obj.is_valid():
            form_obj.save()
            next = request.GET.get('next_page')
            if next:
                return redirect(next)
            return redirect(reverse('crm:course'))
    return render(request, 'crm/teacher/course_add.html', {'form_obj': form_obj,
                                                           })


def study_record(request, course_id):
    FormSet = modelformset_factory(models.StudyRecord, StudyRecordForm, extra=0)
    queryset = models.StudyRecord.objects.filter(course_record_id=course_id)
    form_set = FormSet(queryset=queryset)
    if request.method == 'POST':
        form_set = FormSet(request.POST)
        if form_set.is_valid():
            form_set.save()
        else:
            print("jajajjj")

    return render(request, 'crm/teacher/study_record_list.html', {"form_set": form_set})


def study_record_list(request):
    study_objs = models.StudyRecord.objects.all()
    return render(request, 'crm/teacher/study_list.html', {'study_objs': study_objs})
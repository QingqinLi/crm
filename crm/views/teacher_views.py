# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
__author__ = 'qing.li'
"""
from django.views import View
from django.shortcuts import HttpResponse, redirect, reverse, render
from crm.form.teacher_form import Class
from crm import models


class Classes(View):
    def get(self, request):
        print(request.user.classlist_set)
        class_obj = request.user.classlist_set.all()
        print(class_obj)
        # class_obj = models.ClassList.objects.filter(teachers=request.user)
        return render(request, 'crm/teacher/class_list.html', {'data': class_obj})

    def post(self, request):
        pass


def classes(request, class_id=None):
    class_obj = models.ClassList.objects.filter(id=class_id).first()
    form_obj = Class(instance=class_obj)
    if request.method == 'POST':
        form_obj = Class(request.POST, instance=class_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse("crm:classes"))
    return render(request, 'crm/teacher/class_add.html', {'form_obj': form_obj})
# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
__author__ = 'qing.li'
"""
from crm import models
from django import forms
from django.core.exceptions import ValidationError


class Class(forms.ModelForm):
    class Meta:
        model = models.ClassList
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class CourseForm(forms.ModelForm):
    class Meta:
        model = models.CourseRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for i in self.fields:
            self.fields[i].widget.attrs.update({'class': 'form-control'})

        self.fields['re_class'].widget.choices = [(self.instance.re_class_id, self.instance.re_class)]
        self.fields['teacher'].widget.choices = [(self.instance.teacher.id, self.instance.teacher)]

    def clean(self):
        is_homework = self.cleaned_data['has_homework']
        homework_title = self.cleaned_data['homework_title']
        print(is_homework, homework_title)
        if is_homework:
            if not homework_title:
                self.add_error('homework_title', '作业作业～～')
                raise ValidationError('作业作业～～')
            else:
                return self.cleaned_data
        else:
            if homework_title:
                self.add_error('has_homework', '有作业的，别忘了勾选！！！')
                raise ValidationError('有作业的，别忘了勾选！！！')
            else:
                return self.cleaned_data


class StudyRecordForm(forms.ModelForm):
    class Meta:
        model = models.StudyRecord
        fields = ['attendance', 'score', 'homework_note', 'student']

# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
__author__ = 'qing.li'
"""
from django import forms
from crm import models
from django.core.exceptions import ValidationError


class RegForm(forms.ModelForm):

    re_password = forms.CharField(
        min_length=8,
        label='确认密码',
        widget=forms.widgets.PasswordInput,
        error_messages={
            'required': '确认密码不能为空',
            'min_length': '最小长度为8'
        }
    )

    class Meta:
        model = models.UserProfile
        fields = ['username', 'password', 'name', 'department']
        # exclude = []
        widgets = {
            'password': forms.widgets.PasswordInput(),
            'username': forms.widgets.EmailInput(),  # 这里可以加attrs class
        }
        labels = {
            'username': '邮箱',
            'password': '密码',
            'name': '昵称',
            'department': '部门',
        }
        error_messages = {
            'username': {
                'required': '邮箱不能为空',
                'widget': '邮箱格式不正确',
            },
            'password': {
                'required': '密码不能为空',
                'min_length': '最小长度为8'
            },
            'name': {
                'required': '昵称不能为空',
            },
            'department': {
                'required': '部门不能为空',
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs.update({"class": "input"})
        self.fields['department'].widget.attrs.update({"class": "s1"})
        self.fields['username'].widget.attrs.update({"id": "user"})

    def clean(self):
        username = self.cleaned_data.get("username")
        if models.UserProfile.objects.filter(username=username):
            self.add_error("username", "用户已存在")
            raise ValidationError("用户已存在")
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")
        if password == re_password:
            return self.cleaned_data
        self.add_error('re_password', '两次密码不一致')
        raise ValidationError("两次密码不一致")


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'
        widgets = {
            'course': forms.widgets.SelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields.values():
            i.widget.attrs.update({"class": "form-control"})

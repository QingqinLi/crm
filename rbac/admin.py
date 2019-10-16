from django.contrib import admin
from rbac import models
# Register your models here.


# 在admin中每一条记录的显示
class PermissionAdmin(admin.ModelAdmin):
    # 要显示的字段
    list_display = ['title', 'url', 'name']
    # 可编辑的字段
    list_editable = ['url', 'name']


# 关联
admin.site.register(models.Permission, PermissionAdmin)
admin.site.register(models.User)
admin.site.register(models.Role)
admin.site.register(models.Menu)

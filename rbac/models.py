from django.db import models


# Create your models here.
class Menu(models.Model):
    title = models.CharField(max_length=32, verbose_name='标题')
    icon = models.CharField(max_length=32, verbose_name='图标', null=True, blank=True)
    weight = models.IntegerField(verbose_name='菜单权重', default=1)

    class Meta:
        # 改变admin中显示的表名称（外层）
        verbose_name_plural = '菜单表'
        verbose_name = '菜单表'

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(max_length=32, verbose_name='标题')
    url = models.CharField(max_length=128, verbose_name='权限')
    is_menu = models.BooleanField(default=False, verbose_name='是否为菜单')
    # null 数据库层面字段可以为空，blank在admin层面字段可以为空
    # icon = models.CharField(max_length=32, verbose_name='图标', null=True, blank=True)
    menu = models.ForeignKey('Menu', blank=True, null=True)
    # 自关联
    parent = models.ForeignKey('Permission', verbose_name='父级权限', null=True, blank=True)
    name = models.CharField(max_length=32, verbose_name='别名', null=True, blank=True, unique=True)

    class Meta:
        # 改变admin中显示的表名称（外层）
        verbose_name_plural = '权限表'
        verbose_name = '权限表'

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色表
    """
    name = models.CharField(max_length=32, verbose_name='角色名称')
    permissions = models.ManyToManyField(to='Permission', verbose_name='角色权限', blank=True)

    def __str__(self):
        return self.name


class User(models.Model):
    """
    用户表
    """
    name = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='密码')
    # blank 在admin中可以为空
    roles = models.ManyToManyField(to='Role', verbose_name='用户所拥有的角色')

    def __str__(self):
        return self.name
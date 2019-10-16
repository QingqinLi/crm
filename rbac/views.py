from django.shortcuts import render, redirect, reverse, HttpResponse
from rbac import models
from rbac import form
from django.db.models import Q
from django.forms import modelformset_factory, formset_factory
from rbac.server.routes import get_all_url_dict


# Create your views here.
def role_list(request):
    all_roles = models.Role.objects.all()

    return render(request, 'rbac/role_list.html', {'all_roles': all_roles})


def role(request, role_id=None):
    my_role = models.Role.objects.filter(id=role_id).first()
    role_obj = form.RoleForm(instance=my_role)

    if request.method == 'POST':
        role_obj = form.RoleForm(request.POST, instance=my_role)
        if role_obj.is_valid():
            role_obj.save()
            return redirect(reverse('rbac:role_list'))
    return render(request, 'rbac/role_add.html', {'role_obj': role_obj})


def role_del(request, role_id):
    models.Role.objects.filter(id=role_id).delete()
    return redirect(reverse('rbac:role_list'))


def menu_list(request):
    all_menus = models.Menu.objects.all()
    mid = request.GET.get("mid")
    permission_dict = {}
    if mid:
        permissions_query = models.Permission.objects.filter(Q(menu_id=mid) | Q(parent__menu_id=mid))
    else:
        permissions_query = models.Permission.objects.all()
    all_permissions = permissions_query.values()
    for permission in all_permissions:
        if permission.get('menu_id'):
            permission_dict[permission['id']] = permission
            permission_dict[permission['id']]['child'] = []
    for permission in all_permissions:
        pid = permission['parent_id']
        if pid:
            permission_dict[pid]['child'].append(permission)
    print("permission_dict", permission_dict)

    return render(request, 'rbac/menu_list.html', {'all_menus': all_menus,
                                                   'all_permissions': permission_dict,
                                                   })


def menu(request, edit_id=None):
    menu_obj = models.Menu.objects.filter(id=edit_id).first()
    form_obj = form.MenuForm(instance=menu_obj)
    if request.method == 'POST':
        form_obj = form.MenuForm(request.POST, instance=menu_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:menu_list'))

    return render(request, 'rbac/menu_add.html', {'form_obj': form_obj})


def menu_del(request, del_id):
    models.Menu.objects.filter(id=del_id).delete()
    return redirect(reverse('rbac:menu_list'))


def permission(request, edit_id=None):
    per_obj = models.Permission.objects.filter(id=edit_id).first()
    form_obj = form.PermissionForm(instance=per_obj)

    if request.method == 'POST':
        form_obj = form.PermissionForm(request.POST, instance=per_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:menu_list'))
    return render(request, 'rbac/form.html', {'form_obj': form_obj})


def permission_del(request, del_id):
    models.Permission.objects.filter(id=del_id).delete()
    return redirect(reverse('rbac:menu_list'))


def user_list(request):

    uid = request.GET.get('uid')
    rid = request.GET.get('rid')

    if request.method == 'POST' and request.POST.get('postType') == 'role':
        user = models.User.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        user.roles.set(request.POST.getlist('roles'))

    if request.method == 'POST' and request.POST.get('postType') == 'permission' and rid:
        role = models.Role.objects.filter(id=rid).first()
        if not role:
            return HttpResponse('角色不存在')
        role.permissions.set(request.POST.getlist('permissions'))
    users = models.User.objects.all()
    roles = models.Role.objects.all()

    user_has_roles = models.User.objects.filter(id=uid).values('id', 'roles')
    user_has_roles_dict = {item['roles']: None for item in user_has_roles}

    if rid:
        role_has_permissions = models.Role.objects.filter(id=rid).values('id', 'permissions')
    elif uid and not rid:
        user = models.User.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        role_has_permissions = user.roles.values('id', 'permissions')
    else:
        role_has_permissions = []

    role_has_permissions_dict = {item['permissions']: None for item in role_has_permissions}

    all_menu_list = []
    queryset = models.Menu.objects.values('id', 'title')
    menu_dict = {}

    for item in queryset:
        item['children'] = []
        menu_dict[item['id']] = item
        all_menu_list.append(item)

    other = {'id': None,
             'title': '其他',
             'children': [],
             }
    all_menu_list.append(other)
    menu_dict[None] = other

    root_permission = models.Permission.objects.filter(menu__isnull=False).values('id', 'title', 'menu_id')
    root_permission_dict = {}

    for per in root_permission:
        per['children'] = []
        nid = per['id']
        menu_id = per['menu_id']
        root_permission_dict[nid] = per
        menu_dict[menu_id]['children'].append(per)

    node_permission = models.Permission.objects.filter(menu__isnull=True).values('id', 'title', 'parent_id')
    for per in node_permission:
        pid = per['parent_id']
        if not pid:
            menu_dict[None]['children'].append(per)
            continue
        root_permission_dict[pid]['children'].append(per)
    return render(request, 'rbac/distribute_permissions.html', {'users': users,
                                                                'roles': roles,
                                                                'user_has_roles_dict': user_has_roles_dict,
                                                                'role_has_permissions_dict': role_has_permissions_dict,
                                                                'all_menu_list': all_menu_list,
                                                                'uid': uid,
                                                                'rid': rid,
                                                                })


def multi_permissions(request):
    """
    待新建权限：路由系统中有，但是数据库中没有的url
    :param request:
    :return:
    """
    post_type = request.GET.get('type')

    # 跟新和编辑用的form
    FormSet = modelformset_factory(models.Permission, form.MultiPermissionForm, extra=0)

    # 增加用的form
    AddFormSet = formset_factory(form.MultiPermissionForm, extra=0)

    permissions = models.Permission.objects.all()

    # 获取路由系统中所有的url
    router_dict = get_all_url_dict(ignore_namespace_list=['admin'])

    # 数据库中的所有权限的别名
    permissions_name_set = set([i.name for i in permissions])

    # 路由系统中的所欲权限的别名
    router_name_set = set(router_dict.keys())

    if request.method == 'POST' and post_type == 'add':
        add_formset = AddFormSet(request.POST)
        if add_formset.is_valid():
            print(add_formset.cleaned_data)
            permission_obj_list = [models.Permission(**i) for i in add_formset.cleaned_data]
            print(permission_obj_list)

            query_list = models.Permission.objects.bulk_create(permission_obj_list)

            for i in query_list:
                permissions_name_set.add(i.name)
    add_name_set = router_name_set - permissions_name_set
    add_formset = AddFormSet(initial=[row for name, row in router_dict.items() if name in add_name_set])

    del_name_set = permissions_name_set - router_name_set
    del_formset = FormSet(queryset=models.Permission.objects.filter(name__in=del_name_set))

    update_name_set = permissions_name_set & router_name_set
    update_formset = FormSet(queryset=models.Permission.objects.filter(name__in=update_name_set))

    if request.method == 'POST' and post_type == 'update':
        update_formset = FormSet(request.POST)
        if update_formset.is_valid():
            update_formset.save()
            update_formset = FormSet(queryset=models.Permission.objects.filter(name__in=update_name_set))

    return render(
        request,
        'rbac/multi_permissions.html',
        {
            'del_formset': del_formset,
            'update_formset': update_formset,
            'add_formset': add_formset,
        }
    )


def user(request, edit_id=None):
    user_obj = models.User.objects.filter(id=edit_id).first()
    form_obj = form.UserForm(instance=user_obj)
    if request.method == 'POST':
        form_obj = form.UserForm(request.POST, instance=user_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse("rbac:user_list"))
    return render(request, 'rbac/form.html', {"form_obj": form_obj})
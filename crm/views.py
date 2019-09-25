from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from crm import form
from crm import models
from utils.pagination import Pagination
from django.views import View
from django.db.models import Q
from django.http import QueryDict


# Create your views here.
def login(request):
    error_msg = ''
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_obj = auth.authenticate(request, username=username, password=password)
        if user_obj:
            # 记录登录状态
            auth.login(request, user_obj)
            next = request.POST.get("next")
            if next:
                return redirect(next)
            return redirect(reverse("crm:customer"))
        error_msg = '用户名或密码错误'
    return render(request, "login.html", {'error_msg': error_msg})


def logout(request):
    auth.logout(request)
    return redirect(reverse('crm:login'))


@login_required()
def index(request):
    return render(request, 'index.html')


def register(request):
    reg_form = form.RegForm()
    if request.method == 'POST':
        reg_form = form.RegForm(request.POST)
        if reg_form.is_valid():
            reg_form.cleaned_data.pop("re_password")
            print(reg_form.cleaned_data)
            models.UserProfile.objects.create_user(**reg_form.cleaned_data)
            return redirect(reverse("crm:login"))

        #  save  form.model直接save， 此时密码为明文 无法登录，通过set_password的方法重新设置密码 save保存
        # obj = reg_form.save()
        # obj.set_password(obj.password)
        # obj,save()
    return render(request, 'reg.html', {'reg_form': reg_form})


def check_name(request):
    if request.method == 'POST':
        user = request.POST.get("username")
        print("user", user)
        if models.UserProfile.objects.filter(username=user):
            return HttpResponse("用户已存在")
    else:
        return HttpResponse("")


class Customer(View):

    def get(self, request):
        query_list = ['id', 'name', 'qq_name']
        q = self.get_search_condition(query_list)
        if request.path_info == reverse('crm:customer'):
            customer = models.Customer.objects.filter(q, consultant__isnull=True)
        else:
            customer = models.Customer.objects.filter(q, consultant=request.user)

        query_params = request.GET.copy()

        c = Pagination(request, 10, 10, customer, query_params)
        customer_data = c.show_li
        # print("urlencode()", customer_data)

        next_url = self.get_add_btn()
        print("next_url", next_url)
        return render(request, 'crm/customer_list.html', {'page': customer_data, "data": c.show_list,
                                                          'next_url': next_url})

    def post(self, request):
        operate = request.POST.get('operate')
        # ids = request.POST.getlist("id")
        if not hasattr(self, operate):
            return HttpResponse("illegal operation")
        else:
            getattr(self, operate)()
        return self.get(request)

    def multi_delete(self):
        ids = self.request.POST.getlist("id")
        models.Customer.objects.filter(id__in=ids).delete()

    # 放入私户
    def multi_apply(self):
        ids = self.request.POST.getlist("id")
        ids_objs = models.Customer.objects.filter(id__in=ids)
        if ids:
            for id in ids_objs:
                id.consultant = self.request.user
                # 需要save
                id.save()
                print(id.consultant)

        print(ids)
        # models.Customer.objects.filter(id__in=ids).update(consultant=self.request.user) 不需要save
        # self.request.user.customers.add(*models.Customer.objects.filter(id__in=ids))

    # 放入公户
    def multi_pub(self):
        ids = self.request.POST.getlist("id")
        models.Customer.objects.filter(id__in=ids).update(consultant=None)

    def get_search_condition(self, query_list):
        query = self.request.GET.get('query', '')
        q = Q()
        q.connector = 'OR'
        for i in query_list:
            q.children.append(Q(('{}__contains'.format(i), query)))

        return q

    def get_add_btn(self):
        url = self.request.get_full_path()
        qd = QueryDict()
        qd._mutable = True
        qd['next_page'] = url
        print("qd", qd)
        query_params = qd.urlencode()

        return query_params


@login_required()
def customer_list(request):
    # 判断用户请求的是公户还是私户
    if request.path_info == reverse('crm:customer'):
        customer = models.Customer.objects.filter(consultant__isnull=True)
    else:
        customer = models.Customer.objects.filter(consultant=request.user)
    c = Pagination(request, 10, 10, customer)
    customer_data = c.show_list()

    return render(request, 'crm/customer_list.html', customer_data)


# 添加和编辑可以使用一个view函数
@login_required()
def add_customer(request):
    form_obj = form.CustomerForm()
    next = request.GET.get("next_page")
    print("next", next)
    if request.method == 'POST':
        form_obj = form.CustomerForm(request.POST)
        if form_obj.is_valid():
            # modelsForm的创建用户的方式
            form_obj.save()
            if next:
                return redirect(next)
            return redirect(reverse("crm:customer"))
    return render(request, 'crm/customer_add.html', {'form_obj': form_obj})


@login_required()
def edit_customer(request, edit_id):
    obj = models.Customer.objects.filter(id=edit_id).first()
    form_obj = form.CustomerForm(instance=obj)
    next = request.GET.get("next_page")

    if request.method == 'POST':
        form_obj = form.CustomerForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            if next:
                return redirect(next)
            return redirect(reverse('crm:customer'))
    return render(request, 'crm/customer_edit.html', {'form_obj': form_obj})


class ConsultRecord(View):

    def get(self, request):
        consult_record = models.ConsultRecord.objects.filter(consultant=request.user)

        query_params = request.GET.copy()

        c = Pagination(request, 10, 10, consult_record, query_params)
        page = c.show_li
        query_params = self.get_query_params()

        return render(request, 'crm/consult_record.html',
                      {'consult_record': consult_record, "page": page, "data": c.show_list,
                       'next_url': query_params})

    def post(self, request):
        pass

    def get_query_params(self):
        url = self.request.get_full_path()
        qd = QueryDict()
        qd._mutable = True
        qd['next_page'] = url
        query_params = qd.urlencode()

        return query_params


def add_consult_record(request):
    consult_obj = models.ConsultRecord(consultant=request.user)
    form_obj = form.ConsultRecordForm(instance=consult_obj)
    if request.method == 'POST':
        form_obj = form.ConsultRecordForm(request.POST, instance=consult_obj)
        if form_obj.is_valid():
            form_obj.save()
            next = request.GET.get('next_url')
            if next:
                redirect(next)
            return redirect(reverse("crm:consult_record"))
    return render(request, 'crm/consult_record_add.html', {'form_obj': form_obj})


def edit_consult_record(request, consult_record_id):
    consult_obj = models.ConsultRecord.objects.filter(id=consult_record_id).first()
    # consult_obj = models.ConsultRecord.objects.filter(id=consult_record_id)
    form_obj = form.ConsultRecordForm(instance=consult_obj)
    if request.method == 'POST':
        form_obj = form.ConsultRecordForm(request.POST, instance=consult_obj)
        if form_obj.is_valid():
            form_obj.save()
            next = request.GET.get('next_url')
            if next:
                redirect(next)
            return redirect(reverse("crm:consult_record"))
    return render(request, 'crm/consult_record_edit.html', {'form_obj': form_obj})


class Enrollment(View):
    def get(self, request):
        enrollment_obj = models.Enrollment.objects.all()
        return render(request, 'crm/enrollment_list.html', {'enrollment_obj': enrollment_obj})

    def post(self, request):
        pass


def user_list(request):
    try:
        current_page = int(request.GET.get('page'))
    except TypeError:
        current_page = 1
    item = 10
    user_list = [{"id": i, "name": "alex%s" % i, "sex": "男"} for i in range(1, 203)]
    max_page = 5
    if divmod(len(user_list), item)[1] == 0:
        end = len(user_list) // item
    else:
        end = len(user_list) // item + 1
    range_start = current_page - max_page // 2
    range_end = current_page + max_page // 2
    if range_start < 1:
        range_start = 1
        range_end = max_page
    if range_end > end:
        range_end = end
        range_start = range_end - max_page + 1

    # range_start = 10
    page = range(range_start, range_end + 1)
    # print(page)
    data = user_list[(current_page - 1) * item:current_page * item]
    print("end", end)
    if current_page == 1:
        previous = 1
        next = current_page + 1
    elif current_page == end:
        previous = current_page - 1
        next = current_page
    else:
        previous = current_page - 1
        next = current_page + 1
    print(previous, next)

    return render(request, 'crm/user_list.html',
                  {
                      "user": data,
                      "page": page,
                      "previous": previous,
                      "next": next,
                  })

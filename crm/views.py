from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from crm import form
from crm import models
from utils.pagination import Pagination


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
            return redirect(reverse("crm:index"))
        error_msg = '用户名或密码错误'
    return render(request, "login.html", {'error_msg': error_msg})


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


@login_required()
def customer_list(request):
    customer = models.Customer.objects.all()
    print(customer)
    c = Pagination(request, 10, 10, customer)
    customer_data = c.show_list()
    print(customer_data)
    return render(request, 'crm/customer_list.html', customer_data)


@login_required()
def add_customer(request):
    form_obj = form.CustomerForm()
    if request.method == 'POST':
        form_obj = form.CustomerForm(request.POST)
        if form_obj:
            # modelsForm的创建用户的方式
            form_obj.save()
            return redirect(reverse("crm:customer"))
    return render(request, 'crm/customer_add.html', {'form_obj': form_obj})


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
    range_start = current_page - max_page//2
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

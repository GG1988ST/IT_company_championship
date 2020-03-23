from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from Ratecompany.models import Company, Category, Comments, UserProfile

from django.views import View
from django.db.models import Q


# 登录模块
class LoginRequiredMixin(object):
    """
    登陆限定，并指定登陆url
    """
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view, login_url='/Ratecompany/login')


def index(request):
    return render(request, 'Ratecompany/index.html')


class CompanyListView(View):

    def get(self, request):
        category = Category.objects.all()
        company = Company.objects.all()
        category_id = request.GET.get('id')
        if category_id:
            company = company.filter(category__id=category_id)
        return render(request, 'Ratecompany/companies.html', {'companies': company, 'categories': category})

    def post(self, request):
        category = Category.objects.all()
        company = Company.objects.all()
        search = request.POST.get("search")
        if search:

            company = company.filter(name__contains=search)
        category_id = request.GET.get('id')
        if category_id:
            company = company.filter(category__id=category_id)
        return render(request, 'Ratecompany/companies.html', {'companies': company, 'categories': category})



class CompanyDetailView(View):

    def get(self, request, *args, **kwargs):
        company_id = kwargs.get("id")
        company = Company.objects.get(id=company_id)
        return render(request, 'Ratecompany/company_detail.html', {'company': company})


class CommentListView(View):
    def get(self, request, *args, **kwargs):
        company_id = request.GET.get("id")
        company = Company.objects.get(id=company_id)

        comment_list = Comments.objects.filter(company=company).order_by("-create_time")
        _type = request.GET.get("type")
        if _type:
            comment_list.filter(classify=int(_type))
        return render(request, 'Ratecompany/comments.html', {'company': company, 'comment_list': comment_list})


# 注册模块
class RegisterView(View):
    def get(self, request):
        company = Company.objects.all()
        return render(request, 'Ratecompany/register.html', {'company_list': company})

    def post(self, request):
        company = Company.objects.all()
        company_id = request.POST.get("company_id")
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        rePassword = request.POST.get('rePassword')
        if password != rePassword:
            return render(request, 'Ratecompany/register.html', {'error': '两次密码输入不一致', 'company_list': company})

        user = UserProfile.objects.filter(Q(username=username) | Q(email=email))
        if user:   # 已存在邮箱或者账号
            return render(request, 'Ratecompany/register.html', {'error': '邮箱或者账号已存在', 'company_list': company})
        obj = UserProfile.objects.create(username=username, email=email, company_id=company_id)
        obj.set_password(password)
        obj.save()
        return HttpResponseRedirect(reverse('Ratecompany:login'))


# 退出模块
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('Ratecompany:login'))


# 登录模块
class LoginView(View):
    def get(self, request):
        return render(request, 'Ratecompany/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_remember_me = request.POST.get('is_remember_me')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session.set_expiry(0)
                if is_remember_me:
                    request.session.set_expiry(None)
                return HttpResponseRedirect(reverse("homepage"))
            else:
                return render(request, "Ratecompany/login.html", {"error": "用户未激活！"})
        else:
            return render(request, "Ratecompany/login.html", {"error": "用户名或密码错误！"})



class RateView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'Ratecompany/rate.html')

    def post(self, request):
        classify = request.POST.get("classify")
        star = int(request.POST.get("star"))
        content = request.POST.get("content")
        user = request.user
        company = user.company
        Comments.objects.create(company=company, comments=content, classify=classify, score=star,
                                user_name=user.username)
        user_count = company.users.all().count()
        if classify == '0':
            company.salary = ((company.salary * user_count) + star) / user_count
        if classify == '1':
            company.salary = ((company.wellfare * user_count) + star) / user_count
        if classify == '2':
            company.atmosphere = ((company.atmosphere * user_count) + star) / user_count
        company.save()
        return HttpResponseRedirect(reverse('Ratecompany:rate'))





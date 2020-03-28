from django.shortcuts import render, reverse, redirect
from django.contrib.auth import authenticate, login, logout
from Ratecompany.models import Company, Category, Comments, UserProfile
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from django.db.models import Q
from django.views import View



# login model
class LoginRequiredMixin(object):
    """
    limit the login and refer to certain url
    """
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view, login_url='/Ratecompany/login')



# company list
class CompanyListView(View):

    def get(self, request):
        category = Category.objects.all()
        company = Company.objects.all()
        category_slug = request.GET.get('category')
        if category_slug:
            company = company.filter(category__slug=category_slug)
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



# company detail
class CompanyDetailView(View):

    def get(self, request, *args, **kwargs):
        company_slug = kwargs.get("slug")
        company = Company.objects.get(slug=company_slug)
        return render(request, 'Ratecompany/company_detail.html', {'company': company})



#comment list
class CommentListView(View):
    def get(self, request, *args, **kwargs):
        
        company_slug = request.GET.get("company")
              
        company = Company.objects.get(slug=company_slug)
        comment_list = Comments.objects.filter(company=company).order_by("-create_time")
        _type = request.GET.get("type")
        if _type:
            comment_list=comment_list.filter(classify=int(_type))
        return render(request, 'Ratecompany/comments.html', {'company': company, 'comment_list': comment_list})



# Register model
class RegisterView(View):
    def get(self, request):
        company = Company.objects.all()
        return render(request, 'Ratecompany/register.html', {'company_list': company})

    def post(self, request):
        company = Company.objects.all()
        company_id = request.POST.get("company_id")
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        print(company_id)
        companylist=None;
        companylist=Company.objects.filter(id=company_id)
        if email and not email.endswith(companylist[0].emailtag):
            return render(request,'Ratecompany/register.html', {'error': 'non-commercial email','company_list':company})
        
        password = request.POST.get('password')
        rePassword = request.POST.get('rePassword')
        if password != rePassword:
            return render(request, 'Ratecompany/register.html', {'error': 'Inconsistent password','company_list':company})

        user = UserProfile.objects.filter(Q(username=username) | Q(email=email))
        if user:   # already has the user
            return render(request, 'Ratecompany/register.html', {'error': 'account already exist','company_list':company})
        obj = UserProfile.objects.create(username=username, email=email, company_id=company_id)
        obj.set_password(password)
        obj.save()
        return HttpResponseRedirect(reverse('Ratecompany:login'))



# logout model
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('Ratecompany:login'))



# register model
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
                return render(request, "Ratecompany/login.html", {"error": "unactivated account"})
        else:
            return render(request, "Ratecompany/login.html", {"error": "Username or password is incorrect or both"})


#Rate company
class RateView(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.is_staff:
            return render(request, 'Ratecompany/index.html',{"error": "staff cannot rate!"})
            
        user = request.user
        comment_list = Comments.objects.filter(user_name=user.username).order_by("-create_time")
        
        return render(request, 'Ratecompany/rate.html',{'comment_list': comment_list})

    def post(self, request):
        classify = request.POST.get("classify")
        star = request.POST.get("star")
        content = request.POST.get("content")
        user = request.user
        comment_list = Comments.objects.filter(user_name=user.username).order_by("-create_time")
           
        if classify is None or star is None:
            return render(request, "Ratecompany/rate.html", {"error": "Please complete the info!",'comment_list': comment_list})
        if len(content)<30:
            return render(request, "Ratecompany/rate.html", {"error": "Please enter at least 30 characters in comment!",'comment_list': comment_list})
        star=int(star)
        print(star)
        user = request.user
        company = user.company
        Comments.objects.create(company=company, comments=content, classify=classify, score=star,user_name=user.username)
        if classify == '0':
            print(company.salary)
            commentcount = Comments.objects.filter(company=company,classify=0).count()
            company.salary = ((company.salary * (commentcount-1)) + star) / commentcount
            print(commentcount)
            print(company.salary)
        if classify == '1':
            print(company.wellfare)
            commentcount = Comments.objects.filter(company=company,classify=1).count()
            company.wellfare = ((company.wellfare * (commentcount-1)) + star) / commentcount
            print(commentcount)
            print(company.wellfare)
        if classify == '2':
            print(company.atmosphere)
            commentcount = Comments.objects.filter(company=company,classify=2).count()
            company.atmosphere = ((company.atmosphere * (commentcount-1)) + star)/ commentcount
            print(commentcount)
            print(company.atmosphere)
        company.save()
       
           #print(company.wellfare)
           #print(company.atmosphere)
        return render(request, "Ratecompany/rate.html", {"error": "Submit successful!!!",'comment_list': comment_list})
           #return HttpResponseRedirect(reverse('Ratecompany:rate'))




def index(request):
        return render(request, 'Ratecompany/index.html')

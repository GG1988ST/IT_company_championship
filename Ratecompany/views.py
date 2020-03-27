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



# company detail
class CompanyDetailView(View):

    def get(self, request, *args, **kwargs):
        company_id = kwargs.get("id")
        company = Company.objects.get(id=company_id)
        return render(request, 'Ratecompany/company_detail.html', {'company': company})



#comment list
class CommentListView(View):
    def get(self, request, *args, **kwargs):
        company_id = request.GET.get("id")
        company = Company.objects.get(id=company_id)

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
        company=Company.objects.all()
        emailtag='kdjnedke'
        company_id = request.POST.get("company_id")
        if company_id =='1':
                  emailtag= '@baidu.cn'
        if company_id =='2':
                  emailtag= '@google.cn'
        if company_id =='3':
                  emailtag= '@fire.cn'
        if company_id =='4':
                emailtag= '@wangyi.cn'
        print(company_id)
        print(emailtag)
        username = request.POST.get('username')
        email = request.POST.get('email')
        print(company_id)
        if email and not email.endswith(emailtag):
            return render(request,'Ratecompany/register.html', {'error': 'non-commercial email','company_list':company})
        password = request.POST.get('password')
        rePassword = request.POST.get('rePassword')
        if password != rePassword:
            return render(request, 'Ratecompany/register.html', {'error': 'Inconsistent password'})

        user = UserProfile.objects.filter(Q(username=username) | Q(email=email))
        if user:   # already has the user
            return render(request, 'Ratecompany/register.html', {'error': 'account already exist'})
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
            commentcount = Comments.objects.filter(company=company,classify=0).count()
            company.salary = ((company.salary * commentcount) + star) / commentcount
            print(commentcount)
            print(company.salary)
        if classify == '1':
            company.wellfare = ((company.wellfare * user_count) + star) / user_count
            print(user_count)
        if classify == '2':
            company.atmosphere = ((company.atmosphere * user_count) + star) / user_count
            print(user_count)
        company.save()
       
           #print(company.wellfare)
           #print(company.atmosphere)
        return render(request, "Ratecompany/rate.html", {"error": "Submit successful!!!",'comment_list': comment_list})
           #return HttpResponseRedirect(reverse('Ratecompany:rate'))




def index(request):
    context_dict = {}
    return render(request, 'Ratecompany/index.html', context=context_dict)




def show_category(request):

    context_dict = {}
    # print(company_name_slug)
    try:
        category = Category.objects.all()
        company = Company.objects.all()
        #print(company)
        context_dict['companies'] = company
        context_dict['categories'] = category
    except Company.DoesNotExist:
        print("errorrrrr")
        context_dict['companies'] = None

    return render(request, 'Ratecompany/companies.html', context=context_dict)

def show_company(request, company_name_slug):
    context_dict = {}

    try:
        company = Company.objects.filter(slug=company_name_slug)
        comments = Comments.objects.filter(company=company)

        context_dict['companies'] = company
        context_dict['comments'] = comments
    except Category.DoesNotExist:
        print("error")
        context_dict['companies'] = None

    return render(request, 'Ratecompany/showCompany.html', context=context_dict)

def add_company(request):
    form = CompanyForm()

    if request.method == 'POST':
        form = CompanyForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return render(request, 'Ratecompany/index.html')

        else:
            print(form.errors)

    return render(request, 'Ratecompany/add_company.html', {'form': form})


def add_comment(request, company_name_slug):
    try:
        company = Company.objects.get(slug=company_name_slug)
    except Company.DoesNotExist:
        company = None

    if company is None:
        return redirect(reverse('company:index'))

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if company:
                comment = form.save(commit=False)
                comment.company = company
                comment.save()
                return redirect(reverse('Ratecompany:show_company', kwargs={'company_name_slug':
                                                                         company_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'company': company}
    return render(request, 'Ratecompany/add_comment.html', context=context_dict)



#user register

def register(request):
    registered = False
    if request.method=='POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user

            if 'picture' in request.FILES:
                profile.picture =request.FILES['picture']

            profile.save()
            registered=True
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dic ={'user_form':user_form,
                  'profile_form':profile_form,
                  'registered':registered}

    return render(request,'Ratecompany/register.html',context=context_dic)


def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return redirect(reverse('Ratecompany/index.html'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request,'Ratecompany/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('Ratecompany/index.html'))

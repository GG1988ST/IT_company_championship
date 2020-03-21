from django.shortcuts import render, reverse, redirect
from django.contrib.auth import authenticate, login
from Ratecompany.forms import CompanyForm,Comments
from Ratecompany.models import Company, Category
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from Ratecompany.forms import UserForm, UserProfileForm
from django.contrib.auth import logout
from datetime import datetime

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



###wqeqwe

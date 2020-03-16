from django.shortcuts import render, reverse, redirect

from Ratecompany.forms import CompanyForm,Comments
from Ratecompany.models import Company, Category
from django.http import HttpResponse

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

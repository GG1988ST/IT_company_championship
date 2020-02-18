from django.shortcuts import render
from company.models import Company
from django.http import HttpResponse

def index(request):
    context_dict = {}
    return render(request, 'company/index.html', context=context_dict)


def show_company(request, company_name_slug):

    context_dict = {}

    try:
        company = Company.objects.get(slug=company_name_slug)
        context_dict['company'] = company

    except Company.DoesNotExist:
        context_dict['company'] = None

    return render(request, 'company/companies.html', context=context_dict)



def add_company(request):
    form = CompanyForm()

    if request.method == 'POST':
        form = CompanyForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return render(request, 'company/index.html')

        else:
            print(form.errors)

    return render(request, 'company/add_company.html', {'form': form})



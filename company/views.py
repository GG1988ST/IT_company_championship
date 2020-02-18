from django.shortcuts import render
from company.models import Company
from django.http import HttpResponse



def show_company(request, company_name_slug):

    context_dict = {}

    try:
        company = Company.objects.get(slug=company_name_slug)
        context_dict['company'] = company

    except Company.DoesNotExist:
        context_dict['company'] = None

    return render(request, 'company/companies.html', context=context_dict)



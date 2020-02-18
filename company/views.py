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
        context_dict['companies'] = company

    except Company.DoesNotExist:
        context_dict['companies'] = None

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
                return redirect(reverse('company:show_company', kwargs={'company_name_slug':
                                                                         company_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form 'company': company}
    return render(request, 'company/add_comment.html', context=context_dict)

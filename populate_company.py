import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IT_company_championship.settings')

import django

django.setup()
from Ratecompany.models import Category, Comments, Company


def populate():
    comment01 = [
        {'comments': 'good job?',
         'date': '2020-1-3'},
        {'comments': 'good job>',
         'date': '2020-2-3'},
        {'comments': 'good job{',
         'date': '2020-3-3'}]

    comment02 = [
        {'comments': 'good jobp',
         'date': '2020-1-1'},
        {'comments': 'good job/',
         'date': '2020-4-2'},
        {'comments': 'good job:',
         'date': '2020-5-3'}]

    comment03 = [
        {'comments': 'good jobi',
         'date': '2020-7-6'},
        {'comments': 'good job?',
         'date': '2020-11-7'}]

    itcompany = [{'name': 'Baidu', 'comments': comment01, 'location': 'China', 'rates': 4},
                 {'name': 'Google', 'comments': comment02, 'location': 'British', 'rates': 2}, ]
    gamecompany = [{'name': 'Fire', 'comments': comment03, 'location': 'Japan', 'rates': 1}, ]

    category = {'IT': {'company': itcompany},
                'Game': {'company': gamecompany}}

    for cate, category_data in category.items():
        c = add_category(cate)
        for p in category_data['company']:
            o = add_company(c, p['name'], p['location'], p['rates'])
            for com in p['comments']:
                add_comments(o, com['comments'], com['date'])

    add_category('lalala')

    add_company(add_category('Game'), 'Wangyi', 'GZ', 999)
    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Company.objects.filter(category=c):
            print(f'- {c}: {p}')


def add_comments(company, comments, date):
    print(comments)
    print(date)
    p = Comments.objects.create(company=company, comments=comments,date=date)
    return p


def add_company(category, name, location, rates):

    c = Company.objects.filter(name=name)
    if c:
        c = c[0]
        c.category = category
        c.location = location
        c.rates = rates
        c.save()
    else:
        c = Company.objects.create(category=category, name=name, location=location,rates=rates)
    #c.category = category
    #c.location = location
    #c.rates = rates
    #c.save()
    return c


def add_category(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c


if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()

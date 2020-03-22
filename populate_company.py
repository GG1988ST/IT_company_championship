import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IT_company_championship.settings')

import django

django.setup()
from Ratecompany.models import Category, Comments,  Company


def populate():
    comment01 = [
        {'comments': 'This company is very nice and I love it so much. Very flexible timetable and comfortable workspace!',
         'date': '2020-1-3', 'classify':1, 'score': 3},
        {'comments': 'The colleagues are so lovely and the food is fabulous!',
         'date': '2020-2-3','classify':2, 'score': 3},
        {'comments': 'Fantastic job!!',
         'date': '2020-3-3','classify':3, 'score': 4}]

    comment02 = [
        {'comments': 'I love the atomsphere of this company.',
         'date': '2020-1-1','classify':1, 'score': 5},
        {'comments': 'I think it is ok.',
         'date': '2020-4-2','classify':1, 'score': 3},
        {'comments': 'I donnot like it.',
         'date': '2020-5-3','classify':1, 'score': 3}]

    comment03 = [
        {'comments': 'I really enjoy working in it!',
         'date': '2020-7-6', 'classify':1, 'score': 3},
        {'comments': 'nice job.',
         'date': '2020-11-7','classify':3, 'score': 3}]

    itcompany = [{'name': 'Baidu', 'comments': comment01, 'location': 'China'},
                 {'name': 'Google', 'comments': comment02, 'location': 'British'}, ]
    gamecompany = [{'name': 'Blizzard Entertainment', 'comments': comment03, 'location': 'US'}, ]

    category = {'IT': {'company': itcompany},
                'Game': {'company': gamecompany}}

    for cate, category_data in category.items():
        c = add_category(cate)
        for p in category_data['company']:
            o = add_company(c, p['name'], p['location'])
            for com in p['comments']:
                add_comments(o, com['comments'], com['date'], com['classify'], com['score'])

    add_category('lalala')

    add_company(add_category('Game'), 'Wangyi', 'GZ')
    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Company.objects.filter(category=c):
            print(f'- {c}: {p}')


def add_comments(company, comments, date,classify, score):
    print(comments)
    print(date)

    p = Comments.objects.create(company=company, comments=comments,date=date,  classify=classify, score=score)
    return p


def add_company(category, name, location):

    c = Company.objects.filter(name=name)
    if c:
        c = c[0]
        c.category = category
        c.location = location
        c.save()
    else:
        c = Company.objects.create(category=category, name=name, location=location)
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

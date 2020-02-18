import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','IT_company_championship.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
    comments = [
        {'comments':'good job?',
        'date':2020-1-3},
        {'comments':'good job>',
        'date':2020-2-3},
        {'comments':'good job{',
        'date':2020-3-3} ]

    comments_2 = [
        {'comments':'good jobp',
        'date':2020-1-1},
        {'comments':'good job/',
        'date':2020-1-2},
        {'comments':'good job:',
        'date':2020-1-3} ]

    comments_3 = [
        {'comments':'good jobi,
        'date':2020-1-6},
        {'comments':'good job?',
        'date':2020-1-7} ]

    cats = {'Baidu': {'pages': python_pages,'views':128,'likes':64},
    'Google': {'pages': django_pages,'views':64,'likes':32},
    'Fire': {'pages': other_pages,'views':32,'likes':16} }

    for cat, cat_data in cats.items():
        c = add_cat(cat,cat_data['views'],cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'],p['views'])
    
    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')



def add_page(cat, title, url, views):
        p = Page.objects.get_or_create(category=cat, title=title)[0]
        p.url=url
        p.views=views
        p.save()
        return p

def add_cat(name,views,likes):
        c = Category.objects.get_or_create(name=name)[0]
        c.likes=likes
        c.views=views
        c.save()
        return c

if __name__ == '__main__':
        print('Starting Rango population script...')
        populate()
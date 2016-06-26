from django.shortcuts import render
from django.http import HttpResponse

from .cache import get_setting_cache, get_type_cache, get_type_list

# Create your views here.

def index(request):
    data = r'^(?P<term>[' + '|'.join(get_type_list()) +'])/$'
    return HttpResponse('Home index %s' % data)

def taxonomy(request, taxonomy):
    return HttpResponse('Taxonomy %s page' % taxonomy)

def term(request, taxonomy, term):
    return HttpResponse('Term %s under taxonomy %s page' % (taxonomy, term))

def post(request, term, title):
    context = {'term': term, 'title': title}
    return render(request, 'default/post.html', context=context)

def posttype(request, term):
    return HttpResponse('term %s' % term)
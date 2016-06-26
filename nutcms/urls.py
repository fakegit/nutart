from django.conf.urls import url

from .cache import get_setting_cache, get_type_cache, get_type_list
from . import views

typepattern = r'^(?P<term>' + '|'.join(get_type_list()) +')/'

app_name = 'nutcms'

urlpatterns = [
    # ex: /
    url(r'^$', views.index, name='index'),
    # ex: /post/ /page/
    url(typepattern + '$', views.posttype, name='posttype'),
    # ex: /post/first-news /page/about-us
    url(typepattern + '(?P<title>[\w-]+)/$', views.post, name='post'),
    # ex: /category/ /star/ /director/ /maker/
    url(r'^(?P<taxonomy>[\w-]+)/$', views.taxonomy, name='taxonomy'),
    # ex: /star/will-smith
    url(r'^(?P<taxonomy>[\w-]+)/(?P<term>[\w-]+)/$', views.term, name='term'),
]
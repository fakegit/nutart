from django.conf.urls import url

from .shortcuts import get_all_posttypes, get_all_taxonomies
from . import views

posttype_pattern = r'^(?P<posttype_slug>' + '|'.join([__.slug for __ in get_all_posttypes()]) +')/'
taxonomy_pattern = r'^(?P<taxonomy_slug>' + '|'.join([__.slug for __ in get_all_taxonomies()]) + ')/'

app_name = 'nutcms'

urlpatterns = [
    # ex: /
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.index, name='index'),
    # ex: /post/ /page/
    url(posttype_pattern + '$', views.PosttypeView.as_view(), name='posttype'),
    # url(posttype_pattern + '$', views.posttype, name='posttype'),
    # ex: /post/first-news /page/about-us
    url(posttype_pattern + '(?P<post_slug>[\w-]+)/$', views.PostView.as_view(), name='post'),
    # url(posttype_pattern + '(?P<post_slug>[\w-]+)/$', views.post, name='post'),
    # ex: /category/ /star/ /director/ /maker/
    url(taxonomy_pattern + '$', views.TaxonomyView.as_view(), name='taxonomy'),
    # url(taxonomy_pattern + '$', views.taxonomy, name='taxonomy'),
    # ex: /star/will-smith
    url(taxonomy_pattern + '(?P<term_sulg>[\w-]+)/$', views.TermView.as_view(), name='term'),
    # url(taxonomy_pattern + '(?P<term_slug>[\w-]+)/$', views.term, name='term'),
]
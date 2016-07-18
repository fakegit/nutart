from django.conf.urls import url, include

from .shortcuts import get_all_posttypes, get_all_taxonomies
from . import views

posttype_pattern = r'^(?P<posttype_slug>' + '|'.join([__.slug for __ in get_all_posttypes()]) +')/'
taxonomy_pattern = r'^(?P<taxonomy_slug>' + '|'.join([__.slug for __ in get_all_taxonomies()]) + ')/'

app_name = 'nutcms'

moviepatterns = [
    url(r'^$', views.MovieView.as_view(), name='movie'),
    url(r'^play/(?:(?P<res_id>[\w-]+)/)?$', views.MoviePlayView.as_view(), name='movieplay'),
    url(r'^download/$', views.MovieDownloadView.as_view(), name='moviedownload'),
]

urlpatterns = [
    # ex: /
    url(r'^$', views.IndexView.as_view(), name='index'),
    # url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    # ex: /post/ /page/
    url(posttype_pattern + '$', views.EntrytypeView.as_view(), name='posttype'),
    # url(posttype_pattern + '$', views.posttype, name='posttype'),
    # ex: /movie/fighting-club
    url(r'^(?P<posttype_slug>movie)/' + '(?P<post_slug>[\w-]+)/', include(moviepatterns)),
    # ex: /post/first-news /page/about-us
    url(posttype_pattern + '(?P<post_slug>[\w-]+)/$', views.EntryView.as_view(), name='entry'),
    # url(posttype_pattern + '(?P<post_slug>[\w-]+)/$', views.post, name='post'),
    # ex: /category/ /star/ /director/ /maker/
    url(taxonomy_pattern + '$', views.TaxonomyView.as_view(), name='taxonomy'),
    # url(taxonomy_pattern + '$', views.taxonomy, name='taxonomy'),
    # ex: /star/will-smith
    url(taxonomy_pattern + '(?P<term_slug>[\w-]+)/$', views.TermView.as_view(), name='term'),
    # url(taxonomy_pattern + '(?P<term_slug>[\w-]+)/$', views.term, name='term'),
]
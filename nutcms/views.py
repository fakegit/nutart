import os

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, TemplateView

from .models import Entry
from .shortcuts import get_all_options, get_option, get_theme

# Create your views here.

class NutcmsView(TemplateView):
    """
    Custom TemplateView

    Add view instance attribute context and rewrite method get_context_data to update instance attribute context.
    """

    default_template_type = 'index'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {}
        self.site_options = get_all_options()

    def get_context_data(self, **kwargs):
        if 'view' not in self.context:
            self.context['view'] = self
        if 'site_options' not in self.context:
            self.context['site_options'] = self.site_options

    def pre_get_template_names(self):
        default_templates = {
            'index': ['index.html'],
            'single': ['index.html', 'single.html'],
            'post': ['index.html', 'single.html', 'post.html'],
            'page': ['index.html', 'single.html', 'page.html'],
            'search': ['search.html'],
            'login': ['login.html'],
            'register': ['register.html'],
            'archive': ['index.html', 'archive.html'],
            'taxonomy': ['index.html', 'taxonomy.html'],
        }
        template_names = default_templates[self.default_template_type]
        return template_names

    def _get_template_names(self):
        template_names = self.pre_get_template_names()
        if self.template_name is not None and self.template_name not in template_names:
            template_names.append(self.template_name)
        return template_names

    def get_template_names(self):
        return [os.path.join(self.site_options['theme'], __) for __ in reversed(self._get_template_names())]

    def get(self, request, *args, **kwargs):
        self.get_context_data(**kwargs)
        return self.render_to_response(self.context)


class IndexView(NutcmsView):

    template_name = 'index.html'

class TaxonomyView(NutcmsView):

    template_name = 'taxonomy.html'


def taxonomy(request, taxonomy_slug):
    taxonomyobj = get_object_or_404(slug=taxonomy_slug)
    theme = get_theme()
    template = theme + '/taxonomy.html'
    context = {'taxonomy': taxonomyobj}
    return render(request, template, context=context)

class TermView(NutcmsView):

    template_name = 'term.html'

def term(request, taxonomy_slug, term_slug):
    termobj = get_object_or_404(slug=term_slug, taxonomy__slug=taxonomy_slug)
    theme = get_theme()
    template = theme + '/term.html'
    context = {'term': termobj}
    return render(request, template, context=context)

class SingleTemplateMixin(object):

    default_template_type = 'single'

    def pre_get_template_names(self):
        template_names = super().pre_get_template_names()
        template_names.append(self.kwargs['posttype_slug'] + '.html')
        return template_names

class EntryView(SingleTemplateMixin, NutcmsView):

    def get_context_data(self, **kwargs):
        super().get_context_data(**kwargs)
        if self.kwargs['posttype_slug'] not in self.context:
            self.context[self.kwargs['posttype_slug']] = get_object_or_404(Entry, slug=self.kwargs['post_slug'], terms__slug=self.kwargs['posttype_slug'], terms__taxonomy__name='posttype')

class MovieView(SingleTemplateMixin, NutcmsView):

    def get_context_data(self, **kwargs):
        super().get_context_data(**kwargs)
        if self.kwargs['posttype_slug'] not in self.context:
            self.context[self.kwargs['posttype_slug']] = get_object_or_404(Entry, slug=self.kwargs['post_slug'], terms__slug=self.kwargs['posttype_slug'], terms__taxonomy__name='posttype')

class MoviePlayView(MovieView):

    def get_context_data(self, **kwargs):
        super().get_context_data(**kwargs)
        playlist = self.context[self.kwargs['posttype_slug']].resources.filter(entry__terms__slug='play', entry__terms__taxonomy__name='posttype')
        playlist_html = ['<table class="table table-striped table-condensed table-bordered"><tbody>']
        if playlist:
            for play in playlist:
                playlist_html.append('<tr><td>')
                playlist_html.append(play.entry.id)
                playlist_html.append('</td></tr>')
        else:
            playlist_html.append('<tr><td>No Link</td></tr>')
        playlist_html.append('</tbody></table>')
        playlist_html = ''.join(playlist_html)
        self.context['playlist'] = playlist
        self.context['playlist_html'] = playlist_html

    def pre_get_template_names(self):
        template_names = super().pre_get_template_names()
        template_names.append('movieplay.html')
        return template_names

class MovieDownloadView(MovieView):

    def get_context_data(self, **kwargs):
        super().get_context_data(**kwargs)
        downloadlist = self.context[self.kwargs['posttype_slug']].resources.filter(entry__terms__slug='download', entry__terms__taxonomy__name='posttype')
        self.context['downloadlist'] = downloadlist

    def pre_get_template_names(self):
        template_names = super().pre_get_template_names()
        template_names.append('moviedownload.html')
        return template_names

class EntrytypeView(NutcmsView):

    template_name = 'index.html'

def posttype(request, posttype_slug):
    return HttpResponse('posttype %s' % posttype_slug)

def login(request):
    template = get_theme() + '/login.html'
    context = {}
    return render(request, template, context=context)

def logout(request):
    return HttpResponse('Logout')

def register(request):
    template = get_theme() + '/register.html'
    context = {}
    return render(request, template, context=context)
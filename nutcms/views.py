import os

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, TemplateView

from .models import Entry
from .shortcuts import get_all_options, get_option, get_theme

# Create your views here.

class NutcmsView(TemplateView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {}
        self.site_options = get_all_options()

    def get_context_data(self, **kwargs):
        if 'view' not in self.context:
            self.context['view'] = self
        if 'site_options' not in self.context:
            self.context['site_options'] = self.site_options

    def get_template_names(self):
        return [os.path.join(self.site_options['theme'], self.template_name)]

    def get(self, request, *args, **kwargs):
        self.get_context_data(**kwargs)
        return self.render_to_response(self.context)


class OptionMixin(object):
    def get_options(self):
        options = get_all_options()
        return options

    def get_context_data(self, **kwargs):
        """
        Insert Site Options into the context dict.
        """
        if 'site_options' not in kwargs:
            kwargs['site_options'] = self.get_options()
        self.context.update(kwargs)
        return super().get_context_data(**kwargs)


class IndexView(NutcmsView):
    template_name = 'index.html'

def index(request):
    return HttpResponse('Home index')

class TaxonomyView(OptionMixin, ListView):
    template_name = get_theme() + '/taxonomy.html'


def taxonomy(request, taxonomy_slug):
    taxonomyobj = get_object_or_404(slug=taxonomy_slug)
    theme = get_theme()
    template = theme + '/taxonomy.html'
    context = {'taxonomy': taxonomyobj}
    return render(request, template, context=context)

class TermView(OptionMixin, ListView):
    template_name = get_theme() + '/term.html'

def term(request, taxonomy_slug, term_slug):
    termobj = get_object_or_404(slug=term_slug, taxonomy__slug=taxonomy_slug)
    theme = get_theme()
    template = theme + '/term.html'
    context = {'term': termobj}
    return render(request, template, context=context)

class EntryView(OptionMixin, DetailView):
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self):
        return get_object_or_404(Entry, slug=self.kwargs['post_slug'], terms__slug=self.kwargs['posttype_slug'], terms__taxonomy__name='posttype')

    def get_template_names(self):
        default_single_template = 'single.html'
        default_post_template = 'post.html'
        defautl_page_template = 'page.html'
        template_names = [default_single_template]
        # theme = get_theme()
        theme = self.context['site_options']['theme']
        if self.kwargs['posttype_slug']=='post':
            template_names.append(default_post_template)
        elif self.kwargs['posttype_slug']=='page':
            template_names.append(defautl_page_template)
        elif self.kwargs['posttype_slug']:
            template_names.append(default_post_template)
            template_names.append(self.kwargs['posttype_slug'] + '.html')
        if self.template_name is not None and self.template_name not in template_names:
            template_names.append(self.template_name)
        return [os.path.join(theme, __) for __ in reversed(template_names)]

def post(request, posttype_slug, post_slug):
    postobj = get_object_or_404(Entry, slug=post_slug, terms__slug=posttype_slug, terms__taxonomy__name='posttype')
    # url = reverse('nutcms:post', args=['post', 'hello-world'])
    # url = post.get_absolute_url()
    theme = get_theme()
    if posttype_slug=='post':
        template = '/post.html'
    elif posttype_slug=='page':
        template = '/page.html'
    else:
        template = '/single.html'
    template = theme + template
    context = {'post': postobj}
    return render(request, template, context=context)

class MovieView(OptionMixin, DetailView):
    context_object_name = 'movie'

    def get_object(self):
        return get_object_or_404(Entry, slug=self.kwargs['post_slug'], terms__slug='movie', terms__taxonomy__name='posttype')

    def get_template_names(self):
        default_single_template = 'single.html'
        theme = self.context['site_options']['theme']
        template_names = [default_single_template]
        template_names.append('movie.html')
        if self.template_name is not None and self.template_name not in template_names:
            template_names.append(self.template_name)
        return [os.path.join(theme, __) for __ in reversed(template_names)]

class MoviePlayView(OptionMixin, DetailView):
    context_object_name = 'movie'

    def get_object(self):
        return get_object_or_404(Entry, slug=self.kwargs['post_slug'], terms__slug='movie', terms__taxonomy__name='posttype')

    def get_template_names(self):
        default_single_template = 'single.html'
        theme = self.context['site_options']['theme']
        template_names = [default_single_template]
        template_names.append('playlist.html')
        if self.template_name is not None and self.template_name not in template_names:
            template_names.append(self.template_name)
        return [os.path.join(theme, __) for __ in reversed(template_names)]

class MovieDownloadView(DetailView):
    context_object_name = 'movie'

    def get_object(self):
        return get_object_or_404(Entry, slug=self.kwargs['post_slug'], terms__slug='movie', terms__taxonomy__name='posttype')

    def get_template_names(self):
        default_single_template = 'single.html'
        theme = self.context['site_options']['theme']
        template_names = [default_single_template]
        template_names.append('downloadlist.html')
        if self.template_name is not None and self.template_name not in template_names:
            template_names.append(self.template_name)
        return [os.path.join(theme, __) for __ in reversed(template_names)]

class EntrytypeView(OptionMixin, ListView):
    template_name = get_theme() + '/index.html'

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
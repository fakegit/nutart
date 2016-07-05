import os

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, TemplateView

from .models import Post
from .shortcuts import get_all_options, get_option, get_theme

# Create your views here.

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
        self.context = kwargs
        return super().get_context_data(**kwargs)


class IndexView(OptionMixin, TemplateView):
    template_name = get_theme() + '/index.html'

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

class PostView(OptionMixin, DetailView):
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self):
        return get_object_or_404(Post, slug=self.kwargs['post_slug'], terms__slug=self.kwargs['posttype_slug'], terms__taxonomy__name='posttype')

    def get_template_names(self):
        template_names = ['single.html']
        # theme = get_theme()
        theme = self.context['site_options']['theme']
        if self.kwargs['posttype_slug']=='post':
            template_names.append('post.html')
        elif self.kwargs['posttype_slug']=='page':
            template_names.append('page.html')
        if self.template_name is not None and self.template_name not in template_names:
            template_names.append(self.template_name)
        return [os.path.join(theme, __) for __ in reversed(template_names)]


def post(request, posttype_slug, post_slug):
    postobj = get_object_or_404(Post, slug=post_slug, terms__slug=posttype_slug, terms__taxonomy__name='posttype')
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

class PosttypeView(OptionMixin, ListView):
    template_name = get_theme() + '/index.html'

def posttype(request, posttype_slug):
    return HttpResponse('posttype %s' % posttype_slug)

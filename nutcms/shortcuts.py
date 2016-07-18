from .models import Entry, Taxonomy, Term, Option


def get_all_posttypes():
    return Term.objects.filter(taxonomy__name='posttype')

def get_all_taxonomies():
    return Taxonomy.objects.all()

def get_all_options(autoload=True):
    options = Option.objects.filter(autoload=autoload)
    if options:
        options = {__.key: __.value for __ in options}
    return options

def get_option(key):
    try:
        o = Option.objects.get(key=key)
    except:
        return None
    return o.value

def get_theme():
    theme = get_option('theme')
    if theme is None:
        theme = 'default'
    return theme

def get_post_by_id(id):
    try:
        p = Entry.objects.get(pk=id)
    except:
        return None
    return p

def get_post_by_slug(slug, term='post', taxonomy='posttype'):
    try:
        p = Entry.objects.get(slug=slug, terms__name=term, terms__taxonomy__name=taxonomy)
    except:
        return None
    return p

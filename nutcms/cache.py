from django.core.cache import caches

from .models import Option, Term, Taxonomy

NUTCMS_CACHE = caches['nutcms']

CACHE_SETTING = 'nutcms_setting'
CACHE_TYPE = 'nutcms_type'
CACHE_TAXONOMY = 'nutcms_taxonomy'


def get_type_cache():
    data = NUTCMS_CACHE.get(Term._meta.db_table, 'empty')
    if data == 'empty':
        data = {}
        for nutcms_type in Term.objects.filter(taxonomy__name='type'):
            data[nutcms_type.name] = nutcms_type.slug
        NUTCMS_CACHE.set(Term._meta.db_table, data)
    return data

def get_option_cache():
    data = NUTCMS_CACHE.get(Option._meta.db_table, 'empty')
    if data == 'empty':
        data = {}
        for setting in Setting.objects.iterator():
            if setting.autoload:
                data[setting.key] = setting.value
        NUTCMS_CACHE.set(Option._meta.db_table, data)
    return data

def get_taxonomy_cache():
    data = NUTCMS_CACHE.get(Taxonomy._meta.db_table, 'empty')
    if data == 'empty':
        data = {}
        for taxonomy in Taxonomy.objects.iterator():
            data[taxonomy.name] = taxonomy.slug
        NUTCMS_CACHE.set(Taxonomy._meta.db_table, data)
    return data

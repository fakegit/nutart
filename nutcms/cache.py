from django.core.cache import caches

from .models import Setting, Term, Taxonomy

NUTCMS_CACHE = caches['nutcms']

CACHE_SETTING = 'nutcms_setting'
CACHE_TYPE = 'nutcms_type'
CACHE_TAXONOMY = 'nutcms_taxonomy'


def get_type_cache():
    data = NUTCMS_CACHE.get(CACHE_TYPE, 'empty')
    if data == 'empty':
        data = {}
        for nutcms_type in Term.objects.filter(taxonomy__name='type'):
            data[nutcms_type.name] = nutcms_type.slug
        NUTCMS_CACHE.set(CACHE_TYPE, data)
    return data

def get_setting_cache():
    data = NUTCMS_CACHE.get(CACHE_SETTING, 'empty')
    if data == 'empty':
        data = {}
        for setting in Setting.objects.iterator():
            if setting.autoload:
                data[setting.key] = setting.value
        NUTCMS_CACHE.set(CACHE_SETTING, data)
    return data

def get_taxonomy_cache():
    data = NUTCMS_CACHE.get(CACHE_TAXONOMY, 'empty')
    if data == 'empty':
        data = {}
        for taxonomy in Taxonomy.objects.iterator():
            data[taxonomy.name] = taxonomy.slug
        NUTCMS_CACHE.set(CACHE_TAXONOMY, data)
    return data

def get_type_list():
    return [__ for __ in get_type_cache().values()]



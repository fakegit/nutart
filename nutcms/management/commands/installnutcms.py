from django.core.management.base import BaseCommand, CommandError

from nutcms.models import Setting, Taxonomy, Term

class Command(BaseCommand):
    help = 'Init nutcms'

    def handle(self, *args, **options):
        nutcms_init()
        self.stdout.write('ok')

def nutcms_init():
    default_setting = [
        ('site-name', 'Nutart'),
        ('site-description', 'This is a nutcms.'),
        ('site-url', ''),
        ('home', ''),
    ]

    default_taxonomy = [
        ('posttype', 'posttype'),
        ('category', 'category'),
    ]

    default_term = [
        ('posttype', 'post', 'post'),
        ('posttype', 'page', 'page'),
    ]

    for __ in [Setting(key=key, value=value, autoload=True) for key, value in default_setting]:
        __.save()

    for __ in [Taxonomy(name=name, slug=slug) for (name, slug) in default_taxonomy]:
        __.save()


    for __ in [Term(taxonomy=Taxonomy.objects.get(name=taxonomy), name=name, slug=slug) for (taxonomy, name, slug) in default_term]:
        __.save()

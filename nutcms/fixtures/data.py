# django-admin loaddata data.py
[
    {
        "model": "nutcms.Setting",
        "pk": 1,
        "fields": {
            "key": "site_name",
            "value": "Nutart"
        }
    },
    {
        "model": "nutcms.Setting",
        "pk": 2,
        "fields": {
            "key": "site_description",
            "value": "This is a nutcms."
        }
    },
    {
        "model": "nutcms.Setting",
        "pk": 3,
        "fields": {
            "key": "site_url",
            "value": "/"
        }
    },
    {
        "model": "nutcms.Setting",
        "pk": 4,
        "fields": {
            "key": "home",
            "value": "/"
        }
    },
    {
        "model": "nutcms.Setting",
        "pk": 5,
        "fields": {
            "key": "theme",
            "value": "default"
        }
    },
    {
        "model": "nutcms.Taxonomy",
        "pk": 1,
        "fields": {
            "name": "posttype",
            "slug": "posttype"
        }
    },
    {
        "model": "nutcms.Taxonomy",
        "pk": 2,
        "fields": {
            "name": "category",
            "slug": "category"
        }
    },
    {
        "model": "nutcms.Term",
        "pk": 1,
        "fields": {
            "taxonomy": 1,
            "name": "post",
            "slug": "post"
        }
    },
    {
        "model": "nutcms.Term",
        "pk": 2,
        "fields": {
            "taxonomy": 1,
            "name": "page",
            "slug": "page"
        }
    },
    {
        "model": "nutcms.Term",
        "pk": 2,
        "fields": {
            "taxonomy": 2,
            "name": "attachment",
            "slug": "attachment"
        }
    },
]
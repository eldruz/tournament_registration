DIRECTORIES = (
    ('registration', 'DJANGO_CONFIGURATION=Test python manage.py test -v 2 registration'),
    ('capitalism', 'DJANGO_CONFIGURATION=Test python manage.py test -v 2 capitalism'),
    ('export', 'DJANGO_CONFIGURATION=Test python manage.py test -v 2 export'),
)
IGNORE_EXTENSIONS = ('swp',)

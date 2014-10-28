DIRECTORIES = (
    ('registration', 'DJANGO_CONFIGURATION=Test python manage.py test -v 2 registration'),
    ('capitalism', 'DJANGO_CONFIGURATION=Test python manage.py test -v 2 capitalism')
)
IGNORE_EXTENSIONS = ('swp',)

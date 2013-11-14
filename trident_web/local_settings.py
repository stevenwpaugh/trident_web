DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Put a string here for the base_dir (where you did the git clone)
# like "/home/username/trident_web" or "C:/Users/username/Desktop/trident_web"
base_dir = '/home/spaugh/Repos/trident_web'

db_engine = 'django.db.backends.sqlite3'
db_name = base_dir + '/sqlite3.db'
db_user = 'ple'
db_passwd = ''
db_host = 'localhost'

template_dir = base_dir + '/templates'
interpolator_filename = base_dir + '/interpolator.sav'
static_root = base_dir + '/static'
staticfiles_source = base_dir + '/static_source'

from_email = 'trident@example.com'

secret_key = 'shouldbeuniqueandverylongandrandomseedjangodocs'

TRIDENT_EXE_PATH = "/usr/bin/trident"

ALLOWED_HOSTS = ['example.com']


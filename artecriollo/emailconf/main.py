import os
from dotenv import load_dotenv
load_dotenv()


EMAIL_FROM = os.getenv('EMAIL_FROM')
EMAIL_BCC = os.getenv('EMAIL_BCC')

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'


# DEFAULT_FROM_EMAIL= env('DEFAULT_FROM_EMAIL')
NOTIFY_EMAIL= env('NOTIFY_EMAIL')
# EMAIL_HOST_USER='mail@mail.com'
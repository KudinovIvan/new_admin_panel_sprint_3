import os

STATIC_URL = '_static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '_media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
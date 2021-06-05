from django.conf import settings

if settings.APP_NAME == 'esr21_subjectt_validations':
    from .tests import models

from django.conf import settings

if settings.APP_NAME == 'esr21_subject_validations':
    from .tests import models

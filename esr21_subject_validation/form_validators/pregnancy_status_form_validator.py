from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_base.utils import age, get_utcnow
from edc_constants.constants import OTHER, YES
from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator


class PregnancyStatusFormValidator(CRFFormValidator, FormValidator):

    subject_consent_model = 'esr21_subject.informedconsent'

    @property
    def subject_consent_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    def clean(self):

        self.m2m_required_if(YES,
                             field='contraceptive_usage',
                             m2m_field='contraceptive')

        spontaneous_miscarriages = self.cleaned_data.get('number_miscarriages') or 0

        self.required_if_true(spontaneous_miscarriages > 0,
                              field_required='date_miscarriages',)

        self.validate_other_specify(field='contraceptive')

        self.m2m_other_specify(OTHER,
                               m2m_field='contraceptive',
                               field_other='contraceptive_other')

        self.applicable_if_true(self.participant_age > 50,
                                field_applicable='post_menopausal_range')

        self.validate_other_specify(field='post_menopausal')

        super().clean()

    @property
    def participant_age(self):

        subject_identifier = self.cleaned_data.get('subject_visit').subject_identifier

        try:
            subject_consent_obj = self.subject_consent_cls.objects.get(
                subject_identifier=subject_identifier)
        except self.subject_consent_cls.DoesNotExist:
            raise ValidationError(
                    'Please complete Subject Consent form '
                    f'before proceeding.')
        else:
            return age(subject_consent_obj.dob, get_utcnow()).years

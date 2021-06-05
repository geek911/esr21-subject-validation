from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_base.utils import age
from edc_constants.constants import MALE, FEMALE
from edc_form_validators import FormValidator


class InformedConsentFormValidator(FormValidator):

    eligibility_confirmation_model = 'esr21_subject.eligibilityconfirmation'

    @property
    def eligibility_confirmation_cls(self):
        return django_apps.get_model(self.eligibility_confirmation_model)

    def clean(self):
        self.screening_identifier = self.cleaned_data.get('screening_identifier')
        super().clean()

        self.validate_dob()
        self.validate_identity_gender()

    def validate_identity_gender(self):

        identity_key = self.cleaned_data.get('identity')[4]
        gender = self.cleaned_data.get('gender')

        if gender == MALE and identity_key != '1':
            message = {'identity': 'The national identity number '
                       f'does not match the pattern expected. Expected the '
                       f'fifth digit as \'1\' for male, got \'{identity_key}\''}
            self._errors.update(message)
            raise ValidationError(message)
        elif gender == FEMALE and identity_key != '2':
            message = {'identity': 'The national identity number '
                       f'does not match the pattern expected. Expected the '
                       f'fifth digit as \'2\' for female, got \'{identity_key}\''}
            self._errors.update(message)
            raise ValidationError(message)

    def validate_dob(self):
        try:
            eligibility_confirmation = self.eligibility_confirmation_cls.objects.get(
                screening_identifier=self.screening_identifier)
        except self.eligibility_confirmation_cls.DoesNotExist:
            raise ValidationError('Please complete the Eligibility Confirmation '
                                  'form first.')
        else:
            dob = self.cleaned_data.get('dob')
            consent_date = self.cleaned_data.get('consent_datetime').date()
            age_in_years = age_in_years = age(dob, consent_date).years

            if (eligibility_confirmation.age_in_years
                    and eligibility_confirmation.age_in_years != age_in_years):
                message = {'dob':
                           'The age derived from Date of birth does not '
                           'match the age provided in the Potlako+ Eligibility'
                           f' form. Expected \'{eligibility_confirmation.age_in_years}\' '
                           f'got \'{age_in_years}\''}
                self._errors.update(message)
                raise ValidationError(message)

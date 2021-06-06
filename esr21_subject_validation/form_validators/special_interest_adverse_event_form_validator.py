from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator


class SpecialInterestAdverseEventFormValidator(FormValidator):

    def clean(self):
        cleaned_data = self.cleaned_data
        self.validate_aesi_end_date(cleaned_data=cleaned_data)
        self.validate_date_aware_of(cleaned_data=cleaned_data)

    def validate_aesi_end_date(self, cleaned_data=None):
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date', None)

        if end_date and end_date < start_date:
            message = {'end_date':
                       'AESI end date can not be before AESI start date'}
            self._errors.update(message)
            raise ValidationError(message)

    def validate_date_aware_of(self, cleaned_data=None):
        date_aware_of = cleaned_data.get('date_aware_of')
        start_date = cleaned_data.get('start_date')
        if date_aware_of and date_aware_of < start_date:
            message = {'date_aware_of':
                       'The date investigator became aware of AESI can not be '
                       'before the start date.'}
            self._errors.update(message)
            raise ValidationError(message)

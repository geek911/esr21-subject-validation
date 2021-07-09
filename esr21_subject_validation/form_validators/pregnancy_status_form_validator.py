# from django.core.exceptions import ValidationError
from edc_constants.constants import YES
from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator


class PregnancyStatusFormValidator(CRFFormValidator, FormValidator):

    def clean(self):

        self.required_if(YES,
                         field='contraceptive_usage',
                         field_required='contraceptive')

        spontaneous_miscarriages = self.cleaned_data.get('number_miscarriages') or 0

        self.required_if_true(spontaneous_miscarriages > 0,
                              field_required='date_miscarriages',)

        self.validate_other_specify(field='contraceptive')

        super().clean()

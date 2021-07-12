from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator


class VitalStatusFormValidator(CRFFormValidator, FormValidator):

    def clean(self):
        super().clean()

        self.validate_other_specify(field='reason_not_drawn')

        self.validate_other_specify(field='item_type')

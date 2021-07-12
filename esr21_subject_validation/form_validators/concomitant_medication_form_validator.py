from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator


class ConcomitantMedicationFormValidator(CRFFormValidator, FormValidator):

    def clean(self):

        self.validate_other_specify(field='unit')

        self.validate_other_specify(field='frequency')

        self.validate_other_specify(field='route')

        super().clean()

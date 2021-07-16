from edc_constants.constants import YES
from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator


class VaccineDetailsFormValidator(CRFFormValidator, FormValidator):

    def clean(self):
        self.required_if(YES, field="received_dose", field_required="is_received_dose")

        self.validate_other_specify(field="location", other_specify_field="location_other")

        super().clean()

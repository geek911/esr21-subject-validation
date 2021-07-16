from edc_constants.constants import YES, NO
from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator
from ..constants import FIRST_DOSE


class VaccineDetailsFormValidator(CRFFormValidator, FormValidator):

    def clean(self):

        self.required_if(YES,
                         field="received_dose",
                         field_required="is_received_dose")

        self.required_if(YES,
                         field="received_dose",
                         field_required="vaccination_site")

        self.required_if(YES,
                         field="received_dose",
                         field_required="vaccination_date")

        self.required_if(YES,
                         field="received_dose",
                         field_required="admin_per_protocol")

        self.required_if(NO,
                         field="admin_per_protocol",
                         field_required="reason_not_per_protocol")

        self.required_if(YES,
                         field="received_dose",
                         field_required="lot_number")

        self.required_if(YES,
                         field="received_dose",
                         field_required="expiry_date")

        self.required_if(YES,
                         field="received_dose",
                         field_required="provider_name")

        self.validate_other_specify(field="location")

        self.required_if(FIRST_DOSE,
                         field="is_received_dose",
                         field_required="next_vaccination_data")

        super().clean()

from edc_constants.constants import YES, NO
from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator
from ..constants import FIRST_DOSE


class VaccineDetailsFormValidator(CRFFormValidator, FormValidator):

    def clean(self):

        required_fields = ['received_dose_before', 'vaccination_site',
                           'vaccination_date', 'admin_per_protocol']

        for required_field in required_fields:
            self.required_if(YES,
                             field='received_dose',
                             field_required=required_field)

        self.required_if(NO,
                         field='admin_per_protocol',
                         field_required='reason_not_per_protocol')

        received_fields = ['lot_number', 'expiry_date', 'provider_name']

        for received_field in received_fields:

            self.required_if(YES,
                             field='received_dose',
                             field_required=received_field)

        self.validate_other_specify(field='location')

        self.required_if(FIRST_DOSE,
                         field='received_dose_before',
                         field_required='next_vaccination_data')

        super().clean()

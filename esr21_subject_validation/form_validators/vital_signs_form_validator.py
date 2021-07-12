from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator
from edc_constants.constants import NO, YES


class VitalSignsFormValidator(CRFFormValidator, FormValidator):

    def clean(self):

        self.applicable_if(NO,
                           field='vital_signs_measured',
                           field_applicable='reason_vitals_nd')

        self.required_if(YES,
                         field='vital_signs_measured',
                         required_field='assessment_dt')

        fields_required = ['assessment_dt', 'systolic_bp',
                           'diastolic_bp', 'heart_rate',
                           'body_temp', 'oxygen_saturated']

        for field in fields_required:
            self.required_if(YES,
                             field='vital_signs_measured',
                             field_required=field)

        self.applicable_if_true(self.cleaned_data.get('body_temp') is not None,
                                field_applicable='body_temp_unit')

        super().clean()

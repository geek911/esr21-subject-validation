from django.core.exceptions import ValidationError
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from edc_form_validators import FormValidator
from .crf_form_validator import CRFFormValidator
from ..constants import FIRST_DOSE
from esr21_subject.models import VaccinationDetails
from django.db.models import Q


class VaccineDetailsFormValidator(CRFFormValidator, FormValidator):

    def clean(self):

        required_fields = ['vaccination_site', 'vaccination_date', 'lot_number',
                           'expiry_date', 'provider_name']

        for required_field in required_fields:
            self.required_if(YES,
                             field='received_dose',
                             field_required=required_field)

        applicable_fields = ['received_dose_before', 'location',
                             'admin_per_protocol']

        for applicable_field in applicable_fields:
            self.applicable_if(YES,
                               field='received_dose',
                               field_applicable=applicable_field)

        self.validate_subject_doses()

        self.required_if(NO,
                         field='admin_per_protocol',
                         field_required='reason_not_per_protocol')

        self.validate_other_specify(field='location')

        self.required_if(FIRST_DOSE,
                         field='received_dose_before',
                         field_required='next_vaccination_date')

        super().clean()

    def validate_subject_doses(self):
        """
        This is a validation which check if the vaccination is first or second dose
        """

        received_dose_before = self.cleaned_data.get('received_dose_before')
        subject_visit = self.cleaned_data.get('subject_visit')

        if received_dose_before == 'first_dose' and subject_visit.schedule_name != 'esr21_enrol_schedule':
            # validation for second visit
            raise ValidationError({'received_dose_before': 'Should be a second dose because its the first visi'})

        if received_dose_before == 'second_dose' and subject_visit.schedule_name == 'esr21_enrol_schedule':
            # validation for first visit
            raise ValidationError({'received_dose_before': 'Should be first dose because its the first visit'})

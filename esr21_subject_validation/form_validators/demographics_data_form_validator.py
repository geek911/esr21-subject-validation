from edc_constants.choices import NO
from edc_form_validators import FormValidator


class DemographicsDataFormValidator(FormValidator):

    def clean(self):
        super().clean()

        self.validate_other_specify(field='if_no_reason')
        self.validate_other_specify(field='ethnicity')
        self.required_if(
            NO,
            field='childbearing_potential',
            field_required='if_no_reason')
        self.required_if(
            'reported',
            field='race_of_subject',
            field_required='race')

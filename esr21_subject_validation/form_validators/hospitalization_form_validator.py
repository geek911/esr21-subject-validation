from edc_constants.choices import NO
from edc_form_validators import FormValidator


class HospitalizationFormValidator(FormValidator):

    def clean(self):
        super().clean()

        self.required_if(NO, field='ongoing',
                         field_required='stop_date')

        self.validate_other_specify(field='reason')

        self.required_if('covid19_related_symptoms', field='reason',
                         field_required='covid_symptoms')
from edc_constants.choices import YES
from edc_form_validators import FormValidator


class Covid19SymptomaticInfectionsFormValidator(FormValidator):

    def clean(self):
        super().clean()

        self.validate_symptomatic_experiences()

        self.required_if(
            YES,
            field='visits',
            field_required='hospitalisation_date')

    def validate_symptomatic_experiences(self):
        fields = ['symptomatic_infections', 'date_of_infection']
        for field in fields:
            self.required_if(
                YES,
                field='symptomatic_experiences',
                field_required=field)

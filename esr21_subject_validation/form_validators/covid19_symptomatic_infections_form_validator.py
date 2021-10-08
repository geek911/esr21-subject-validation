from edc_constants.choices import YES
from edc_constants.constants import OTHER
from edc_form_validators import FormValidator


class Covid19SymptomaticInfectionsFormValidator(FormValidator):

    def clean(self):
        super().clean()

        self.validate_symptomatic_experiences()

        self.required_if(
            YES,
            field='visits',
            field_required='hospitalisation_date')

        self.m2m_required_if(YES,
                             field='symptomatic_infections_experiences',
                             m2m_field='symptomatic_infections')

        self.m2m_other_specify(OTHER,
                               m2m_field='symptomatic_infections',
                               field_other='symptomatic_infections_other', )

    def validate_symptomatic_experiences(self):
        fields = ['symptomatic_infections', 'date_of_infection']
        for field in fields:
            self.required_if(
                YES,
                field='symptomatic_experiences',
                field_required=field)

from edc_constants.choices import NO
from edc_form_validators import FormValidator


class HospitalisationFormValidator(FormValidator):

    def clean(self):
        """
        All validations defined in directly on the forms will be called by the super
        """
        super().clean()

        """
        Stop date is required if the symptoms are no longer on going
        """
        self.required_if(NO, field='ongoing',
                         field_required='stop_date')

        """
        Will make the {varable}_other required 
        """
        self.validate_other_specify(field='reason')


        self.required_if('covid19_related_symptoms', field='reason',
                         field_required='covid_symptoms')
from django.core.exceptions import ValidationError
from edc_constants.choices import NO
from edc_form_validators import FormValidator
from django import forms

class DemographicsDataFormValidator(FormValidator):

    def clean(self):
        """
        All validations defined in directly on the forms will be called by the super
        """
        super().clean()


        """
        Will make the {varable}_other required 
        """
        self.validate_other_specify(field='ethnicity')
        self.validate_other_specify(field='employment_status')
        self.validate_other_specify(field='marital_status')

        """
        Number of people in a household cannot be negative
        """
        self.household_members = self.cleaned_data.get('household_members')

        if self.household_members < 0:
            self.validation_error_message('Number cannot be negative')
    

    def validation_error_message(msg: str):
        raise forms.ValidationError(msg)

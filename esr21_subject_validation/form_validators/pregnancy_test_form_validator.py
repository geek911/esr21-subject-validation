from edc_constants.choices import YES
from edc_form_validators import FormValidator

class PregnancyTestFormValidator(FormValidator):

    def clean(self):
        super().clean()
        self.required_if(YES, field = 'preg_performed', field_required='result')

from edc_constants.choices import YES
from edc_form_validators import FormValidator


class RapidHivTestingFormValidator(FormValidator):

    def clean(self):
        super().clean()

        self.required_if(
            YES,
            field='rapid_test_done',
            field_required='result_date')

        self.required_if(
            YES,
            field='rapid_test_done',
            field_required='result')

from edc_constants.choices import YES
from edc_form_validators import FormValidator


class RapidHivTestingFormValidator(FormValidator):

    def clean(self):
        super().clean()

        self.required_if(
            YES,
            field='rapid_test_done',
            field_required='rapid_test_date')

        self.required_if(
            YES,
            field='rapid_test_done',
            field_required='rapid_test_result')

        self.required_if(
            YES,
            field='prev_hiv_test',
            field_required='hiv_result'
        )

        self.required_if(
            YES,
            field='prev_hiv_test',
            field_required='hiv_test_date'
        )

        self.applicable_if(
            YES,
            field='prev_hiv_test',
            field_applicable='evidence_hiv_status'
        )

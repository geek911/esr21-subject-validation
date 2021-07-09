from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import POS, YES, NOT_APPLICABLE

from ..form_validators import RapidHivTestingFormValidator


class TestRapidHivTestingForm(TestCase):

    def setUp(self):

        self.rapid_hiv_testing_options = {
            'rapid_test_done': YES,
            'result_date': get_utcnow(),
            'result': POS, }

    def test_rapid_hiv_testing(self):
        form_validator = RapidHivTestingFormValidator(
            cleaned_data=self.rapid_hiv_testing_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_result_invalid(self):
        self.rapid_hiv_testing_options['result'] = None

        form_validator = RapidHivTestingFormValidator(
            cleaned_data=self.rapid_hiv_testing_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('result', form_validator._errors)

from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow, relativedelta

from ..form_validators import EligibilityConfirmationFormValidator


class TestEligibilityConfirmationForm(TestCase):

    def test_eligibility_report_datetime_valid(self):
        cleaned_data = {
            'report_datetime': get_utcnow(),
            'age_in_years': 45,
        }
        form_validator = EligibilityConfirmationFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_eligibility_report_datetime_invalid(self):
        cleaned_data = {
            'report_datetime': get_utcnow() - relativedelta(months=6),
            'age_in_years': 45,
        }
        form_validator = EligibilityConfirmationFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('report_datetime', form_validator._errors)

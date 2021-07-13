from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_constants.constants import NO, OTHER, YES

from ..form_validators import PregnancyStatusFormValidator


class TestPregnancyStatusForm(TestCase):

    def setUp(self):

        self.pregnancy_status_options = {
            'contraceptive_usage': NO,
            'number_miscarriages': 0,
            'date_miscarriages': None}

    def test_pregnancy_status_data(self):
        """ Assert that form is valid. """
        form_validator = PregnancyStatusFormValidator(
            cleaned_data=self.pregnancy_status_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_contraceptive_usage_invalid(self):
        """ Assert that if contraception usage is YES, then contraception specification
         is required.
        """
        self.pregnancy_status_options['contraceptive_usage'] = YES

        form_validator = PregnancyStatusFormValidator(
            cleaned_data=self.pregnancy_status_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('contraceptive', form_validator._errors)

    def test_number_miscarriages_date_invalid(self):
        """ Assert that if number of miscarriages is 1 or greater, then date of last
         miscarriage is required.
        """
        self.pregnancy_status_options['number_miscarriages'] = 1

        form_validator = PregnancyStatusFormValidator(
            cleaned_data=self.pregnancy_status_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('date_miscarriages', form_validator._errors)

    def test_contraceptive_other_invalid(self):
        """ Assert that if contraception specificcation is Other, then contraception other
         is required.
        """
        self.pregnancy_status_options['contraceptive_usage'] = YES
        self.pregnancy_status_options['contraceptive'] = OTHER

        form_validator = PregnancyStatusFormValidator(
            cleaned_data=self.pregnancy_status_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('contraceptive_other', form_validator._errors)

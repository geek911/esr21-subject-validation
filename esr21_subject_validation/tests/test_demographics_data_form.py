from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import NO, MALE, FEMALE, OTHER, YES

from ..form_validators import DemographicsDataFormValidator
from .models import ListModel


class TestDemographicsDataForm(TestCase):

    def setUp(self):
        DemographicsDataFormValidator.demographics_data_model = \
            'esr21_subject_validation.demographicsdata'

        self.demographics_options = {
            'dob': (get_utcnow() - relativedelta(years=45)).date(),
            'age': 45,
            'gender': FEMALE,
            'childbearing_potential': NO,
            'if_no_reason': OTHER,
            'if_no_reason_other': 'Test',
            'ethnicity': OTHER,
            'ethnicity_other': 'Asian',
            'race_of_subject': 'reported',
            'race': ['american', 'asian', 'african',
                     'pacific_islander', 'white']}

    def test_demographics_data(self):
        form_validator = DemographicsDataFormValidator(
            cleaned_data=self.demographics_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_ethnicity_other_other_invalid(self):
        self.demographics_options['ethnicity'] = 'Black African'

        form_validator = DemographicsDataFormValidator(
            cleaned_data=self.demographics_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('ethnicity_other', form_validator._errors)

    def test_if_no_reason_invalid(self):
        self.demographics_options['childbearing_potential'] = YES

        form_validator = DemographicsDataFormValidator(
            cleaned_data=self.demographics_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('if_no_reason', form_validator._errors)

    def test_race_invalid(self):
        self.demographics_options['race_of_subject'] = 'not_reported'
        form_validator = DemographicsDataFormValidator(
            cleaned_data=self.demographics_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('race', form_validator._errors)

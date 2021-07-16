from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import NO, FEMALE, NONE, OTHER, YES

from ..form_validators import DemographicsDataFormValidator


class TestDemographicsDataForm(TestCase):

    def setUp(self):
         self.data = {
            'dob': (get_utcnow() - relativedelta(years=45)).date(),
            'household_members': 23,
            'age': '45',
            'gender': FEMALE,
            'childbearing_potential': NO,
            'if_no_reason': OTHER,
            'if_no_reason_other': 'Test',
            'ethnicity': NONE,
            'employment_status': NONE,
            'marital_status':  NONE,
            'race_of_subject': 'reported',
            'household_members': 6,
            'race': ['american', 'asian', 'african',
                     'pacific_islander', 'white']}

    def test_demographics_can_be_validated(self):
        """
        General tests
        """
        form_validator = DemographicsDataFormValidator(
            cleaned_data=self.data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_ethnicity_other_invalid(self):
        """
        If enthnicity is other, then enthnicity_other is required or else an exception will be thrown
        """
        self.data['ethnicity'] = OTHER
        form_validator = DemographicsDataFormValidator(cleaned_data=self.data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_employment_status_other_invalid(self):
        """
        If employee is other, then employee_other is required or else an exception will be thrown
        """
        self.data['employment_status'] =  OTHER
        form_validator = DemographicsDataFormValidator(cleaned_data=self.data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_marital_status_other_invalid(self):
        """
        If maritalstatus is other, then maritalstatus_other is required or else an exception will be thrown
        """
        self.data['marital_status'] =  OTHER
        form_validator = DemographicsDataFormValidator(cleaned_data=self.data)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_house_members_negative_number_invalid(self):
        """
        If house_members should be a positive integer or else an exception will be thrown
        """
        self.data['household_members'] = -27
        form_validator = DemographicsDataFormValidator(cleaned_data=self.data)
        self.assertRaises(ValidationError, form_validator.validate)


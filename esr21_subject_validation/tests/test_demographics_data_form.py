from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import NO, MALE, FEMALE, OTHER, YES

from ..form_validators import DemographicsDataFormValidator
from .models import ListModel


class TestDemographicsDataForm(TestCase):


    def test_demographics_can_be_validated(self):
        demographics_options = {
            'dob': (get_utcnow() - relativedelta(years=45)).date(),
            'household_members': '23',
            'age': '45',
            'gender': FEMALE,
            'childbearing_potential': NO,
            'if_no_reason': OTHER,
            'if_no_reason_other': 'Test',
            'ethnicity': OTHER,
            'ethnicity_other': 'ABC',
            'race_of_subject': 'reported',
            'race': ['american', 'asian', 'african',
                     'pacific_islander', 'white']}
        form_validator = DemographicsDataFormValidator(
            cleaned_data=demographics_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_ethnicity_is_other_then_ethnicityother_is_required(self):

        demographics_options = {
            'dob': (get_utcnow() - relativedelta(years=45)).date(),
            'household_members': '23',
            'age': '45',
            'gender': FEMALE,
            'childbearing_potential': NO,
            'ethnicity': OTHER,
            'race_of_subject': 'reported',
            'race': ['american', 'asian', 'african',
                     'pacific_islander', 'white']}

        form_validator = DemographicsDataFormValidator(
            cleaned_data=demographics_options)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_employmentstatus_is_other_then_employmentstatusother_is_required(self):

        demographics_options = {
            'dob': (get_utcnow() - relativedelta(years=45)).date(),
            'household_members': '23',
            'age': '45',
            'gender': FEMALE,
            'childbearing_potential': NO,
            'employment_status': OTHER,
            'race_of_subject': 'reported',
            'race': ['american', 'asian', 'african',
                     'pacific_islander', 'white']}

        form_validator = DemographicsDataFormValidator(
            cleaned_data=demographics_options)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_maritalstatus_is_other_then_maritalstatusother_is_required(self):

        demographics_options = {
            'dob': (get_utcnow() - relativedelta(years=45)).date(),
            'household_members': '23',
            'age': '45',
            'gender': FEMALE,
            'childbearing_potential': NO,
            'marital_status': OTHER,
            'race_of_subject': 'reported',
            'race': ['american', 'asian', 'african',
                     'pacific_islander', 'white']}

        form_validator = DemographicsDataFormValidator(
            cleaned_data=demographics_options)
        self.assertRaises(ValidationError, form_validator.validate)

    def test_if_house_members_cannot_be_negative(self):

        demographics_options = {
            'dob': (get_utcnow() - relativedelta(years=45)).date(),
            'household_members': '23',
            'age': '45',
            'gender': FEMALE,
            'childbearing_potential': NO,
            'marital_status': OTHER,
            'household_members': -27,
            'race_of_subject': 'reported',
            'race': ['american', 'asian', 'african',
                     'pacific_islander', 'white']}


        form_validator = DemographicsDataFormValidator(
            cleaned_data=demographics_options)
        self.assertRaises(ValidationError, form_validator.validate)


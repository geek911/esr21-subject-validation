from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_constants.constants import NO, OTHER, YES, NOT_APPLICABLE

from ..form_validators import MedicalHistoryFormValidator
from .models import ListModel


class TestMedicalHistoryForm(TestCase):

    def setUp(self):

        self.medical_history_options = {
            'prior_covid_infection': NO,
            'no_internal_trips': 0,
            'mode_of_transport': None,
            'comorbidities': None}

    def test_medical_history_valid(self):
        """ Assert that form is valid. """
        form_validator = MedicalHistoryFormValidator(
            cleaned_data=self.medical_history_options)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_covid_symptoms_invalid(self):
        """ Assert that if the participant has had prior covid infection then symptoms
         are required.
        """
        self.medical_history_options['prior_covid_infection'] = YES

        form_validator = MedicalHistoryFormValidator(
            cleaned_data=self.medical_history_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('covid_symptoms', form_validator._errors)

    def test_covid_symptoms_other_invalid(self):
        """ Assert that if covid symptoms is other, then sypmtoms_other is required."""
        self.medical_history_options['prior_covid_infection'] = YES
        ListModel.objects.create(short_name=OTHER)
        self.medical_history_options['covid_symptoms'] = ListModel.objects.all()

        form_validator = MedicalHistoryFormValidator(
            cleaned_data=self.medical_history_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('symptoms_other', form_validator._errors)

    def test_comorbidities_other_invalid(self):
        """ Assert that if comorbidities is Other, then comorbidities_other
         is required.
        """
        ListModel.objects.create(short_name=OTHER)
        self.medical_history_options['comorbidities'] = ListModel.objects.all()

        form_validator = MedicalHistoryFormValidator(
            cleaned_data=self.medical_history_options)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('comorbidities_other', form_validator._errors)

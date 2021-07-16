from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import NO, YES, OTHER

from ..form_validators import VaccineDetailsFormValidator


class VaccinationDetailsFormValidatorTests(TestCase):

    def test_is_received_dose_invalid(self):
        """
        Test if received_dose is YES, then is_received_dose is required
        hence a ValidationError will be raised
        """
        data = {
            'received_dose': YES
        }

        form = VaccineDetailsFormValidator(cleaned_data=data)
        self.assertRaises(ValidationError, form.validate)

    def test_location_other_invalid(self):
        """
        Test if location is OTHER, then location_other is required
        hence a ValidationError will be raised
        """
        data = {
            'location': OTHER
        }
        form = VaccineDetailsFormValidator(cleaned_data=data)
        self.assertRaises(ValidationError, form.validate)

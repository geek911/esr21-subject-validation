from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow, relativedelta
from edc_constants.constants import NO, YES, OTHER

from ..form_validators import VaccineDetailsFormValidator


class VaccinationDetailsFormValidatorTests(TestCase):

    def test_is_received_dose_invalid(self):
        data = {
            'received_dose': YES
        }

        form = VaccineDetailsFormValidator(cleaned_data=data)
        self.assertRaises(ValidationError, form.validate)

    def test_location_other_invalid(self):
        data = {
            'location': OTHER
        }
        form = VaccineDetailsFormValidator(cleaned_data=data)
        self.assertRaises(ValidationError, form.validate)
